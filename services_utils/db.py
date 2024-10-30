from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URI
from models import Base

engine = create_engine(DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# check if the database connection is working
try:
    conn = engine.connect()    
    print("Database connection successful.")
except Exception as e:
    print("Error occurred while connecting to the database.")
    raise e
