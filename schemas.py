from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Blog post schemas
class BlogPostBase(BaseModel):
    title: str
    content: str


class BlogPostCreate(BlogPostBase):
    author_id: int


class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class BlogPost(BlogPostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime

    author: User

    class Config:
        from_attributes = True


# Response schemas
class SuccessResponse(BaseModel):
    success: bool
    message: str


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
