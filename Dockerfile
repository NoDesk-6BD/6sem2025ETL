FROM mcr.microsoft.com/mssql/server:2022-latest

# Variáveis de ambiente do SQL Server
ENV ACCEPT_EULA=Y
ENV MSSQL_PID=Developer
ENV SA_PASSWORD=SqlServer@6

# Rodar como root para instalar pacotes
USER root

# Instalar dependências, registrar repositório MS e instalar mssql-tools (sqlcmd)
RUN apt-get update && apt-get install -y curl apt-transport-https gnupg unzip ca-certificates lsb-release \
  && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
  && curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list \
       -o /etc/apt/sources.list.d/mssql-release.list \
  && apt-get update \
  && ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev mssql-tools \
  && ln -s /opt/mssql-tools/bin/sqlcmd /usr/bin/sqlcmd \
  && ln -s /opt/mssql-tools/bin/bcp /usr/bin/bcp

# Instalar sqlpackage (binário)
RUN apt-get install -y unzip curl \
  && curl -L -o /tmp/sqlpackage.zip https://aka.ms/sqlpackage-linux \
  && mkdir -p /opt/sqlpackage \
  && unzip /tmp/sqlpackage.zip -d /opt/sqlpackage \
  && chmod +x /opt/sqlpackage/sqlpackage \
  && ln -s /opt/sqlpackage/sqlpackage /usr/bin/sqlpackage \
  && rm /tmp/sqlpackage.zip \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copiar script de inicialização (apenas shell) e dar permissão
COPY init.sh /init.sh
RUN chmod +x /init.sh

# Voltar para usuário padrão do SQL Server
USER mssql

# ENTRYPOINT: o script inicia o sqlservr, faz a importação e depois espera
ENTRYPOINT ["/bin/bash", "/init.sh"]