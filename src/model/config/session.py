from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = r'sqlite:///gurschedule.db'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)