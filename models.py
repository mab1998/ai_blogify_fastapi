from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    uid: str
    email: str
    display_name: Optional[str]
    role: Optional[str]

class Blog(BaseModel):
    title: str
    content: str
    author_id: str
    created_at: Optional[str] = None

class Subscription(BaseModel):
    user_id: str
    plan: str
    start_date: str
    end_date: str
