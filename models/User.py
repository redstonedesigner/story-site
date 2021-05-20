from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, unique=False, default=datetime.datetime.utcnow())
    modified_at = Column(DateTime, unique=False, default=datetime.datetime.utcnow(),
                         onupdate=datetime.datetime.utcnow())

    stories = relationship(
        "Story",
        back_populates="author",
        cascade="all, delete",
        passive_deletes=True,
        order_by="Story.created_at"
    )

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username
