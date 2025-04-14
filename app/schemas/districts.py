from pydantic import BaseModel

class DistrictBase(BaseModel):
    district: str
    amphoe: str
    province: str
    zipcode: str
    district_code: str
    amphoe_code: str
    province_code: str

class DistrictOut(DistrictBase):
    id: int

    class Config:
        orm_mode = True
