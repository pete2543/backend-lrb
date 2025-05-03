from sqlalchemy import Column, Integer, String, Text, DateTime, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class LRBSubscribe(Base):
    __tablename__ = "LRB_Subscribe"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_number = Column(String(50), unique=True, nullable=False)
    datestart = Column(DateTime)
    titel = Column(String(10), nullable=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    age = Column(Integer, nullable=True)
    birthday = Column(Date)
    profession = Column(String(50), nullable=True)
    status = Column(String(50), nullable=True)
    tel = Column(Integer, nullable=True) 
    address = Column(Text, nullable=True)
    province = Column(String(50), nullable=True)
    district = Column(String(50), nullable=True)
    city = Column(String(50), nullable=True)
    postcode = Column(Integer, nullable=True)
    disease = Column(String(50), nullable=True)
    blood = Column(String(50), nullable=True)
    batch_number = Column(Integer, nullable=True)
    signature_path = Column(String(255), nullable=True)
    document_path = Column(String(255), nullable=True)


