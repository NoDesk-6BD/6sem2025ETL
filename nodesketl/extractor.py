from db_connector import connect_sql_server
import pyodbc

def extract_table(table_name, columns):
    """Extrai dados de uma tabela específica do SQL Server e retorna como lista de tuplas."""
    conn = None
    try:
        conn = connect_sql_server()
        cursor = conn.cursor()
        query = f'SELECT {", ".join(columns)} FROM "{table_name}" ORDER BY 1'
        cursor.execute(query)
        data = cursor.fetchall()
        print(f"Extração da tabela '{table_name}' concluída. {len(data)} registros encontrados.")
        return data
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Erro de extração em '{table_name}': {sqlstate}")
        return None
    finally:
        if conn:
            conn.close()

def extract_users():
    return extract_table("Users", ["UserId", "CompanyId", "FullName", "Email", "Phone", "CPF", "CreatedAt", "IsVIP"])

def extract_agents():
    return extract_table("Agents", ["AgentId", "FullName", "Email", "Phone", "DepartmentId", "IsActive", "HiredAt"])