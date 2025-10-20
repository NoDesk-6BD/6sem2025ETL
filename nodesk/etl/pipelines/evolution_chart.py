from nodesk.etl.settings import Settings
from src.extract import extract_sqlserver_for_evolution_chart
from src.transform import transform_tickets
from src.load import load_evolution_to_mongo


def evolution_chart_pipeline():
    print("🚀 Iniciando ETL do Evolution Chart...")

    # Extract
    print("📥 Extraindo dados do SQL Server...")
    df_first_date, df_tickets = extract_sqlserver_for_evolution_chart()

    # Transform
    print("🔄 Transformando dados...")
    evolution = transform_tickets(df_first_date, df_tickets)

    # Load
    print("📤 Carregando dados no MongoDB...")
    settings = Settings()
    mongo_uri = settings.MONGO_URI
    load_evolution_to_mongo(
        evolution, mongo_uri=mongo_uri, db_name=settings.MONGO_DB, collection_name="tickets_evolution"
    )

    print("✅ Pipeline concluída com sucesso!")


if __name__ == "__main__":
    evolution_chart_pipeline()
