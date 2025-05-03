from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from datetime import datetime
import os

# ลงทะเบียนฟอนต์ไทย
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
FONT_PATH = os.path.join("app", "static", "font", "THSarabunNew.ttf")
pdfmetrics.registerFont(TTFont('THSarabun', FONT_PATH))

def create_thai_form(output_pdf: str, data: dict):
    c = canvas.Canvas(output_pdf, pagesize=A4)
    width, height = A4
    c.setFont("THSarabun", 16)
    
    y = height - 50
    c.drawString(480, y, "เลขที่:")
    c.drawString(508, y, data.get('order_number', ''))  # Order number aligned right after label
    
    y -= 30
    c.drawCentredString(width / 2, y, "ใบสมัครสมาชิกชมรมศิษย์เก่าโรงเรียนลาดตะเคียนราษฏร์บำรุง")
    
    y -= 55
    c.drawString(55, y, "เรียน ประธานชมรมศิษย์เก่าโรงเรียนลาดตะเคียนราษฏร์บํารุง")
    c.drawString(450, y + 15, f"วันที่: {datetime.now().strftime('%d/%m/%Y')}")

    # Form fields
    y = height - 180
    c.setFillColor(colors.black)
    c.drawString(50, y, "1. ข้าพเจ้า ชื่อ .............................................. นามสกุล ................................................ อายุ .............. ปี")
    c.setFillColor(colors.blue)
    c.drawString(150, y + 2, data.get('first_name', ''))
    c.drawString(300, y + 2, data.get('last_name', ''))
    c.drawString(440, y + 2, str(data.get('age', '')))
    y -= 40

    c.setFillColor(colors.black)
    c.drawString(50, y, "เกิดวันที่ .............. เดือน ............................ พ.ศ. .............. ที่อยู่บ้านเลขที่ ............... หมู่ที่ ........ ตรอก/ซอย .................................")
    c.setFillColor(colors.blue)
    c.drawString(110, y + 2, data.get('birth_day', ''))
    c.drawString(175, y + 2, data.get('birth_month', ''))
    c.drawString(255, y + 2, data.get('birth_year', ''))
    c.drawString(358, y + 2, data.get('house_number', ''))
    c.drawString(428, y + 2, data.get('village', ''))
    c.drawString(510, y + 2, data.get('alley', ''))
    y -= 40

    c.setFillColor(colors.black)
    c.drawString(50, y, "ถนน............................. ตําบล............................ อําเภอ............................ จังหวัด ....................................................")
    c.setFillColor(colors.blue)
    c.drawString(85, y + 2, data.get('road', ''))
    c.drawString(180, y + 2, data.get('subdistrict', ''))
    c.drawString(300, y + 2, data.get('district', ''))
    c.drawString(420, y + 2, data.get('province', ''))
    y -= 40

    c.setFillColor(colors.black)
    c.drawString(50, y, "รหัสไปรษณีย์.......................... หมายเลขโทรศัพท์ ...............................................")
    c.setFillColor(colors.blue)
    c.drawString(130, y + 2, data.get('zipcode', ''))
    c.drawString(260, y + 2, data.get('tel', ''))
    y -= 40

    c.setFillColor(colors.black)
    c.drawString(50, y, "2. ประกอบอาชีพ ........................................................................................................................................")
    c.setFillColor(colors.blue)
    c.drawString(145, y + 2, data.get('profession', ''))
    y -= 40

    c.setFillColor(colors.black)
    c.drawString(50, y, "3. โรคประจําตัว.......................................................................... กรุ๊ปเลือด.................................................")
    c.setFillColor(colors.blue)
    c.drawString(125, y + 2, data.get('disease', ''))
    c.drawString(470, y + 2, data.get('blood_group', ''))
    y -= 40

    c.setFillColor(colors.black)
    c.drawString(50, y, "4. ศิษย์เก่าโรงเรียนลาดตะเคียนราษฏร์บํารุง รุ่นที่...............................")
    c.setFillColor(colors.blue)
    c.drawString(286, y + 2, str(data.get('generation', '')))
    y -= 60

    # Consent section
    c.setFillColor(colors.black)
    c.drawString(70, y, "ข้าพเจ้า.................................................................................. พร้อมปฏิบัติตามระเบียบข้อบังคับของชมรมศิษย์เก่าโรงเรียน")
    c.setFillColor(colors.blue)
    c.drawString(130, y + 2, data.get('consent_name', ''))
    y -= 25

    c.setFillColor(colors.black)
    c.drawString(50, y, "ลาดตะเคียนราษฏร์บํารุงทุกประการ ให้ความร่วมมือในการพัฒนาการจัดการศึกษาและร่วมกิจกรรมของโรงเรียนตามที่")
    y -= 25
    c.drawString(50, y, "ได้รับการประสานจากชมรมฯ")
    y -= 60

    # Signature section
    signature_path = data.get("signature_path")
    if os.path.exists(signature_path):
        signature_width = 100
        signature_height = 30
        signature_x = width - 210
        signature_y = y
        c.drawImage(signature_path, signature_x, signature_y, width=signature_width, height=signature_height, mask='auto')

    c.setFillColor(colors.black)
    c.drawRightString(width - 50, y, "ลงชื่อ..............................................ผู้สมัคร")
    y -= 25
    c.drawRightString(width - 130, y, f"({data.get('consent_name', '')})")
    y -= 25
    c.drawRightString(width - 50, y, "ลงชื่อ.................................................ผู้รับรอง")
    y -= 25
    c.drawRightString(width - 96, y, "(นายสุพจน์ ห่านทองคำ)")
    y -= 25
    c.drawRightString(width - 50, y, "ประธานชมรมศิษย์เก่าโรงเรียนลาดตะเคียนราษฏร์บํารุง")

    c.save()
    return output_pdf