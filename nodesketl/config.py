# Carregará as configurações do .env

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # SQL Server (Origem)
    SQL_SERVER_HOST = os.getenv("SQL_SERVER_HOST")
    SQL_SERVER_DB = os.getenv("SQL_SERVER_DB")
    SQL_SERVER_USER = os.getenv("SQL_SERVER_USER")
    SQL_SERVER_PASSWORD = os.getenv("SQL_SERVER_PASSWORD")

    # PostgreSQL (Destino)
    PG_DB_HOST = os.getenv("DB_HOST")
    PG_DB_PORT = os.getenv("DB_PORT")
    PG_DB_USER = os.getenv("DB_USER")
    PG_DB_PASSWORD = os.getenv("DB_PASSWORD")
    PG_DB_NAME = os.getenv("DB_NAME")
