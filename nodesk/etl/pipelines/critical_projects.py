from datetime import datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from ..settings import Settings
from ..databases import sqlserver, mongo
from ..models import Ticket, Product

settings = Settings()

OPEN_STATUS_IDS = (1, 2, 3)  # 1=Aberto, 2=Em Atendimento, 3=Aguardando Cliente


def critical_projects_pipeline(limit: int = 10):
    with Session(sqlserver) as session:
        stmt = (
            select(
                Ticket.product_id,
                Product.name,
                func.count(Ticket.ticket_id).label("open_count"),
            )
            .join(Product, Product.product_id == Ticket.product_id)
            .where(Ticket.current_status_id.in_(OPEN_STATUS_IDS))
            .group_by(Ticket.product_id, Product.name)
            .order_by(func.count(Ticket.ticket_id).desc())
            .limit(limit)
        )
        rows = session.execute(stmt).all()

    return [
        {
            "product_id": pid,
            "product_name": pname,
            "open_tickets": int(count),
        }
        for (pid, pname, count) in rows
    ]


def save_snapshot_to_mongo(rows: list[dict], limit: int) -> str:
    doc = {
        "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        "limit": limit,
        "open_status_ids": list(OPEN_STATUS_IDS),
        "rows": rows,
    }
    coll = mongo["critical_projects"]
    coll.insert_one(doc)
    return f"Inserted snapshot into {settings.MONGO_DB}.critical_projects"


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Critical Projects")
    parser.add_argument("--limit", type=int, default=10, help="Top N projects with most opened tickets (default: 10)")
    parser.add_argument("--save-mongo", action="store_true", help="Save snapshot to MongoDB")
    args = parser.parse_args()

    rows = critical_projects_pipeline(limit=args.limit)
    print(json.dumps(rows, ensure_ascii=False, indent=2))

    if args.save_mongo:
        msg = save_snapshot_to_mongo(rows, limit=args.limit)
        print(msg)
