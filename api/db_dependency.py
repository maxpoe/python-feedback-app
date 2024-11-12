from .database import SessionLocal
from sqlalchemy.orm import Session

# Dependency for managing session lifecycle
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
