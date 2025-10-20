# etl.Dockerfile
FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install Microsoft ODBC Driver 18 for SQL Server (per MS docs for Debian 12)
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl ca-certificates gnupg \
 && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc \
    | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
 && echo "deb [arch=amd64,arm64 signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" \
    > /etc/apt/sources.list.d/microsoft-prod.list \
 && apt-get update \
 && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
 # (optional, handy for debugging) \
 # && ACCEPT_EULA=Y apt-get install -y mssql-tools18 \
 # && echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' > /etc/profile.d/mssql-tools.sh \
 && rm -rf /var/lib/apt/lists/*

# Install Poetry (swap for pip + requirements.txt if you prefer)
RUN pip install --no-cache-dir poetry

WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
 && poetry install --only main --no-root

COPY . .

CMD ["python", "-m", "nodesk.etl.pipelines.evolution_chart", "--save-mongo", "main.py"]
