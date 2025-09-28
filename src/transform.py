import pandas as pd
from datetime import timedelta
from collections import Counter

from .utils import normalize_date

def transform_tickets(df_first_date, df_tickets):
    start_date = pd.to_datetime(df_first_date.iloc[0, 0]).date()
    end_date = pd.Timestamp.today().date()

    # PARA TESTES
    # start_date = pd.Timestamp("2025-09-04").date()
    # end_date = start_date + timedelta(days=2)

    open_tickets = {}   # dict: {TicketId: {"TicketId": ..., "Categoria": ..., "Subcategoria": ...}}
    evolution = []

    current_date = start_date

    while current_date <= end_date:
        print("current_date", current_date, "\n")
        current_date_ts = pd.Timestamp(current_date)

        # Tickets criados hoje
        created_today = df_tickets[
            pd.to_datetime(df_tickets["CreatedAt"]).dt.normalize() == current_date_ts
        ]

        # Tickets que mudaram para status aberto, em atendimento, aguardando cliente hoje
        changed_today = df_tickets[
            (pd.to_datetime(df_tickets["ChangedAt"]).dt.normalize() == current_date_ts) &
            (df_tickets["ToStatusId"].isin([1, 2, 3]))
        ]

        # Todos os tickets que devem ser adicionados
        to_add = pd.concat([created_today, changed_today])

        for _, row in to_add.iterrows():
            open_tickets[row["TicketId"]] = {
                "TicketId": row["TicketId"],
                "Categoria": row["Category"],
                "Subcategoria": row["Subcategories"]
            }

        # Tickets fechados hoje
        closed_today = df_tickets[
            (pd.to_datetime(df_tickets["ChangedAt"]).dt.normalize() == current_date_ts) &
            (df_tickets["ToStatusId"].isin([4, 5]))
        ]

        for _, row in closed_today.iterrows():
            open_tickets.pop(row["TicketId"], None)  # remove se existir

         # Contagem de categorias e subcategorias
        categories_count = Counter([t["Categoria"] for t in open_tickets.values()])
        subcategories_count = Counter([t["Subcategoria"] for t in open_tickets.values()])

        # Salvar a evolução do dia
        date_to_bson = normalize_date(current_date)
        evolution.append({
            "date": date_to_bson,
            "categories_count": dict(categories_count),
            "subcategories_count": dict(subcategories_count),
            # "tickets": list(open_tickets.values())
        })

        # Próximo dia
        current_date += timedelta(days=1)

    return evolution
