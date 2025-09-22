import pyodbc
import psycopg2
import pandas as pd

def extract_sqlserver_for_evolution_chart(config):
    conn_str = (
        f"DRIVER={config['driver']};"
        f"SERVER={config['server']};"
        f"DATABASE={config['database']};"
        f"UID={config['user']};"
        f"PWD={config['password']}"
    )
    conn = pyodbc.connect(conn_str)

    query_first_date = "SELECT TOP 1 CreatedAt " \
    "FROM Tickets " \
    "ORDER BY createdat ASC;"
    df_first_date = pd.read_sql(query_first_date, conn)

    query_tickets = "SELECT TicketId, FromStatusId, ToStatusId, ChangedAt, " \
    "Categories.Name as Category, Sucategories.Name as Subcategories, CreatedAt " \
    "FROM TicketStatusHistory JOIN Ticket ON TicketStatusHistory.TicketId = Ticket.TicketId " \
    "JOIN Categories ON Ticket.CategoryId = Categories.CategoryId " \
    "JOIN Subcategories ON Ticket.SubcategoryId = Subcategory.SubcategoryId"
    df_tickets = pd.read_sql(query_tickets)

    conn.close()
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
