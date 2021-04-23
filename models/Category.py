from sqlalchemy import Column, Integer, String
from database import Base


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(128), nullable=False, unique=True)
    description = Column(String(255), nullable=False)
    url_slug = Column(String(255), nullable=False, unique=True)

    def __init__(self, name=None, short_name=None):
        self.name = name
        self.short_name = short_name

    def __repr__(self):
        return '<User %r>' % self.username
