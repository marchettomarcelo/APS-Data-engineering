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


def get_recipient_by_id(db: Session, recipient_id: int) -> models.EmailRecipient | None:
    stmt = select(models.EmailRecipient).where(models.EmailRecipient.id == recipient_id)
    return db.execute(stmt).scalar_one_or_none()


def get_recipient_by_email(db: Session, email: str) -> models.EmailRecipient | None:
    stmt = select(models.EmailRecipient).where(models.EmailRecipient.email == email)
    return db.execute(stmt).scalar_one_or_none()


def list_recipients(db: Session, skip: int = 0, limit: int = 100) -> list[models.EmailRecipient]:
    stmt = select(models.EmailRecipient).order_by(models.EmailRecipient.name).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars())


def update_recipient(db: Session, recipient_id: int, data: schemas.RecipientUpdate) -> models.EmailRecipient | None:
    recipient = get_recipient_by_id(db, recipient_id)
    if not recipient:
        return None
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(recipient, key, value)
    
    db.commit()
    db.refresh(recipient)
    return recipient


def delete_recipient_by_email(db: Session, email: str) -> bool:
    recipient = get_recipient_by_email(db, email)
    if not recipient:
        return False
    db.delete(recipient)
    db.commit()
    return True


# Articles CRUD
def create_article(db: Session, data: schemas.ArticleCreate) -> models.Article:
    article = models.Article(url=data.url, title=data.title, content=data.content)
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


def get_article_by_id(db: Session, article_id: int) -> models.Article | None:
    stmt = select(models.Article).where(models.Article.id == article_id)
    return db.execute(stmt).scalar_one_or_none()


def get_article_by_url(db: Session, url: str) -> models.Article | None:
    stmt = select(models.Article).where(models.Article.url == url)
    return db.execute(stmt).scalar_one_or_none()


def list_articles(db: Session, skip: int = 0, limit: int = 100) -> list[models.Article]:
    stmt = select(models.Article).order_by(models.Article.id.desc()).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars())


def update_article(db: Session, article_id: int, data: schemas.ArticleUpdate) -> models.Article | None:
    article = get_article_by_id(db, article_id)
    if not article:
        return None
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(article, key, value)
    
    db.commit()
    db.refresh(article)
    return article


def delete_article(db: Session, article_id: int) -> bool:
    article = get_article_by_id(db, article_id)
    if not article:
        return False
    db.delete(article)
    db.commit()
    return True


# Email Content CRUD
def create_email_content(db: Session, data: schemas.EmailContentCreate) -> models.EmailContent:
    email_content = models.EmailContent(subject=data.subject, content=data.content)
    db.add(email_content)
    db.commit()
    db.refresh(email_content)
    return email_content


def get_email_content_by_id(db: Session, email_content_id: int) -> models.EmailContent | None:
    stmt = select(models.EmailContent).where(models.EmailContent.id == email_content_id)
    return db.execute(stmt).scalar_one_or_none()


def list_email_content(db: Session, skip: int = 0, limit: int = 100) -> list[models.EmailContent]:
    stmt = select(models.EmailContent).order_by(models.EmailContent.created_at.desc()).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars())


def get_latest_email_content(db: Session) -> models.EmailContent | None:
    stmt = select(models.EmailContent).order_by(models.EmailContent.created_at.desc()).limit(1)
    return db.execute(stmt).scalar_one_or_none()


def update_email_content(db: Session, email_content_id: int, data: schemas.EmailContentUpdate) -> models.EmailContent | None:
    email_content = get_email_content_by_id(db, email_content_id)
    if not email_content:
        return None
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(email_content, key, value)
    
    db.commit()
    db.refresh(email_content)
    return email_content


def delete_email_content(db: Session, email_content_id: int) -> bool:
    email_content = get_email_content_by_id(db, email_content_id)
    if not email_content:
        return False
    db.delete(email_content)
    db.commit()
    return True

