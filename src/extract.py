import pandas as pd


def extract_sqlserver_for_evolution_chart():
    """
    Extrai dados do SQL Server usando SQLAlchemy para evitar warnings do pandas.
    Retorna o df da primeira data e df dos tickets (histórico completo).
    """
    from nodesk.etl.databases import sqlserver

     # Query para pegar a primeira data
    query_first_date = """
    SELECT TOP 1 Tickets.CreatedAt AS FirstCreatedAt
    FROM Tickets
    ORDER BY Tickets.CreatedAt ASC;
    """
    df_first_date = pd.read_sql(query_first_date, sqlserver)

    # Query para pegar histórico completo de tickets
    query_tickets = """
    SELECT Tickets.TicketId, FromStatusId, ToStatusId, ChangedAt,
           Categories.Name AS Category, Subcategories.Name AS Subcategories, CreatedAt
    FROM Tickets
    LEFT JOIN TicketStatusHistory ON TicketStatusHistory.TicketId = Tickets.TicketId
    JOIN Categories ON Tickets.CategoryId = Categories.CategoryId
    JOIN Subcategories ON Tickets.SubcategoryId = Subcategories.SubcategoryId
    """
    df_tickets = pd.read_sql(query_tickets, sqlserver)

    # Debug rápido
    print("df_tickets (preview):")
    print(df_tickets.head(3))

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
