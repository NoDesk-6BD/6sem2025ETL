#!/bin/bash
set -e

# senha SA vem da variável de ambiente MSSQL_SA_PASSWORD ou fallback
SA_PASS="${MSSQL_SA_PASSWORD:-SqlServer@6}"
BACPAC_PATH="/backup.bacpac"
IMPORT_MARKER="/var/opt/mssql/.bacpac_imported"

echo "ENTRYPOINT: iniciando sqlservr em background..."
/opt/mssql/bin/sqlservr &

SQLSRV_PID=$!

# Espera até o SQL Server aceitar conexões (timeout controlado)
echo "ENTRYPOINT: aguardando SQL Server ficar disponível..."
TRIES=0
MAX_TRIES=60
until /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "$SA_PASS" -Q "SELECT 1" > /dev/null 2>&1; do
  TRIES=$((TRIES+1))
  if [ "$TRIES" -ge "$MAX_TRIES" ]; then
    echo "ERROR: SQL Server não ficou disponível em tempo (timeout). Saindo."
    kill "$SQLSRV_PID" || true
    exit 1
  fi
  echo -n "."
  sleep 5
done
echo
echo "ENTRYPOINT: SQL Server pronto."

# Criar o banco pro4tech se não existir
echo "ENTRYPOINT: criando database 'pro4tech' se não existir..."
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "$SA_PASS" -Q "IF DB_ID('pro4tech') IS NULL CREATE DATABASE pro4tech;"
echo "ENTRYPOINT: database pronto."

# Importar bacpac apenas se existir e não tiver sido importado antes
if [ -f "$BACPAC_PATH" ]; then
  if [ -f "$IMPORT_MARKER" ]; then
    echo "ENTRYPOINT: BACPAC já importado anteriormente. Pulando import."
  else
    echo "ENTRYPOINT: importando BACPAC ($BACPAC_PATH) para pro4tech..."
    if /usr/bin/sqlpackage /a:Import \
      /sf:"$BACPAC_PATH" \
      /tsn:localhost \
      /tdn:pro4tech \
      /tu:sa \
      /tp:"$SA_PASS" \
      /TargetTrustServerCertificate:true
    then
      echo "ENTRYPOINT: importacao concluida com sucesso."
      touch "$IMPORT_MARKER"
      chown mssql:mssql "$IMPORT_MARKER" || true
    else
      echo "ENTRYPOINT: erro na importacao do bacpac (sqlpackage retornou erro)."
      kill "$SQLSRV_PID" || true
      exit 1
    fi
  fi
else
  echo "ENTRYPOINT: arquivo BACPAC nao encontrado em $BACPAC_PATH. Pulando import."
fi

# Mantém o processo do SQL Server em foreground
echo "ENTRYPOINT: aguardando processo do SQL Server (pid $SQLSRV_PID)..."
wait "$SQLSRV_PID"