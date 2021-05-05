from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
from models import User, Category
import datetime


class Story(Base):
	__tablename__ = "stories"
	id = Column(Integer, primary_key=True, autoincrement=True)
	author = Column(String(32), ForeignKey('users.id', ondelete="CASCADE", name="author_id"), nullable=False)
	title = Column(String(255), nullable=False)
	description = Column(String(255), nullable=False)
	url_slug = Column(String(32), nullable=False, unique=True)
	multiple_chapters = Column(Boolean, nullable=False)
	created_at = Column(String(48), unique=False, default=datetime.datetime.utcnow())
	modified_at = Column(String(48), unique=False, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

	chapters = relationship(
		"Chapter",
		back_populates="story",
		cascade="all, delete",
		passive_deletes=True
	)

	def __init__(
			self,
			author: User = None,
			title: str = None,
			description: str = None,
			categories: list[Category] = None,
			url_slug: str = None,
			multiple_chapters: bool = None):
		self.author = author.id
		self.description = description
		self.title = title
		self.categories = list()
		for i in categories:
			self.categories.append(i.id)
		self.categories = str(self.categories)
		self.url_slug = url_slug
		self.multiple_chapters = multiple_chapters

	def __repr__(self):
		return '<Story %r>' % self.title
