import pandas as pd
from datetime import timedelta


def transform_tickets(df_first_date, df_tickets):
    start_date = pd.to_datetime(df_first_date.iloc[0, 0]).date()
    end_date = pd.Timestamp.today().date()

    open_tickets = []
    evolution = []

    current_date = start_date

    while current_date <= end_date:
        created_today = df_tickets[pd.to_datetime(df_tickets["CreatedAt"]).dt.date == current_date]

        # Tickets que mudaram para status aberto, em atendimento, aguardando cliente hoje
        changed_today = df_tickets[
            (pd.to_datetime(df_tickets["ChangedAt"]).dt.date == current_date)
            & (df_tickets["ToStatusId"].isin([1, 2, 3]))
        ]

        # Todos os tickets que devem ser adicionados
        to_add = pd.concat([created_today, changed_today])

        for _, row in to_add.iterrows():
            open_tickets[row["TicketId"]] = {
                "TicketId": row["TicketId"],
                "Categoria": row["Category"],
                "Subcategoria": row["Subcategories"],
            }

        # Tickets fechados hoje
        closed_today = df_tickets[
            (pd.to_datetime(df_tickets["ChangedAt"]).dt.date == current_date) & (df_tickets["ToStatusId"].isin([4, 5]))
        ]

        for _, row in closed_today.iterrows():
            open_tickets.pop(row["TicketId"], None)  # remove se existir

        evolution.append({"date": current_date, "tickets": open_tickets.copy()})

        # Próximo dia
        current_date += timedelta(days=1)

    return evolution
