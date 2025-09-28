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
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

    # Query para pegar a primeira data
    query_first_date = """
    SELECT TOP 1 Tickets.CreatedAt AS FirstCreatedAt
    FROM Tickets
    ORDER BY Tickets.CreatedAt ASC;
    """
    df_first_date = pd.read_sql(query_first_date, engine)

    # Query para pegar histórico completo de tickets
    query_tickets = """
    SELECT Tickets.TicketId, FromStatusId, ToStatusId, ChangedAt,
           Categories.Name AS Category, Subcategories.Name AS Subcategories, CreatedAt
    FROM Tickets
    LEFT JOIN TicketStatusHistory ON TicketStatusHistory.TicketId = Tickets.TicketId
    JOIN Categories ON Tickets.CategoryId = Categories.CategoryId
    JOIN Subcategories ON Tickets.SubcategoryId = Subcategories.SubcategoryId
    """
    df_tickets = pd.read_sql(query_tickets, engine)

    # Debug rápido
    print("df_tickets (preview):")
    print(df_tickets.head(3))

    return df_first_date, df_tickets
