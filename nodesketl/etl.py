'''
Script principal, orquestra o processo completo, seguindo a ordem de dependência.
    Extração: Ler todos os dados das tabelas do SQL Server Express.
    Transformação: Reestruturar os dados das tabelas Users e Agents para isolar as informações pessoais, e atribuir o papel de viewer a todos os agentes.
    Carga (Ordenada): Inserir os dados no PostgreSQL na seguinte ordem:
    Nível 1 (Sem dependências): Companies, Departments, Priorities, Products, SLA_Plans, Statuses, Categories, Tags, Roles (se ainda não existirem).
    Nível 2: Users (dados não-pessoais), Agents (dados não-pessoais), Subcategories.
    Nível 3 (LGPD/RBAC): UserPersonalData, AgentPersonalData, AgentsRoles.
    Nível 4 (Dados Principais): Tickets.
    Nível 5 (Dados de Log e Interação): TicketInteractions, Attachments, TicketStatusHistory, TicketTags, AuditLogs
'''
import sys
from extractor import extract_table, extract_users, extract_agents
from transformer import transform_users, transform_agents
from loader import load_data, load_user_personal_data, load_agent_personal_data, load_agents_roles


def run_etl():
    print("Iniciando o processo de ETL completo...")

    try:
        # Extração de todos os dados na ordem correta
        print("1. Extraindo dados do SQL Server...")
        raw_data = {}

        # Nível 1: Tabelas sem dependências
        raw_data["Companies"] = extract_table("Companies", ["CompanyId", "Name", "CNPJ", "Segmento", "CreatedAt"])
        raw_data["Departments"] = extract_table("Departments", ["DepartmentId", "Name"])
        raw_data["Priorities"] = extract_table("Priorities", ["PriorityId", "Name", "Weight"])
        raw_data["Products"] = extract_table("Products",
                                             ["ProductId", "Name", "Code", "Description", "IsActive", "CreatedAt"])
        raw_data["SLA_Plans"] = extract_table("SLA_Plans", ["SLAPlanId", "Name", "FirstResponseMins", "ResolutionMins"])
        raw_data["Statuses"] = extract_table("Statuses", ["StatusId", "Name"])
        raw_data["Categories"] = extract_table("Categories", ["CategoryId", "Name"])
        raw_data["Tags"] = extract_table("Tags", ["TagId", "Name"])

        # Extração de Usuários e Agentes
        raw_data["Users"] = extract_users()
        raw_data["Agents"] = extract_agents()

        # Nível 2: Tabelas com dependências de Nível 1
        raw_data["Subcategories"] = extract_table("Subcategories", ["SubcategoryId", "CategoryId", "Name"])

        # Nível 3: Tickets
        raw_data["Tickets"] = extract_table("Tickets",
                                            ["TicketId", "CompanyId", "CreatedByUserId", "AssignedAgentId", "ProductId",
                                             "CategoryId", "SubcategoryId", "PriorityId", "CurrentStatusId",
                                             "SLAPlanId", "Title", "Description", "Channel", "Device", "CreatedAt",
                                             "FirstResponseAt", "ClosedAt"])

        # Nível 4: Tabelas com dependências de Tickets
        raw_data["TicketInteractions"] = extract_table("TicketInteractions",
                                                       ["InteractionId", "TicketId", "AuthorType", "AuthorUserId",
                                                        "AuthorAgentId", "Message", "IsPublic", "CreatedAt"])
        raw_data["Attachments"] = extract_table("Attachments",
                                                ["AttachmentId", "TicketId", "FileName", "MimeType", "SizeBytes",
                                                 "StoragePath", "UploadedAt"])
        raw_data["TicketStatusHistory"] = extract_table("TicketStatusHistory",
                                                        ["HistoryId", "TicketId", "FromStatusId", "ToStatusId",
                                                         "ChangedAt", "ChangedByAgentId"])
        raw_data["TicketTags"] = extract_table("TicketTags", ["TicketId", "TagId"])
        raw_data["AuditLogs"] = extract_table("AuditLogs",
                                              ["AuditId", "EntityType", "EntityId", "Operation", "PerformedBy",
                                               "PerformedAt", "DetailsJson"])

        # Carregando dados no PostgreSQL
        print("\n2. Carregando dados no PostgreSQL...")

        # Nível 1
        print("-> Carregando tabelas de Nível 1...")
        load_data("Companies", raw_data["Companies"], ["CompanyId", "Name", "CNPJ", "Segmento", "CreatedAt"])
        load_data("Departments", raw_data["Departments"], ["DepartmentId", "Name"])
        load_data("Priorities", raw_data["Priorities"], ["PriorityId", "Name", "Weight"])
        load_data("Products", raw_data["Products"],
                  ["ProductId", "Name", "Code", "Description", "IsActive", "CreatedAt"])
        load_data("SLA_Plans", raw_data["SLA_Plans"], ["SLAPlanId", "Name", "FirstResponseMins", "ResolutionMins"])
        load_data("Statuses", raw_data["Statuses"], ["StatusId", "Name"])
        load_data("Categories", raw_data["Categories"], ["CategoryId", "Name"])
        load_data("Tags", raw_data["Tags"], ["TagId", "Name"])

        # Nível 2 e 3: Usuários e Agentes (LGPD/RBAC)
        print("-> Carregando dados de Usuários e Agentes (LGPD/RBAC)...")
        users_for_db, users_personal_data = transform_users(raw_data["Users"])
        load_data("Users", users_for_db, ["UserId", "CompanyId", "CreatedAt"])
        load_user_personal_data(users_personal_data)

        agents_for_db, agents_personal_data, agents_roles = transform_agents(raw_data["Agents"])
        load_data("Agents", agents_for_db, ["AgentId", "DepartmentId", "IsActive", "HiredAt"])
        load_agent_personal_data(agents_personal_data)
        load_agents_roles(agents_roles)

        # Nível 2
        print("-> Carregando tabelas de Nível 2...")
        load_data("Subcategories", raw_data["Subcategories"], ["SubcategoryId", "CategoryId", "Name"])

        # Nível 4
        print("-> Carregando a tabela Tickets...")
        load_data("Tickets", raw_data["Tickets"],
                  ["TicketId", "CompanyId", "CreatedByUserId", "AssignedAgentId", "ProductId", "CategoryId",
                   "SubcategoryId", "PriorityId", "CurrentStatusId", "SLAPlanId", "Title", "Description", "Channel",
                   "Device", "CreatedAt", "FirstResponseAt", "ClosedAt"])

        # Nível 5
        print("-> Carregando tabelas de Nível 5...")
        load_data("TicketInteractions", raw_data["TicketInteractions"],
                  ["InteractionId", "TicketId", "AuthorType", "AuthorUserId", "AuthorAgentId", "Message", "IsPublic",
                   "CreatedAt"])
        load_data("Attachments", raw_data["Attachments"],
                  ["AttachmentId", "TicketId", "FileName", "MimeType", "SizeBytes", "StoragePath", "UploadedAt"])
        load_data("TicketStatusHistory", raw_data["TicketStatusHistory"],
                  ["HistoryId", "TicketId", "FromStatusId", "ToStatusId", "ChangedAt", "ChangedByAgentId"])
        load_data("TicketTags", raw_data["TicketTags"], ["TicketId", "TagId"])
        load_data("AuditLogs", raw_data["AuditLogs"],
                  ["AuditId", "EntityType", "EntityId", "Operation", "PerformedBy", "PerformedAt", "DetailsJson"])

        print("\nProcesso de ETL completo concluído com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro fatal durante o ETL: {e}", file=sys.stderr)


if __name__ == "__main__":
    run_etl()
