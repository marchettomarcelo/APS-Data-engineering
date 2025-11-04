from datetime import datetime

from pydantic import BaseModel, EmailStr


class RecipientBase(BaseModel):
    name: str
    email: EmailStr


class RecipientCreate(RecipientBase):
    pass


class RecipientRead(RecipientBase):
    id: int

    class Config:
        from_attributes = True


class RecipientUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class ArticleBase(BaseModel):
    url: str
    title: str | None = None
    content: str | None = None


class ArticleCreate(ArticleBase):
    pass


class ArticleRead(ArticleBase):
    id: int

    class Config:
        from_attributes = True


class ArticleUpdate(BaseModel):
    url: str | None = None
    title: str | None = None
    content: str | None = None


class EmailContentBase(BaseModel):
    subject: str | None = None
    content: str | None = None


class EmailContentCreate(EmailContentBase):
    pass


class EmailContentRead(EmailContentBase):
    id: int
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class EmailContentUpdate(BaseModel):
    subject: str | None = None
    content: str | None = None

