from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, unique=False, default=datetime.datetime.utcnow())
    modified_at = Column(DateTime, unique=False, default=datetime.datetime.utcnow(),
                         onupdate=datetime.datetime.utcnow())

    stories = relationship(
        "Story",
        back_populates="author",
        cascade="all, delete",
        passive_deletes=True,
        order_by="Story.created_at"
    )

    profile = relationship(
        "UserProfile",
        back_populates="user",
        cascade="all, delete",
    )

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    def get_all_followers(self):
        from models import Follower
        raw_followers = Follower.query.filter(self.id == Follower.following_id).all()
        followers = []
        for i in raw_followers:
            user = User.query.filter(User.id == Follower.follower_id).first()
            followers.append(user)
        return followers

    def get_all_following(self):
        from models import Follower
        raw_following = Follower.query.filter(self.id == Follower.follower_id).all()
        following = []
        for i in raw_following:
            user = User.query.filter(User.id == i.following_id).first()
            following.append(user)
        return following

    def get_follower_count(self):
        return len(self.get_all_followers())

    def get_following_count(self):
        return len(self.get_all_following())
