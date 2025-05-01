import datetime
from sqlalchemy.orm import Session
from app.models.subscribe import LRBSubscribe

def generate_order_number(db: Session) -> str:
    now = datetime.datetime.now()
    year = now.strftime("%y") 
    month = now.strftime("%m") 

    prefix = f"LRB{year}{month}"
    last_order = db.query(LRBSubscribe).filter(
        LRBSubscribe.order_number.startswith(prefix)
    ).order_by(LRBSubscribe.order_number.desc()).first()

    if last_order:
        last_number = int(last_order.order_number[-3:])  # ดึงตัวเลข 3 หลักท้ายสุด
        new_number = last_number + 1
    else:
        new_number = 1 

    order_number = f"{prefix}{new_number:03}"  # สร้างหมายเลขคำสั่งใหม่
    return order_number
