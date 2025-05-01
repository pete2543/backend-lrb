from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import get_db  
from app.models.districts import LRB_Distrcts
from app.schemas.districts import DistrictOut

router = APIRouter(
    prefix="/api/v1/districts",
    tags=["districts"]
)


@router.get("/provinces")
def get_provinces(db: Session = Depends(get_db)):
    provinces = db.query(
        LRB_Distrcts.province_code,
        LRB_Distrcts.province
    ).distinct().order_by(LRB_Distrcts.province).all()
    
    return [{"code": p.province_code, "province": p.province} for p in provinces]

@router.get("/amphoes")
def get_amphoes(province_code: str, db: Session = Depends(get_db)):
    amphoes = db.query(
        LRB_Distrcts.amphoe_code,
        LRB_Distrcts.amphoe
    ).filter(
        LRB_Distrcts.province_code == province_code
    ).distinct().order_by(LRB_Distrcts.amphoe).all()
    
    return [{"code": a.amphoe_code, "amphoe": a.amphoe} for a in amphoes]

@router.get("/subdistricts")
def get_subdistricts(amphoe_code: str, db: Session = Depends(get_db)):
    subdistricts = db.query(
        LRB_Distrcts.district_code,
        LRB_Distrcts.district
    ).filter(
        LRB_Distrcts.amphoe_code == amphoe_code
    ).distinct().order_by(LRB_Distrcts.district).all()
    
    return [{"code": s.district_code, "district": s.district} for s in subdistricts]

@router.get("/zipcode")
def get_zipcode(district_code: str, db: Session = Depends(get_db)):
    result = db.query(
        LRB_Distrcts.district_code,
        LRB_Distrcts.zipcode
    ).filter(
        LRB_Distrcts.district_code == district_code
    ).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="District not found")

    return {"code": result.district_code, "zipcode": result.zipcode}

@router.get("/detail/{district_id}", response_model=DistrictOut)
def get_district_by_id(district_id: int, db: Session = Depends(get_db)):
    district = db.query(LRB_Distrcts).filter(LRB_Distrcts.id == district_id).first()
    if district is None:
        raise HTTPException(status_code=404, detail="District not found")
    return district
