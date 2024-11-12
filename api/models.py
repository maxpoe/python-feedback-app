from sqlalchemy import Column, String, Integer, DateTime
from .database import Base
from datetime import datetime

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    feedback_text = Column(String, nullable=False)
    sentiment = Column(String)
    keywords = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
