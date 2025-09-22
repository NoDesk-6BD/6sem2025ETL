import psycopg2
from db_connector import connect_postgresql


def load_data(table_name, data, columns):
    """Insere dados em uma tabela no PostgreSQL."""
    if not data:
        print(f"Sem dados para carregar na tabela '{table_name}'.")
        return

    conn = None
    try:
        conn = connect_postgresql()
        cursor = conn.cursor()

        pg_columns = [f'"{col}"' for col in columns]
        placeholders = ', '.join(['%s'] * len(columns))

        query = f'INSERT INTO "{table_name}" ({", ".join(pg_columns)}) VALUES ({placeholders}) ON CONFLICT DO NOTHING'

        cursor.executemany(query, data)
        conn.commit()
        print(f"-> {len(data)} registros carregados na tabela '{table_name}'.")
    except psycopg2.Error as ex:
        print(f"Erro ao carregar dados na tabela '{table_name}': {ex}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def load_roles(data):
    load_data("Roles", data, ["RoleId", "RoleName"])


def load_user_personal_data(data):
    load_data("UserPersonalData", data, ["UserId", "FullName", "Email", "Phone", "CPF", "IsVIP"])


def load_agent_personal_data(data):
    load_data("AgentPersonalData", data, ["AgentId", "FullName", "Email", "Phone"])


def load_agents_roles(data):
    load_data("AgentsRoles", data, ["AgentId", "RoleId"])
