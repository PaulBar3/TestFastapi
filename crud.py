from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import User, BlogPost
from schemas import UserCreate, UserUpdate, BlogPostCreate, BlogPostUpdate


# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    fake_hashed_password = (
        user.password + "notreallyhashed"
    )  # In real app, use proper hashing
    db_user = User(username=user.username, email=user.email, full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        for field, value in user_update.model_dump(exclude_unset=True).items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


# BlogPost CRUD operations
def get_blog_post(db: Session, post_id: int):
    return db.query(BlogPost).filter(BlogPost.id == post_id).first()


def get_blog_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(BlogPost).offset(skip).limit(limit).all()


def get_blog_posts_by_user(db: Session, user_id: int):
    return db.query(BlogPost).filter(BlogPost.author_id == user_id).all()


def create_blog_post(db: Session, post: BlogPostCreate):
    db_post = BlogPost(title=post.title, content=post.content, author_id=post.author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_blog_post(db: Session, post_id: int, post_update: BlogPostUpdate):
    db_post = get_blog_post(db, post_id)
    if db_post:
        for field, value in post_update.model_dump(exclude_unset=True).items():
            setattr(db_post, field, value)
        db.commit()
        db.refresh(db_post)
    return db_post


def delete_blog_post(db: Session, post_id: int):
    db_post = get_blog_post(db, post_id)
    if db_post:
        db.delete(db_post)
        db.commit()
        return True
    return False
