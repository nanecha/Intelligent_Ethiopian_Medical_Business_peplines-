from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas

def get_top_products(db: Session, limit: int = 10):
    result = (
        db.query(models.Message.message_text, func.count(models.Message.id).label("count"))
        .group_by(models.Message.message_text)
        .order_by(func.count(models.Message.id).desc())
        .limit(limit)
        .all()
    )
    return [{"product_name": r[0], "count": r[1]} for r in result]


def get_channel_activity(db: Session, channel_name: str):
    result = (
        db.query(func.date(models.Message.posted_at).label("date"),
                 func.count(models.Message.id).label("count"))
        .filter(models.Message.channel_name == channel_name)
        .group_by(func.date(models.Message.posted_at))
        .all()
    )
    return [{"date": str(r[0]), "count": r[1]} for r in result]


def search_messages(db: Session, query: str):
    return db.query(models.Message).filter(models.Message.message_text.ilike(f"%{query}%")).all()
