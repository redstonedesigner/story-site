from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from models import User, Category


class Story(Base):
	__tablename__ = "stories"
	id = Column(Integer, primary_key=True, autoincrement=True)
	author = Column(String(32), ForeignKey('users.id'), nullable=False)
	title = Column(String(255), nullable=False)
	description = Column(String(255), nullable=False)
	url_slug = Column(String(32), nullable=False, unique=True)

	def __init__(
			self,
			author: User = None,
			title: str = None,
			description: str = None,
			categories: list[Category] = None,
			url_slug: str = None):
		self.author = author.id
		self.description = description
		self.title = title
		self.categories = list()
		for i in categories:
			self.categories.append(i.id)
		self.categories = str(self.categories)
		self.url_slug = url_slug

	def __repr__(self):
		return '<Story %r>' % self.title
