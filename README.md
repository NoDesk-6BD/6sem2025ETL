<!-- Badges -->
![Python](https://img.shields.io/badge/python-3.13%2B-blue)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

# ETL - NoDesk - Pro4tech (API Fatec)

API ETL repository for the 6th Semester of the Database course at FATEC - São José dos Campos

<br>

## Stack

* **Python** 3.11+
* **pytest**
* **ruff**, **pre-commit** (code quality)

<br>

## Installation

### 1. Prepare the .env file

The `.env` file contains configuration variables (keys, database, etc.). Copy the `.env-example` and adjust as needed.

### 2. Install and prepare the environment:

Prepare the environment with project's dependencies

```bash
pip install -r requirements.txt
```

### 3. Install and active the pre-commit hook:

```bash
pre-commit install --hook-type commit-msg --hook-type pre-commit
```

<br>

## Running in development

```bash
 python.exe .\nodesketl\etl.py
```

<br>

## Code Quality

Through of the pre-commit, code quality will be ensured using `ruff`.

#### 1. Format:

```bash
ruff format .
```

#### 2. Lint (with autofix via pre-commit):

```bash
ruff check .
```

# 6sem2025ETL
Repositório etl da API para o 6º Semestre do curso de Banco de Dados da FATEC - São José dos Campos

rodar:
    docker network create db_etl
    docker compose up --build
    docker compose -f docker-compose-etl.yml up --build

docker exec -it 6sem2025etl-mongo-1 mongosh "mongodb://root:Mongo6@localhost:27017"
use pro4tech


