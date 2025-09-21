import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    salt = Column(String(255), nullable=False)
    failed_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    
    transactions = relationship("Transaction", back_populates="user")

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="transactions")

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False)
    is_default = Column(Integer, default=0)  # 1 for default categories, 0 for user-defined

# Database setup
DATABASE_URL = "sqlite:///tracker.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database and create default categories."""
    Base.metadata.create_all(bind=engine)
    
    # Add default categories if they don't exist
    session = SessionLocal()
    default_categories = ['Food', 'Rent', 'Transport', 'Entertainment', 'Utilities', 'Healthcare', 'Shopping', 'Other']
    
    for cat_name in default_categories:
        existing = session.query(Category).filter_by(name=cat_name, user_id=0, is_default=1).first()
        if not existing:
            category = Category(name=cat_name, user_id=0, is_default=1)
            session.add(category)
    
    session.commit()
    session.close()

def get_db_session():
    """Get a database session."""
    return SessionLocal()
