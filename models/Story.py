from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from database import Base
from .User import User
from .StoryCategory import StoryCategory
from .Category import Category
import datetime
from shortuuid import uuid


class Story(Base):
	__tablename__ = "stories"
	id = Column(Integer, primary_key=True, autoincrement=True)
	author_id = Column(String(32), ForeignKey('users.id', ondelete="CASCADE", name="author_id"), nullable=False)
	title = Column(String(255), nullable=False)
	description = Column(String(255), nullable=False)
	url_slug = Column(String(32), nullable=False, unique=True, default=uuid)
	multiple_chapters = Column(Boolean, nullable=False)
	created_at = Column(DateTime, unique=False, default=datetime.datetime.utcnow)
	modified_at = Column(DateTime, unique=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

	chapters = relationship(
		"Chapter",
		back_populates="story",
		cascade="all, delete",
		passive_deletes=True,
		order_by="Chapter.created_at"
	)

	author = relationship(
		"User",
		back_populates="stories"
	)

	def __init__(
			self,
			author: User = None,
			title: str = None,
			description: str = None,
			multiple_chapters: bool = None):
		self.author = author.id
		self.description = description
		self.title = title
		self.multiple_chapters = multiple_chapters

	def __repr__(self):
		return '<Story %r>' % self.title

	def get_category_relations(self):
		category_relations: list[StoryCategory] = StoryCategory.query.filter(StoryCategory.story_id == self.id).all()
		categories = []
		for i in category_relations:
			category: Category = i.get_category()
			data = {
				'slug': category.url_slug,
				'name': category.name
			}
			categories.append(data)
		return categories

	def get_author(self):
		u_id = self.author
		u: User = User.query.filter(User.id == u_id).first()
		return u
