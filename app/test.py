from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime

# ลงทะเบียนฟอนต์ไทย
pdfmetrics.registerFont(TTFont('THSarabun', './font/THSarabunNew.ttf'))

def create_thai_form(output_pdf, data):
    c = canvas.Canvas(output_pdf, pagesize=A4)
    width, height = A4
    c.setFont("THSarabun", 16)

    c.drawCentredString(520, height - 50, "เลขที่...................")
    c.drawCentredString(width / 2, height - 80, "ใบสมัครสมาชิกชมรมศิษย์เก่าโรงเรียนลาดตะเคียนราษฏร์บำรุง")
    c.drawCentredString(145, height - 135, "เรียน ประธานชมรมศิษย์เก่าโรงเรียนลาดตะเคียนราษฏร์บํารุง")
    c.drawString(450, height - 120, f"วันที่: {datetime.now().strftime('%d/%m/%Y')}")

    y = height - 180

    c.drawString(50, y, "1. ข้าพเจ้า ชื่อ .............................................. นามสกุล ................................................ อายุ .............. ปี")

    c.drawString(150, y + 2, data['first_name'])
    c.drawString(300, y + 2, data['last_name'])
    c.drawString(440, y + 2, data['age'])
    y -= 40

    c.drawString(50, y, "เกิดวันที่ .............. เดือน ............................ พ.ศ. .............. ที่อยู่บ้านเลขที่ ............... หมู่ที่ ........ ตรอก/ซอย .................................")
    c.drawString(110, y + 2, data['birth_day'])
    c.drawString(175, y + 2, data['birth_month'])
    c.drawString(255, y + 2, data['birth_year'])
    c.drawString(358, y + 2, data['house_number'])
    c.drawString(428, y + 2, data['village'])
    c.drawString(510, y + 2, data['alley'])
    y -= 40

    c.drawString(50, y, "ถนน............................. ตําบล............................ อําเภอ............................ จังหวัด ....................................................")
    c.drawString(85, y + 2, data['road'])
    c.drawString(180, y + 2, data['subdistrict'])
    c.drawString(300, y + 2, data['district'])
    c.drawString(420, y + 2, data['province'])
    y -= 40

    c.drawString(50, y, "รหัสไปรษณีย์.......................... หมายเลขโทรศัพท์ ...............................................")
    c.drawString(130, y + 2, data['zipcode'])
    c.drawString(260, y + 2, data['phone'])
    y -= 40

    c.drawString(50, y, "2. ประกอบอาชีพ ........................................................................................................................................")
    c.drawString(145, y + 2, data['occupation'])
    y -= 40

    c.drawString(50, y, "3. โรคประจําตัว.......................................................................... กรุ๊ปเลือด.................................................")
    c.drawString(125, y + 2, data['disease'])
    c.drawString(470, y + 2, data['blood_group'])
    y -= 40

    c.drawString(50, y, "4. ศิษย์เก่าโรงเรียนลาดตะเคียนราษฏร์บํารุง รุ่นที่...............................")
    c.drawString(286, y + 2, data['generation'])
    y -= 60

    # เจตจำนง
    c.drawString(70, y, "ข้าพเจ้า.................................................................................. พร้อมปฏิบัติตามระเบียบข้อบังคับของชมรมศิษย์เก่าโรงเรียน")
    c.drawString(130, y + 2, data['consent_name'])
    y -= 25
    c.drawString(50, y, "ลาดตะเคียนราษฏร์บํารุงทุกประการ ให้ความร่วมมือในการพัฒนาการจัดการศึกษาและร่วมกิจกรรมของโรงเรียนตามที่")
    y -= 25
    c.drawString(50, y, "ได้รับการประสานจากชมรมฯ")
    y -= 60

    # ลายเซ็น
    c.drawRightString(width - 50, y, f"ลงชื่อ.................................................{data['consent_name']} ผู้สมัคร")
    y -= 25
    c.drawRightString(width - 96, y, f"({data['consent_name']})")
    y -= 25
    c.drawRightString(width - 50, y, "ลงชื่อ.................................................ผู้รับรอง")
    y -= 25
    c.drawRightString(width - 96, y, "(นายสุพจน์ ห่านทองคำ)")
    y -= 25
    c.drawRightString(width - 50, y, "ประธานชมรมศิษย์เก่าโรงเรียนลาดตะเคียนราษฏร์บํารุง")

    c.save()
    print(f"✅ ฟอร์มพร้อมข้อมูลพอดีจุด (ขยับขึ้น) : {output_pdf}")

# ข้อมูล mock เหมือนเดิม
mock_data = {
    "first_name": "สมชาย",
    "last_name": "ใจดี",
    "age": "35",
    "birth_day": "15",
    "birth_month": "มิถุนายน",
    "birth_year": "2533",
    "house_number": "99",
    "village": "5",
    "alley": "ลาดตะเคียน",
    "road": "ลาดตะเคียน",
    "subdistrict": "ลาดตะเคียน",
    "district": "บ้านโป่ง",
    "province": "ราชบุรี",
    "zipcode": "70110",
    "phone": "0812345678",
    "occupation": "วิศวกร",
    "disease": "ไม่มี",
    "blood_group": "O",
    "generation": "25",
    "consent_name": "สมชาย ใจดี"
}

create_thai_form("ใบสมัครศิษย์เก่า_บนจุด_ยกสูง.pdf", mock_data)
