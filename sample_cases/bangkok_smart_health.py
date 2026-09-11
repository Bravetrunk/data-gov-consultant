"""
Sample Pilot Case: Bangkok Smart Healthcare System (โรงพยาบาลกรุงเทพสมาร์ทเฮลท์แคร์ ขนาด 400 เตียง)
A real-world inspired scenario facing Data Governance, Big Data integration, and AI transformation challenges.
"""

from models.state import ClientOrganization

BANGKOK_SMART_HEALTH_PROFILE = ClientOrganization(
    name="โรงพยาบาลกรุงเทพสมาร์ทเฮลท์แคร์ (Bangkok Smart Healthcare System)",
    industry="healthcare",
    organization_size="Large Enterprise (400 เตียง)",
    annual_revenue_thb=1_200_000_000.0,
    current_systems=[
        "ระบบสารสนเทศโรงพยาบาล (Hospital Information System - HOSxP)",
        "ระบบจัดเก็บและรับส่งภาพทางการแพทย์ (PACS)",
        "ระบบสารสนเทศห้องปฏิบัติการ (LIS - Laboratory Information System)",
        "ระบบบริหารงานการเงินและการเบิกจ่าย (Billing & Claims System)",
        "ไฟล์ Excel สำรองข้อมูลการครองเตียงและการจัดเวรพยาบาล (Shadow IT)"
    ],
    primary_pain_points=[
        "ข้อมูลประวัติการรักษา (EMR) แยกส่วนกับระบบผลแล็บและรังสีวิทยา ทำให้แพทย์ต้องเปิดหลายโปรแกรมพร้อมกัน",
        "ตัวเลขการครองเตียง (Bed Occupancy) ระหว่างหอผู้ป่วยกับแผนกรับผู้ป่วยไม่ตรงกัน ทำให้ผู้ป่วยฉุกเฉินรอเตียงนานกว่า 6 ชั่วโมง",
        "การส่งเคลมงบประมาณประกันสุขภาพ (สปสช./กรมบัญชีกลาง) มีรหัสโรค ICD-10 ไม่สมบูรณ์ ทำให้ถูกหักเงินเคลมตกปีละกว่า 15 ล้านบาท",
        "ความกังวลด้านกฎหมาย PDPA ม.26 เรื่องข้อมูลสุขภาพรั่วไหล และไม่มีกระบวนการขอใช้ข้อมูลเพื่อทำวิจัยทางการแพทย์อย่างเป็นระบบ",
        "ผู้บริหารต้องการนำ AI มาช่วยพยากรณ์คนไข้และบริหารเตียง แต่ไม่มีระบบ Data Lakehouse กลางรองรับ"
    ],
    target_objectives=[
        "จัดตั้งสภาธรรมาภิบาลข้อมูล (Data Governance Council) และเครือข่าย Data Steward ในทุกแผนก",
        "สร้างสถาปัตยกรรม Modern Data Lakehouse เชื่อมโยงข้อมูล HIS, LIS, PACS เข้าด้วยกันอย่างมั่นคงปลอดภัย",
        "ยกระดับคุณภาพข้อมูล (Data Quality) ให้ผ่านเกณฑ์มาตรฐานกระทรวงสาธารณสุข และรองรับมาตรฐาน HL7 FHIR",
        "ติดตั้งโมเดล AI พยากรณ์การครองเตียงและระบบช่วยตรวจรหัสเคลมโรค (DRGs) ที่ถูกต้องตามหลัก AI Ethics (ISO 42001)",
        "จัดอบรม Data Literacy ให้แก่บุคลากรทางการแพทย์และพยาบาลทั้งองค์กร"
    ]
)
