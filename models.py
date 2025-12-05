import os
from dotenv import load_dotenv
from sqlalchemy import Column, String, Integer, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    id = Column(String, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    last_updated = Column(DateTime)

class PriceHistory(Base):
    __tablename__ = 'price_history'
    rowid = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(String, index=True)
    price = Column(Integer)
    timestamp = Column(DateTime)

def get_engine():
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        return create_engine('sqlite:///shop.db')
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    return create_engine(db_url)

def get_session():
    engine = get_engine()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()