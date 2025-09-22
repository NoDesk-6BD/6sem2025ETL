def transform_users(users_data):
    """Transforma dados de usuários para as novas tabelas Users e UserPersonalData."""
    if not users_data:
        return [], []

    new_users = []
    user_personal_data = []

    for user in users_data:
        # Pega os dados do negócio (tupla de User)
        new_users.append((user.UserId, user.CompanyId, user.CreatedAt))
        # Pega os dados pessoais (tupla de UserPersonalData)
        user_personal_data.append((user.UserId, user.FullName, user.Email, user.Phone, user.CPF, user.IsVIP))

    return new_users, user_personal_data


def transform_agents(agents_data):
    """Transforma dados de agentes para as novas tabelas Agents e AgentPersonalData."""
    if not agents_data:
        return [], [], []

    new_agents = []
    agent_personal_data = []
    agent_roles = []

    # O RoleId para 'viewer' é 3, conforme nosso script de criação
    VIEWER_ROLE_ID = 3

    for agent in agents_data:
        # Dados do Agente para a tabela Agents
        new_agents.append((agent.AgentId, agent.DepartmentId, agent.IsActive, agent.HiredAt))
        # Dados Pessoais do Agente
        agent_personal_data.append((agent.AgentId, agent.FullName, agent.Email, agent.Phone))
        # Atribui o papel de 'viewer' a todos os agentes
        agent_roles.append((agent.AgentId, VIEWER_ROLE_ID))

    return new_agents, agent_personal_data, agent_roles