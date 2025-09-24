# 6sem2025ETL
Repositório etl da API para o 6º Semestre do curso de Banco de Dados da FATEC - São José dos Campos

rodar:
    docker network create db_etl
    docker-compose up --build
    docker-compose -f docker-compose-etl.yml up --build --no-cache
