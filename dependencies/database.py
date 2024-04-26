from core.config import settings
from models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database_url = f"mssql+pymssql://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"
engine = create_engine(url=database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("\n \033[1;32m ✔️  Azure Database Connection stablished. 🔌  \n")

def get_db():
    db = SessionLocal()
    try:
        # yield is a keyword used in a function like a return statement but it returns a generator. 
        # A generator is an iterator, a kind of iterable you can only iterate over once.
        # In this case, the yield db statement is used within a generator function get_db(). 
        # This function is designed to provide a database session (db) to the caller and ensure that the session is properly closed after its use, even if an error occurs. 
        # This pattern is particularly useful in web applications where you want to ensure that resources like database connections are properly managed and released after use.
        yield db
    finally:
        db.close()
