from sqlalchemy.orm import Session
from sqlalchemy import select

from . import models, schemas


# Email Recipients CRUD
def create_recipient(db: Session, data: schemas.RecipientCreate) -> models.EmailRecipient:
    recipient = models.EmailRecipient(name=data.name, email=data.email)
    db.add(recipient)
    db.commit()
    db.refresh(recipient)
    return recipient


def get_recipient_by_email(db: Session, email: str) -> models.EmailRecipient | None:
    stmt = select(models.EmailRecipient).where(models.EmailRecipient.email == email)
    return db.execute(stmt).scalar_one_or_none()


def list_recipients(db: Session, skip: int = 0, limit: int = 100) -> list[models.EmailRecipient]:
    stmt = select(models.EmailRecipient).order_by(models.EmailRecipient.name).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars())


def delete_recipient_by_email(db: Session, email: str) -> bool:
    recipient = get_recipient_by_email(db, email)
    if not recipient:
        return False
    db.delete(recipient)
    db.commit()
    return True


# Articles CRUD (basic)
def list_articles(db: Session, limit: int | None = None) -> list[models.Article]:
    stmt = select(models.Article).order_by(models.Article.id.desc())
    if limit:
        stmt = stmt.limit(limit)
    return list(db.execute(stmt).scalars())


# Email Content CRUD (basic)
def get_latest_email_content(db: Session) -> models.EmailContent | None:
    stmt = select(models.EmailContent).order_by(models.EmailContent.created_at.desc()).limit(1)
    return db.execute(stmt).scalar_one_or_none()

