from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Visitor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Listing(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    external_id: Optional[str] = None
    title: Optional[str] = None
    city: Optional[str] = None
    area_m2: Optional[float] = None
    rooms: Optional[int] = None
    price_tnd: Optional[float] = None
    raw: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Lead(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    listing_id: Optional[int] = Field(default=None, index=True)
    visitor_id: Optional[int] = Field(default=None, index=True)
    intent: Optional[str] = None
    raw_message: Optional[str] = None
    status: str = Field(default="new")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ConversationMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lead_id: Optional[int] = Field(default=None, index=True)
    role: str = Field(default="user")
    content: str = Field(default="")
    created_at: datetime = Field(default_factory=datetime.utcnow)
