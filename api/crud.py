# crud.py
from sqlalchemy.orm import Session
from .models import Feedback
from datetime import datetime
from openai import OpenAI
import os

# Load OpenAI API key from environment
openaiClient = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
)

def analyze_sentiment(feedback_text: str) -> str:
    # Call OpenAI API to get sentiment analysis
    response = openaiClient.chat.completions.create(
       messages= [
           {
            "role": "user",
            "content": "Analyze the sentiment of this text: \"{feedback_text}\". Respond with either Positive, Neutral, or Negative.",
        }
       ],
        model="gpt-3.5-turbo",
    )
    
    sentiment = response.choices[0].message.content
    return sentiment

# Create feedback entry
def create_feedback(db: Session, feedback_text: str):
    sentiment = analyze_sentiment(feedback_text) 
    feedback = Feedback(feedback_text=feedback_text, sentiment=sentiment, timestamp=datetime.utcnow())
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback

# Read all feedback entries
def get_feedback(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Feedback).offset(skip).limit(limit).all()

# Read single feedback by ID
def get_feedback_by_id(db: Session, feedback_id: int):
    return db.query(Feedback).filter(Feedback.id == feedback_id).first()

# Update feedback by ID
def update_feedback(db: Session, feedback_id: int, feedback_text: str):
    db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if db_feedback:
        new_sentiment = analyze_sentiment(feedback_text) 
        db_feedback.feedback_text = feedback_text
        db_feedback.sentiment = new_sentiment
        db.commit()
        db.refresh(db_feedback)
    return db_feedback

# Delete feedback by ID
def delete_feedback(db: Session, feedback_id: int):
    db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if db_feedback:
        db.delete(db_feedback)
        db.commit()
        return True
    return None