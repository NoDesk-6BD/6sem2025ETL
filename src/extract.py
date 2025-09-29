import pandas as pd
from sqlalchemy import create_engine
import urllib


def extract_sqlserver_for_evolution_chart(config):
    """
    Extrai dados do SQL Server usando SQLAlchemy para evitar warnings do pandas.
    Retorna o df da primeira data e df dos tickets (histórico completo).
    """
    driver = config["driver"]
    server = config["server"]
    database = config["database"]
    username = config["user"]
    password = config["password"]

    # String de conexão segura
    params = urllib.parse.quote_plus(
        f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    )
    conn = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

    query_first_date = "SELECT TOP 1 CreatedAt FROM Tickets ORDER BY createdat ASC;"
    df_first_date = pd.read_sql(query_first_date, conn)

    query_tickets = (
        "SELECT TicketId, FromStatusId, ToStatusId, ChangedAt, "
        "Categories.Name as Category, Sucategories.Name as Subcategories, CreatedAt "
        "FROM TicketStatusHistory JOIN Ticket ON TicketStatusHistory.TicketId = Ticket.TicketId "
        "JOIN Categories ON Ticket.CategoryId = Categories.CategoryId "
        "JOIN Subcategories ON Ticket.SubcategoryId = Subcategory.SubcategoryId"
    )
    df_tickets = pd.read_sql(query_tickets)

    return df_first_date, df_tickets


# def extract_postgres(config):
#     conn = psycopg2.connect(
#         host=config["host"],
#         port=config["port"],
#         database=config["database"],
#         user=config["user"],
#         password=config["password"]
#     )
#     query = "SELECT * FROM chamados LIMIT 10;"  # Exemplo
#     df = pd.read_sql(query, conn)
#     conn.close()
#     return df
