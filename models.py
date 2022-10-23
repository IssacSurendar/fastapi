from email.policy import default
from enum import unique
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Post(base):

    __tablename__ = "t_posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(16), nullable=False)
    content = Column(String(16), nullable=False)
    published = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("t_users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class User(base):

    __tablename__ = "t_users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Vote(base):
    
    __tablename__ = "t_votes"

    user_id = Column(Integer, ForeignKey("t_users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey("t_posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)
