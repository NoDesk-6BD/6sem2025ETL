import pandas as pd
from datetime import timedelta

def transform_tickets(df_first_date, df_tickets):
    start_date = pd.to_datetime(df_first_date.iloc[0, 0]).date()
    end_date = pd.Timestamp.today().date()

    open_tickets = []   
    evolution = []      

    current_date = start_date
    while current_date <= end_date:
        created_today = df_tickets[
            pd.to_datetime(df_tickets["CreatedAt"]).dt.date == current_date
        ]

        changed_today = df_tickets[
            (pd.to_datetime(df_tickets["ChangedAt"]).dt.date == current_date) &
            (df_tickets["ToStatusId"].isin([1, 2, 3]))
        ]

        to_add = pd.concat([created_today, changed_today])

        for _, row in to_add.iterrows():
            ticket_obj = {
                "TicketId": row["TicketId"],
                "Categoria": row["Category"],
                "Subcategoria": row["Subcategories"]
            }
            if not any(t["TicketId"] == row["TicketId"] for t in open_tickets):
                open_tickets.append(ticket_obj)

        closed_today = df_tickets[
            (pd.to_datetime(df_tickets["ChangedAt"]).dt.date == current_date) &
            (df_tickets["ToStatusId"].isin([4, 5]))
        ]

        for _, row in closed_today.iterrows():
            open_tickets = [t for t in open_tickets if t["TicketId"] != row["TicketId"]]

        evolution.append({
            "date": current_date,
            "tickets": open_tickets.copy()  
        })

        current_date += timedelta(days=1)

    return evolution
