from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, get_db_session
from . import crud, schemas, models


app = FastAPI(title="News Pipeline API", version="0.2.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.post("/recipients", response_model=schemas.RecipientRead, status_code=status.HTTP_201_CREATED)
def create_recipient(payload: schemas.RecipientCreate, db: Session = Depends(get_db_session)):
    existing = crud.get_recipient_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_recipient(db, payload)


@app.get("/recipients", response_model=list[schemas.RecipientRead])
def get_recipients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    return crud.list_recipients(db, skip=skip, limit=limit)


@app.get("/recipients/{recipient_id}", response_model=schemas.RecipientRead)
def get_recipient(recipient_id: int, db: Session = Depends(get_db_session)):
    recipient = crud.get_recipient_by_id(db, recipient_id)
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    return recipient


@app.put("/recipients/{recipient_id}", response_model=schemas.RecipientRead)
def update_recipient(recipient_id: int, payload: schemas.RecipientUpdate, db: Session = Depends(get_db_session)):
    recipient = crud.update_recipient(db, recipient_id, payload)
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    return recipient


@app.delete("/recipients/by-email/{email}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipient(email: str, db: Session = Depends(get_db_session)):
    ok = crud.delete_recipient_by_email(db, email)
    if not ok:
        raise HTTPException(status_code=404, detail="Recipient not found")
    return None


@app.post("/articles", response_model=schemas.ArticleRead, status_code=status.HTTP_201_CREATED)
def create_article(payload: schemas.ArticleCreate, db: Session = Depends(get_db_session)):
    existing = crud.get_article_by_url(db, payload.url)
    if existing:
        raise HTTPException(status_code=400, detail="Article with this URL already exists")
    return crud.create_article(db, payload)


@app.get("/articles", response_model=list[schemas.ArticleRead])
def get_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    return crud.list_articles(db, skip=skip, limit=limit)


@app.get("/articles/{article_id}", response_model=schemas.ArticleRead)
def get_article(article_id: int, db: Session = Depends(get_db_session)):
    article = crud.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@app.get("/articles/by-url/{url:path}", response_model=schemas.ArticleRead)
def get_article_by_url(url: str, db: Session = Depends(get_db_session)):
    article = crud.get_article_by_url(db, url)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@app.put("/articles/{article_id}", response_model=schemas.ArticleRead)
def update_article(article_id: int, payload: schemas.ArticleUpdate, db: Session = Depends(get_db_session)):
    article = crud.update_article(db, article_id, payload)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@app.delete("/articles/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(article_id: int, db: Session = Depends(get_db_session)):
    ok = crud.delete_article(db, article_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Article not found")
    return None


@app.post("/email-content", response_model=schemas.EmailContentRead, status_code=status.HTTP_201_CREATED)
def create_email_content(payload: schemas.EmailContentCreate, db: Session = Depends(get_db_session)):
    return crud.create_email_content(db, payload)


@app.get("/email-content", response_model=list[schemas.EmailContentRead])
def get_email_content_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    return crud.list_email_content(db, skip=skip, limit=limit)


@app.get("/email-content/latest", response_model=schemas.EmailContentRead)
def get_latest_email_content(db: Session = Depends(get_db_session)):
    email_content = crud.get_latest_email_content(db)
    if not email_content:
        raise HTTPException(status_code=404, detail="No email content found")
    return email_content


@app.get("/email-content/{email_content_id}", response_model=schemas.EmailContentRead)
def get_email_content(email_content_id: int, db: Session = Depends(get_db_session)):
    email_content = crud.get_email_content_by_id(db, email_content_id)
    if not email_content:
        raise HTTPException(status_code=404, detail="Email content not found")
    return email_content


@app.put("/email-content/{email_content_id}", response_model=schemas.EmailContentRead)
def update_email_content(email_content_id: int, payload: schemas.EmailContentUpdate, db: Session = Depends(get_db_session)):
    email_content = crud.update_email_content(db, email_content_id, payload)
    if not email_content:
        raise HTTPException(status_code=404, detail="Email content not found")
    return email_content


@app.delete("/email-content/{email_content_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_email_content(email_content_id: int, db: Session = Depends(get_db_session)):
    ok = crud.delete_email_content(db, email_content_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Email content not found")
    return None