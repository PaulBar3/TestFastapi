from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uvicorn
import os

from database import engine, get_db
from models import Base
from schemas import (
    User,
    UserCreate,
    UserUpdate,
    BlogPost,
    BlogPostCreate,
    BlogPostUpdate,
    SuccessResponse,
)
from crud import (
    get_user,
    get_users,
    create_user,
    update_user,
    delete_user,
    get_blog_post,
    get_blog_posts,
    create_blog_post,
    update_blog_post,
    delete_blog_post,
    get_user_by_username,
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TestFastAPI Application",
    description="A sample FastAPI web application with user management and blog functionality",
    version="1.0.0",
)


@app.get("/")
def read_root():
    return {"message": "Welcome to TestFastAPI Application!", "status": "running"}


# User endpoints
@app.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/", response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)


@app.put("/users/{user_id}", response_model=User)
def update_existing_user(
    user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)
):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return update_user(db=db, user_id=user_id, user_update=user_update)


@app.delete("/users/{user_id}", response_model=SuccessResponse)
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "message": "User deleted successfully"}


# Blog post endpoints
@app.get("/posts/", response_model=List[BlogPost])
def read_blog_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = get_blog_posts(db, skip=skip, limit=limit)
    return posts


@app.get("/posts/{post_id}", response_model=BlogPost)
def read_blog_post(post_id: int, db: Session = Depends(get_db)):
    post = get_blog_post(db, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.post("/posts/", response_model=BlogPost)
def create_new_blog_post(post: BlogPostCreate, db: Session = Depends(get_db)):
    # Verify that the author exists
    author = get_user(db, post.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return create_blog_post(db=db, post=post)


@app.put("/posts/{post_id}", response_model=BlogPost)
def update_existing_blog_post(
    post_id: int, post_update: BlogPostUpdate, db: Session = Depends(get_db)
):
    post = get_blog_post(db, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return update_blog_post(db=db, post_id=post_id, post_update=post_update)


@app.delete("/posts/{post_id}", response_model=SuccessResponse)
def delete_existing_blog_post(post_id: int, db: Session = Depends(get_db)):
    success = delete_blog_post(db, post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"success": True, "message": "Post deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
