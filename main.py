from config.settings import SQLSERVER_CONFIG, MONGODB_CONFIG
from src.extract import extract_sqlserver_for_evolution_chart
from src.transform import transform_tickets
from src.load import load_evolution_to_mongo


def main():
    print("🚀 Iniciando ETL...")

    # Extract
    print("📥 Extraindo dados do SQL Server...")
    df_first_date, df_tickets = extract_sqlserver_for_evolution_chart(SQLSERVER_CONFIG)

    # Transform
    print("🔄 Transformando dados...")
    evolution = transform_tickets(df_first_date, df_tickets)

    # Load
    print("📤 Carregando dados no MongoDB...")
    mongo_uri = f"mongodb://root:Mongo6@{MONGODB_CONFIG['host']}:27017/admin"
    load_evolution_to_mongo(
        evolution, mongo_uri=mongo_uri, db_name=MONGODB_CONFIG["database"], collection_name=MONGODB_CONFIG["collection"]
    )

    print("✅ Pipeline concluída com sucesso!")


if __name__ == "__main__":
    main()
