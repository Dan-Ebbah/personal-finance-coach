from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import date

DB_URL = "sqlite:///finance.db"

engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    transaction_date = Column(Date, index=True)
    transaction= Column(String)
    name = Column(String)
    memo = Column(String)
    amount = Column(Float)

def init_db():
    Base.metadata.create_all(bind=engine)