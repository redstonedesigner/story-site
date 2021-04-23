from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from models.User import User


class Story(Base):
    __tablename__ = "stories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(String(32), ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)

    def __init__(self, author: User = None, title=None, description=None):
        self.author = author.id
        self.description = description
        self.title = title

    def __repr__(self):
        return '<User %r>' % self.username
