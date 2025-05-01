from fastapi import APIRouter, Depends,UploadFile, File, Form,HTTPException
from sqlalchemy.orm import Session
from app.db.db import get_db  
from app.models.subscribe import LRBSubscribe
from app.schemas.subscribe import SubscribeBase,StatusEnum,SignatureUpdate
from app.services.genorder import generate_order_number
from datetime import datetime
import os
from uuid import uuid4
from app.services.s3_service import upload_file_to_s3
router = APIRouter(
    prefix="/api/v1/order",
    tags=["subscribe"]
)

@router.post("/subscribe")
def create_subscription(subscribe: SubscribeBase, db: Session = Depends(get_db)):
    order_number = generate_order_number(db)
    
    new_subscribe = LRBSubscribe(
        **subscribe.dict(exclude={"status"}, exclude_unset=True),
        status=subscribe.status or "wait",
        order_number=order_number,
        datestart=subscribe.datestart or datetime.now()
    )

    db.add(new_subscribe)
    db.commit()
    db.refresh(new_subscribe)

    return {
        "order_number": new_subscribe.order_number,
        "status": "success"
    }


@router.put("/subscribe/signature")
def update_signature(order_number: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    subscription = db.query(LRBSubscribe).filter(LRBSubscribe.order_number == order_number).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Order number not found")

    s3_url = upload_file_to_s3(file.file, f"{order_number}.png")
    if not s3_url:
        raise HTTPException(status_code=500, detail="Upload to S3 failed")

    subscription.signature_path = s3_url
    db.commit()
    db.refresh(subscription)

    return {
        "order_number": subscription.order_number,
        "signature_url": subscription.signature_path,
        "status": "upload successful"
    }
