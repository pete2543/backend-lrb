from pydantic import BaseModel, Field, validator
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
    age: Optional[int] = None
    birthday: Optional[date] = None
    birth_day: Optional[int] = Field(None, ge=1, le=31)
    birth_month: Optional[int] = Field(None, ge=1, le=12)
    birth_year: Optional[int] = Field(None, ge=1900, le=datetime.now().year)
    profession: Optional[str] = None
    status: Optional[StatusEnum] = Field(default="wait")
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

    # ✅ เพิ่มฟิลด์ใหม่ที่ใช้สร้าง address และส่งลง PDF
    house_number: Optional[str] = None
    village: Optional[str] = None
    alley: Optional[str] = None
    road: Optional[str] = None
    subdistrict: Optional[str] = None
    blood_group: Optional[str] = None
    generation: Optional[int] = None
