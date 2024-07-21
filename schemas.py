from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    display_name: str

class BlogCreate(BaseModel):
    title: str
    content: str

class SubscriptionCreate(BaseModel):
    plan: str
