from sqlalchemy import Column, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    education = Column(Text, nullable=True, default=None)
    location = Column(Text, nullable=True, default=None)
    skills = Column(Text, nullable=True, default=None)
    notes = Column(Text, nullable=True, default=None)

    user = relationship(
        "User",
        back_populates="profile"
    )

    def __init__(
            self,
            id: int = None,
            education: str = None,
            location: str = None,
            skills: str = None,
            notes: str = None
    ):
        self.id = id
        self.education = education
        self.location = location
        self.skills = skills
        self.notes = notes
