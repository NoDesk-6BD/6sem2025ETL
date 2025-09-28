FROM python:3.12-bullseye

# Instala dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    apt-transport-https \
    lsb-release \
    sudo \
    unixodbc \
    unixodbc-dev \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Adiciona repositório da Microsoft e instala driver ODBC
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    rm -rf /var/lib/apt/lists/*

# Diretório da aplicação
WORKDIR /project

# Dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código do ETL
COPY . .

CMD ["python", "main.py"]
