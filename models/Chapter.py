from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime


class Chapter(Base):
    __tablename__ = 'story_chapters'

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    story_id = Column(Integer, ForeignKey('stories.id', ondelete="CASCADE", name="chapter_story_id"), unique=False)
    title = Column(String(255), unique=False, nullable=False)
    content = Column(Text, unique=False, nullable=False)
    created_at = Column(String(48), unique=False, default=datetime.datetime.utcnow())
    modified_at = Column(String(48), unique=False, default=datetime.datetime.utcnow(),
                         onupdate=datetime.datetime.utcnow())

    story = relationship(
        "Story",
        back_populates="chapters"
    )