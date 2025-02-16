from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings
"""
Connect to sqlite3 database
"""
SQLALCHEMY_DATABASE_URL = settings.database_url
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

print(f"SQLALCHEMY_DATABASE_URL: {settings.database_url}")

"""
HOW TO CONNECT TO SOME POPULAR PRODUCTION DATABASE:
Connect to PostgreSQL database
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:test1234!@localhost/TodoApplicationDatabase'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
"""

"""
Connect to MySQL database
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:algonquin@127.0.0.1:3306/todoapplicationdatabase'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
"""
