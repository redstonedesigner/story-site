from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime
from shortuuid import uuid


class Chapter(Base):
    __tablename__ = 'story_chapters'

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    story_id = Column(Integer, ForeignKey('stories.id', ondelete="CASCADE", name="chapter_story_id"), unique=False)
    title = Column(String(255), unique=False, nullable=False)
    content = Column(Text, unique=False, nullable=False)
    url_slug = Column(String, unique=True, nullable=False, default=uuid)
    created_at = Column(DateTime, unique=False, default=datetime.datetime.utcnow)
    modified_at = Column(DateTime, unique=False, default=datetime.datetime.utcnow,
                         onupdate=datetime.datetime.utcnow)

    story = relationship(
        "Story",
        back_populates="chapters"
    )
    
    def __init__(self, story_id: int = None, title: str = None, content: str = None):
        self.story_id = story_id
        self.title = title
        self.content = content
