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


@app.delete("/recipients/by-email/{email}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipient(email: str, db: Session = Depends(get_db_session)):
    ok = crud.delete_recipient_by_email(db, email)
    if not ok:
        raise HTTPException(status_code=404, detail="Recipient not found")
    return None