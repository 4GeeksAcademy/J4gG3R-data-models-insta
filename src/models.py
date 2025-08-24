from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    followers: Mapped[list["Followers"]] = relationship("Followers", foreign_keys="[Followers.followed_id]", back_populates="followed")
    followings: Mapped[list["Followers"]] = relationship("Followers", foreign_keys="[Followers.follower_id]", back_populates="follower")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            #"is_active": self.is_active
            # do not serialize the password, its a security breach
        }
    
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    img: Mapped[str] = mapped_column(nullable=False)
    likes: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="posts")


    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "img": self.img,
            "likes": self.likes,
            "user_id": self.user_id
            #"is_active": self.is_active
            # do not serialize the password, its a security breach
        }

class Comments(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

    post: Mapped["Post"] = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "post_id": self.post_id
            #"is_active": self.is_active
            # do not serialize the password, its a security breach
        }

class Followers(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    followed_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    follower_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    followed: Mapped["User"] = relationship("User", foreign_keys=[followed_id], back_populates="followers")
    follower: Mapped["User"] = relationship("User", foreign_keys=[follower_id], back_populates="followings")

    def serialize(self):
        return {
            "id": self.id,
            "followed_id": self.followed_id,
            "follower_id": self.follower_id,
            #"is_active": self.is_active
            # do not serialize the password, its a security breach
        }
    