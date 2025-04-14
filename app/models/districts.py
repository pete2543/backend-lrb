from sqlalchemy import Column, Integer ,VARCHAR
from sqlalchemy.orm import declarative_base
Base = declarative_base()

class LRB_Distrcts(Base) :
    __tablename__ = "LRB_Districts"
    id = Column(Integer,primary_key=True,autoincrement=True)
    district = Column(VARCHAR(100),unique=True, nullable=False)
    amphoe = Column(VARCHAR(100),unique=True)
    province= Column(VARCHAR(100),unique=True)
    zipcode = Column(VARCHAR(100),unique=True)
    district_code = Column(VARCHAR(100),unique=True)
    amphoe_code = Column(VARCHAR(100),unique=True)
    province_code= Column(VARCHAR(100),unique=True)
