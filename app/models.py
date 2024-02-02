# from sqlalchemy import column,Integer,String,Boolean,PrimaryKeyConstraint
# from sqlalchemy.sql.expression import null
# from .database import Base

# class post(Base):
#    class Post(Base):
#     __tablename__ = "posts"

#     id = column(Integer ,primary_key = True, nullable=False)
#     title = column(String, nullable=False)
#     content = column(String, nullable=False)
#     published = column(Boolean, server_default='TRUE', nullable=False)
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .database import Base
Base = declarative_base()

                  #here this model is sql alchemy model used for schema of table

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    owner = relationship("User")       # an relation between the model user it automatically retrieves the posts based on the ownerid which is actually a great part of sqlalchemy

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    phone_number = Column(String)
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id", ondelete="CASCADE"),primary_key=True)
