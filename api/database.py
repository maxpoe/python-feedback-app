from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


        
# Replace these with your actual PostgreSQL credentials
DATABASE_URL = "postgresql://feedbackuser:feedback@localhost/feedback_db"

# Set up the database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class to define models
Base = declarative_base()



