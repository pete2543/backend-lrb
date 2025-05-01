from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime, date
from enum import Enum

class StatusEnum(str, Enum):
    wait = "wait"
    submit = "submit"
    approved = "approved"
    reject = "reject"

class SubscribeBase(BaseModel):
    order_number: Optional[str] = None
    datestart: Optional[datetime] = None
    titel: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birthday: Optional[date] = None
    profession: Optional[str] = None
    status: Optional[StatusEnum] =  Field(default="wait")
    tel: Optional[str] = None
    address: Optional[str] = None
    province: Optional[str] = None
    district: Optional[str] = None
    city: Optional[str] = None
    postcode: Optional[str] = None
    disease: Optional[str] = None
    blood: Optional[str] = None
    batch_number: Optional[int] = None
    signature_path: Optional[str] = None
    document_path: Optional[str] = None
    
class SignatureUpdate(BaseModel):
    order_number: str
    signature_path: str