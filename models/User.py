from sqlalchemy import Column, Integer, String
from database import Base
import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Integer, default=0, nullable=False)
    created_at = Column(String(48), unique=False, default=datetime.datetime.utcnow())
    modified_at = Column(String(48), unique=False, default=datetime.datetime.utcnow(),
                         onupdate=datetime.datetime.utcnow())

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username
