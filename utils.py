from database import db_session
from models import StoryCategory, Category
from datetime import datetime


def format_date(obj: datetime):
    return obj.strftime("%A, %d %B %Y")