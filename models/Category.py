from sqlalchemy import Column, Integer, String
from database import Base


class Category(Base):
	__tablename__ = "categories"
	id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
	name = Column(String(128), nullable=False, unique=True)
	description = Column(String(255), nullable=False)
	url_slug = Column(String(255), nullable=False, unique=True)
	content_warning = Column(Integer, default=0, nullable=False)

	def __init__(self, name=None, description=None, url_slug=None, content_warning=None):
		self.name = name
		self.description = description
		self.url_slug = url_slug
		self.content_warning = content_warning

	def __repr__(self):
		return '<User %r>' % self.username
