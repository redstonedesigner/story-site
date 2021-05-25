from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime

from database import Base
from models import User


class Follower(Base):
    __tablename__ = 'followers'
    _id = Column(Integer, primary_key=True, autoincrement=True)
    follower_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    following_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    since = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, follower: User = None, following: User = None):
        self.following_id = follower.id
        self.following_id = following.id

    def get_following(self):
        return User.query.filter(User.id == self.following_id).first()

    def get_follower(self):
        return User.query.filter(User.id == self.follower_id).first()