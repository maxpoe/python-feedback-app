from fastapi import FastAPI, Depends, HTTPException
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine
from .db_dependency import get_db
from .models import Base
from . import crud

# Create tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow requests from all origins (can be restricted later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (you can specify specific origins here)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Sample route to test the setup
@app.get("/")
def read_root():
    return {"message": "Welcome to the Feedback Analysis App"}

# Additional route example for submitting feedback
@app.post("/submit-feedback/")
def submit_feedback(feedback_text: str, db: Session = Depends(get_db)):
    feedback = crud.create_feedback(db=db, feedback_text=feedback_text)
    return {"message": "Feedback submitted successfully", "feedback": feedback.feedback_text, "sentiment": feedback.sentiment}


# Route to create feedback
@app.post("/feedback/")
def create_feedback(feedback_text: str, db: Session = Depends(get_db)):
    feedback = crud.create_feedback(db=db, feedback_text=feedback_text)
    return feedback


# Route to get all feedback with pagination
@app.get("/feedback/")
def read_feedback(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_feedback(db=db, skip=skip, limit=limit)

# Route to get a single feedback entry by ID
@app.get("/feedback/{feedback_id}")
def read_feedback_by_id(feedback_id: int, db: Session = Depends(get_db)):
    feedback = crud.get_feedback_by_id(db=db, feedback_id=feedback_id)
    if feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback

# Route to update feedback
@app.put("/feedback/{feedback_id}")
def update_feedback(feedback_id: int, feedback_text: str, db: Session = Depends(get_db)):
    feedback = crud.update_feedback(db=db, feedback_id=feedback_id, feedback_text=feedback_text)
    if feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback

# Route to delete feedback
@app.delete("/feedback/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = crud.delete_feedback(db=db, feedback_id=feedback_id)
    if feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return {"message": "Feedback deleted"}
