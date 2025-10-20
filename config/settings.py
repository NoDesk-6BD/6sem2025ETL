import os

SQLSERVER_CONFIG = {
    "driver": os.getenv("MSSQL_DRIVER", "ODBC Driver 18 for SQL Server"),
    "server": os.getenv("MSSQL_HOST", "mssql"),
    "port": os.getenv("MSSQL_PORT", "1433"),
    "database": os.getenv("MSSQL_DATABASE", "NoDesk"),
    "user": os.getenv("MSSQL_USER", "sa"),
    "password": os.getenv("MSSQL_PASSWORD", "Abcd1234*"),
    "encrypt": os.getenv("MSSQL_ENCRYPT", "true"),
    "trust_server_certificate": os.getenv("MSSQL_TRUST_SERVER_CERTIFICATE", "true"),
}

MONGODB_CONFIG = {
    "uri": os.getenv("MONGO_URI", "mongodb://nodesk:nodesk@mongo:27017/?authSource=admin"),
    "database": os.getenv("MONGO_DB", "nodesk"),
    "port": os.getenv("MONGO_PORT", "27017"),
    "collection": os.getenv("MONGO_COLLECTION", "tickets_evolution"),
}

