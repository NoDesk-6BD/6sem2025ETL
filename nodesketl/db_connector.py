# Gerencia as conexões com bancos de dados SQL Server e PostgreSQL.

import pyodbc
import psycopg2
from config import Config

def connect_sql_server():
    """Cria e retorna a conexão com o SQL Server."""
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={Config.SQL_SERVER_HOST};"
        f"DATABASE={Config.SQL_SERVER_DB};"
        f"UID={Config.SQL_SERVER_USER};"
        f"PWD={Config.SQL_SERVER_PASSWORD};"
    )
    try:
        conn = pyodbc.connect(conn_str, autocommit=True)
        print("Conexão com SQL Server estabelecida com sucesso.")
        return conn
    except pyodbc.Error as ex:
        sql_error = ex.args[1].decode('utf-8')
        print(f"Erro de conexão com o SQL Server: {sql_error}")
        return None

def connect_postgresql():
    """Cria e retorna a conexão com o PostgreSQL."""
    return psycopg2.connect(
        host=Config.PG_DB_HOST,
        port=Config.PG_DB_PORT,
        user=Config.PG_DB_USER,
        password=Config.PG_DB_PASSWORD,
        dbname=Config.PG_DB_NAME
    )