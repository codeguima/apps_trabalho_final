#db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_USER = 'positivo'
DB_PASS = 'root'
DB_HOST = 'db'
DB_NAME = 'sistemademensagem'

DATABASE_URL = f'mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
