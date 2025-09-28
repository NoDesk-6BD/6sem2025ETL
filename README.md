# 6sem2025ETL
Repositório etl da API para o 6º Semestre do curso de Banco de Dados da FATEC - São José dos Campos

rodar:
    docker network create db_etl
    docker compose up --build
    docker compose -f docker-compose-etl.yml up --build

docker exec -it 6sem2025etl-mongo-1 mongosh "mongodb://root:Mongo6@localhost:27017"
use pro4tech


