from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.settings import settings



engine = create_engine(f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}")
session_local = sessionmaker(autocommit=False, autoflush=True, bind=engine)
base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()