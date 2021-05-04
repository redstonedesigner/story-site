from sqlalchemy import Column, Integer, ForeignKey
from database import Base


class StoryCategory(Base):
    __tablename__ = 'story_categories'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    story_id = Column(Integer, ForeignKey('stories.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    def __init__(self, story_id: int = None, category_id: int = None):
        self.story_id = story_id
        self.category_id = category_id

    def __repr__(self):
        return "<Story/Category Relation %s>" % self.id