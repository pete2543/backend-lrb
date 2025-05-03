
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.models.subscribe import LRBSubscribe
from app.schemas.subscribe import SubscribeBase
from app.services.genorder import generate_order_number
from datetime import datetime
import os,re,requests,logging
import tempfile
from app.services.s3_service import upload_file_to_s3, upload_pdf_to_s3
from app.services.pdf_generator import create_thai_form

router = APIRouter(
    prefix="/api/v1/order",
    tags=["subscribe"]
)

def parse_birthday(day: str, month: str, year: str) -> datetime:
    try:
        return datetime.strptime(f"{day}-{month}-{year}", "%d-%m-%Y")
    except (ValueError, TypeError):
        return None

def ensure_string(value):
    return str(value) if value is not None else ""

def extract_address_parts(address: str):
    pattern = r"(?P<house_number>.*?) หมู่ (?P<village>.*?) ซอย (?P<alley>.*?) ถนน (?P<road>.*)"
    match = re.match(pattern, address)
    if match:
        return match.groupdict()
    return {
        "house_number": "",
        "village": "",
        "alley": "",
        "road": ""
    }

@router.post("/subscribe")
def create_subscription(subscribe: SubscribeBase, db: Session = Depends(get_db)):
    order_number = str(generate_order_number(db))

    postcode = int(subscribe.postcode) if subscribe.postcode else 0
    generation = int(subscribe.generation) if subscribe.generation else 1

    new_subscribe = LRBSubscribe(
        titel=subscribe.titel,
        first_name=subscribe.first_name,
        last_name=subscribe.last_name,
        age=subscribe.age,
        birthday=parse_birthday(subscribe.birth_day, subscribe.birth_month, subscribe.birth_year),
        profession=subscribe.profession,
        status=subscribe.status or "wait",
        tel=subscribe.tel,
        address=f"{subscribe.house_number} หมู่ {subscribe.village} ซอย {subscribe.alley} ถนน {subscribe.road}",
        province=subscribe.province,
        district=subscribe.subdistrict,
        city=subscribe.district,
        postcode=postcode,
        disease=subscribe.disease,
        blood=subscribe.blood_group,
        batch_number=generation,
        order_number=order_number,
        datestart=subscribe.datestart or datetime.now()
    )

    db.add(new_subscribe)
    db.commit()
    db.refresh(new_subscribe)

    return {
        "order_number": order_number,
        "status": "success",
        "message": "Subscription created successfully"
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
        "status": "signature uploaded"
    }
@router.post("/subscribe/generate-pdf")
def generate_pdf(order_number: str = Query(...), db: Session = Depends(get_db)):
    subscription = db.query(LRBSubscribe).filter(LRBSubscribe.order_number == order_number).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Order not found")

    signature_path = None
    pdf_path = None

    try:
        address_parts = extract_address_parts(subscription.address)

        # ดาวน์โหลดลายเซ็น
        if subscription.signature_path:
            try:
                response = requests.get(subscription.signature_path, timeout=10)
                response.raise_for_status()

                if not response.content:
                    raise HTTPException(status_code=500, detail="Signature file is empty.")

                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as sig_file:
                    sig_file.write(response.content)
                    signature_path = sig_file.name
                    logging.info(f"Signature saved to temp file: {signature_path}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to download signature: {str(e)}")

        form_data = {
            "order_number": subscription.order_number,
            "first_name": ensure_string(subscription.first_name),
            "last_name": ensure_string(subscription.last_name),
            "age": ensure_string(subscription.age),
            "birth_day": ensure_string(subscription.birthday.day if subscription.birthday else ""),
            "birth_month": ensure_string(subscription.birthday.month if subscription.birthday else ""),
            "birth_year": ensure_string(subscription.birthday.year if subscription.birthday else ""),
            "house_number": ensure_string(address_parts["house_number"]),
            "village": ensure_string(address_parts["village"]),
            "alley": ensure_string(address_parts["alley"]),
            "road": ensure_string(address_parts["road"]),
            "subdistrict": subscription.district,
            "district": subscription.city,
            "province": subscription.province,
            "zipcode": ensure_string(subscription.postcode),
            "tel": ensure_string(subscription.tel),
            "profession": ensure_string(subscription.profession),
            "disease": ensure_string(subscription.disease),
            "blood_group": ensure_string(subscription.blood),
            "generation": ensure_string(subscription.batch_number),
            "consent_name": f"{ensure_string(subscription.first_name)} {ensure_string(subscription.last_name)}",
            "signature_path": signature_path
        }

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdf_path = tmp.name

        create_thai_form(pdf_path, form_data)

        pdf_filename = f"{order_number}.pdf"
        with open(pdf_path, "rb") as pdf_file:
            pdf_s3_url = upload_pdf_to_s3(pdf_file, pdf_filename)

        if not pdf_s3_url:
            raise HTTPException(status_code=500, detail="Failed to upload PDF to S3")

        subscription.document_path = pdf_s3_url
        subscription.document_name = pdf_filename
        db.commit()
        db.refresh(subscription)

        return {
            "order_number": subscription.order_number,
            "pdf_url": pdf_s3_url,
            "pdf_filename": pdf_filename,
            "status": "PDF generated successfully"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

    finally:
        try:
            if pdf_path and os.path.exists(pdf_path):
                os.unlink(pdf_path)
            if signature_path and os.path.exists(signature_path):
                os.unlink(signature_path)
        except Exception as cleanup_error:
            logging.warning(f"Error during cleanup: {cleanup_error}")
            