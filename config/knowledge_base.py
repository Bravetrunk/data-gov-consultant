"""
Core Knowledge Base for data-gov-consultant Platform.
Embedded with Thai & Global Standards: DGA, DAMA-DMBOK, PDPA, ISO/IEC 42001, NIST AI RMF.
"""

DGA_MANDATORY_METADATA_FIELDS = [
    {"no": 1, "field_th": "ประเภทข้อมูล", "field_en": "data_type", "type": "Code", "example": "ข้อมูลระเบียน / ข้อมูลสถิติ / ภูมิสารสนเทศ"},
    {"no": 2, "field_th": "ชื่อชุดข้อมูล", "field_en": "title", "type": "Text", "example": "สถิติการรับบริการผู้ป่วยนอก (OPD)"},
    {"no": 3, "field_th": "องค์กร", "field_en": "owner_org", "type": "Code", "example": "โรงพยาบาลศูนย์ / กรมการแพทย์"},
    {"no": 4, "field_th": "ชื่อผู้ติดต่อ", "field_en": "maintainer", "type": "Text", "example": "กลุ่มงานสารสนเทศทางการแพทย์"},
    {"no": 5, "field_th": "อีเมลผู้ติดต่อ", "field_en": "maintainer_email", "type": "Text", "example": "it_health@hospital.go.th"},
    {"no": 6, "field_th": "คำสำคัญ", "field_en": "tag_string", "type": "Text", "example": "OPD, ผู้ป่วยนอก, บริการสุขภาพ"},
    {"no": 7, "field_th": "รายละเอียด", "field_en": "notes", "type": "Text", "example": "ข้อมูลสรุปจำนวนผู้เข้ารับบริการตรวจรักษาผู้ป่วยนอกประจำเดือน"},
    {"no": 8, "field_th": "วัตถุประสงค์", "field_en": "objective", "type": "Code", "example": "เพื่อการวางแผนกำลังคนและจัดสรรทรัพยากรบริการ"},
    {"no": 9.1, "field_th": "หน่วยความถี่ของการปรับปรุงข้อมูล", "field_en": "update_frequency_unit", "type": "Code", "example": "รายเดือน (Monthly)"},
    {"no": 9.2, "field_th": "ค่าความถี่ของการปรับปรุงข้อมูล", "field_en": "update_frequency_interval", "type": "Number", "example": "1"},
    {"no": 10, "field_th": "ขอบเขตเชิงภูมิศาสตร์หรือเชิงพื้นที่", "field_en": "geo_coverage", "type": "Code", "example": "ระดับจังหวัด / ระดับเขตสุขภาพ"},
    {"no": 11, "field_th": "แหล่งที่มา", "field_en": "data_source", "type": "Text", "example": "ระบบบริหารจัดการโรงพยาบาล (HIS)"},
    {"no": 12, "field_th": "รูปแบบการเก็บข้อมูล", "field_en": "data_format", "type": "Code", "example": "Database / CSV / Parquet"},
    {"no": 13, "field_th": "หมวดหมู่ข้อมูลตามธรรมาภิบาลข้อมูลภาครัฐ", "field_en": "data_category", "type": "Code", "example": "ข้อมูลส่วนบุคคล (PDPA ม.26 ข้อมูลสุขภาพ) / ข้อมูลใช้ภายใน"},
    {"no": 14, "field_th": "สัญญาอนุญาตให้ใช้ข้อมูล", "field_en": "license_id", "type": "Code", "example": "Government Data License / Internal Restrictive License"}
]

DATA_QUALITY_5_DIMENSIONS = {
    "accuracy_completeness": {
        "th": "ความถูกต้องและสมบูรณ์",
        "description": "ความแม่นยำ ปราศจากข้อผิดพลาด และครบถ้วนทุกฟิลด์ที่จำเป็น",
        "weight": 0.25,
        "indicators": ["ความครบถ้วนของเรคคอร์ด", "ความถูกต้องตาม Single Source of Truth", "ไม่มีค่าว่างในคีย์หลัก"]
    },
    "consistency": {
        "th": "ความสอดคล้องกัน",
        "description": "รูปแบบและรหัสตรงตามมาตรฐานเดียวกันข้ามตารางและระบบ",
        "weight": 0.20,
        "indicators": ["ใช้รูปแบบวันที่เดียวกัน (ISO 8601)", "รหัสมาตรฐานสากล/ระดับประเทศ (เช่น ICD-10, TMT, รหัสไปรษณีย์)"]
    },
    "timeliness": {
        "th": "ความเป็นปัจจุบัน",
        "description": "ข้อมูลทันสมัยและพร้อมใช้งานตรงตามรอบเวลาที่กำหนด",
        "weight": 0.20,
        "indicators": ["การอัปเดตตรงตามรอบปฏิทิน", "ความถี่เพียงพอต่อการตัดสินใจ"]
    },
    "relevancy": {
        "th": "ตรงตามความต้องการของผู้ใช้",
        "description": "ตอบโจทย์ตัวชี้วัด ยุทธศาสตร์ และการปฏิบัติงานจริง",
        "weight": 0.15,
        "indicators": ["มีผู้ใช้งานนำฟิลด์ไปใช้จริงในรายงาน/โมเดล", "มีแบบประเมินความพึงพอใจ"]
    },
    "availability": {
        "th": "ความพร้อมใช้",
        "description": "เข้าถึงได้สะดวกตามสิทธิ์ที่ถูกต้อง และอยู่ในรูปแบบ Machine-Readable",
        "weight": 0.20,
        "indicators": ["เก็บในรูปแบบฐานข้อมูล/API", "มี Data Catalog และขั้นตอนขอสิทธิ์ชัดเจน"]
    }
}

DATA_CLASSIFICATION_LEVELS = [
    {"level": 1, "name_th": "ลับที่สุด (Top Secret)", "color": "7B1113", "description": "กระทบต่อความมั่นคงแห่งรัฐอย่างร้ายแรงที่สุด"},
    {"level": 2, "name_th": "ลับมาก (Secret)", "color": "C0392B", "description": "กระทบต่อความมั่นคงแห่งรัฐหรือประโยชน์สาธารณะอย่างร้ายแรง"},
    {"level": 3, "name_th": "ลับ (Confidential)", "color": "E67E22", "description": "กระทบต่อชื่อเสียง การดำเนินงาน หรือข้อมูลส่วนบุคคลอ่อนไหว (PDPA ม.26)"},
    {"level": 4, "name_th": "ข้อมูลใช้ภายใน (Internal Use Only)", "color": "2980B9", "description": "ใช้เพื่อการดำเนินงานภายในองค์กร ห้ามเผยแพร่ภายนอกก่อนอนุญาต"},
    {"level": 5, "name_th": "ข้อมูลสาธารณะ (Public Data)", "color": "27AE60", "description": "เปิดเผยได้ทั่วไป ไม่มีความเสี่ยงต่อองค์กรหรือบุคคล"}
]

INDUSTRY_ACCELERATORS = {
    "healthcare": {
        "name_th": "การแพทย์และโรงพยาบาล (Healthcare)",
        "regulatory_drivers": ["PDPA ม.26 (ข้อมูลสุขภาพอ่อนไหว)", "พ.ร.บ. สุขภาพแห่งชาติ ม.7", "พ.ร.บ. ไซเบอร์ (หน่วยงาน CII)"],
        "standards": ["HL7 FHIR", "ICD-10", "ICD-9-CM", "SNOMED CT", "TMT"],
        "high_value_use_cases": [
            {
                "id": "HC-01",
                "title": "Predictive Bed Occupancy & Discharge Analytics",
                "impact": 5, "feasibility": 4,
                "annual_benefit": 8_500_000.0, "cost": 1_900_000.0,
                "benefit_desc": "พยากรณ์อัตราการครองเตียงล่วงหน้า 48 ชม. ลดเวลารอคอยผู้ป่วยใน (IPD) 35%",
                "target_data": ["HIS Admission Logs", "Electronic Medical Records (EMR)", "Nurse Shift Data"]
            },
            {
                "id": "HC-02",
                "title": "Medical Billing & DRG Claims Optimization",
                "impact": 5, "feasibility": 4,
                "annual_benefit": 15_000_000.0, "cost": 2_800_000.0,
                "benefit_desc": "ตรวจสอบความสมบูรณ์ของรหัสโรค ICD-10 ก่อนส่งเคลม สปสช. ลดอัตราเคลมตก 18%",
                "target_data": ["Doctor Discharge Summary", "Diagnosis Code Table", "Billing Details"]
            },
            {
                "id": "HC-03",
                "title": "Clinical AI De-identification & Research Sandbox",
                "impact": 4, "feasibility": 3,
                "annual_benefit": 5_000_000.0, "cost": 1_900_000.0,
                "benefit_desc": "สร้างระบบตัดตัวตนผู้ป่วยอัตโนมัติ (Anonymization) สำหรับงานวิจัย AI ทางการแพทย์",
                "target_data": ["PACS Imaging Metadata", "Lab Results", "Pathology Reports"]
            }
        ],
        "default_catalog": [
            {
                "title": "Electronic Medical Records & Clinical Summaries",
                "maintainer": "กลุ่มงานเวชระเบียนและสารสนเทศ",
                "tag_string": "EMR, ประวัติการรักษา, การวินิจฉัย",
                "notes": "บันทึกประวัติการตรวจรักษา รายการยา ผลแล็บ และหัตถการทางการแพทย์",
                "objective": "เพื่อการรักษาพยาบาลและการติดตามผลอาการ",
                "frequency": "Daily (รายวัน)", "geo": "ระดับสถานพยาบาล",
                "source": "HIS Database", "format": "RDBMS / JSON",
                "category": "ข้อมูลส่วนบุคคลอ่อนไหว (PDPA ม.26)",
                "license": "Internal Restrictive License", "score": 91.5, "classification": "ลับ (Confidential)"
            },
            {
                "title": "Inpatient Bed Occupancy & Admission Registry",
                "maintainer": "ฝ่ายการพยาบาลและบริหารเตียง",
                "tag_string": "IPD, อัตราครองเตียง, วอร์ด",
                "notes": "สถานะเตียงว่าง เตียงที่ครองอยู่ การย้ายหอผู้ป่วย และการจำหน่าย",
                "objective": "เพื่อการบริหารจัดการเตียงและการพยากรณ์ความต้องการบุคลากร",
                "frequency": "Real-time (ตามเวลาจริง)", "geo": "ระดับหอผู้ป่วย",
                "source": "Bed Management System", "format": "RDBMS",
                "category": "ข้อมูลใช้ภายใน (Internal Use Only)",
                "license": "Internal License", "score": 87.0, "classification": "ข้อมูลใช้ภายใน (Internal Use Only)"
            },
            {
                "title": "Medical Billing & Health Insurance Claims",
                "maintainer": "ฝ่ายการเงินและประกันสุขภาพ",
                "tag_string": "Billing, เคลมประกัน, สปสช, กรมบัญชีกลาง",
                "notes": "รายละเอียดค่ารักษาพยาบาล รหัสโรค ICD-10 และสถานะการเบิกจ่าย",
                "objective": "เพื่อการตรวจสอบความถูกต้องของการเบิกจ่ายงบประมาณ",
                "frequency": "Monthly (รายเดือน)", "geo": "ระดับสถานพยาบาล",
                "source": "Billing & Claims System", "format": "RDBMS / CSV",
                "category": "ข้อมูลความลับทางการเงินและข้อมูลส่วนบุคคล",
                "license": "Restricted Financial License", "score": 94.2, "classification": "ลับ (Confidential)"
            }
        ]
    },
    "retail": {
        "name_th": "ค้าปลีกและสินค้าอุปโภคบริโภค (Retail / FMCG)",
        "regulatory_drivers": ["PDPA ม.24 (ฐานสัญญา/ความยินยอม)", "พ.ร.บ. คุ้มครองผู้บริโภค", "พ.ร.บ. การแข่งขันทางการค้า"],
        "standards": ["GS1", "UNSPSC"],
        "high_value_use_cases": [
            {
                "id": "RET-01",
                "title": "Omnichannel Customer 360 & Dynamic Personalization",
                "impact": 5, "feasibility": 4,
                "annual_benefit": 12_500_000.0, "cost": 2_200_000.0,
                "benefit_desc": "เชื่อมโยงข้อมูลหน้าร้านและออนไลน์ วิเคราะห์ LTV และเพิ่ม Conversion Rate 18%",
                "target_data": ["POS Transactions", "E-Commerce Events", "CRM Loyalty Data"]
            },
            {
                "id": "RET-02",
                "title": "AI Demand Forecasting & Automated Replenishment",
                "impact": 5, "feasibility": 4,
                "annual_benefit": 18_000_000.0, "cost": 2_900_000.0,
                "benefit_desc": "พยากรณ์ยอดสั่งซื้อสินค้าล่วงหน้า ลดปัญหาสินค้าค้างสต็อก (Holding Cost) 22%",
                "target_data": ["Sales History", "Warehouse Inventory", "Promotion Calendars"]
            },
            {
                "id": "RET-03",
                "title": "Real-Time Dynamic Pricing & Competitor Scraping",
                "impact": 4, "feasibility": 3,
                "annual_benefit": 6_500_000.0, "cost": 1_800_000.0,
                "benefit_desc": "ปรับเปลี่ยนราคาสินค้าตามกลไกดีมานด์และราคาคู่แข่ง เพิ่ม Gross Margin 2.4%",
                "target_data": ["Product Catalog", "Market Price Scraping", "Competitor Feeds"]
            }
        ],
        "default_catalog": [
            {
                "title": "Omnichannel POS & Transaction Logs",
                "maintainer": "ฝ่ายเทคโนโลยีสารสนเทศและการค้าปลีก",
                "tag_string": "POS, ยอดขาย, ตะกร้าสินค้า",
                "notes": "รายการการซื้อสินค้าจากหน้าร้านทุกสาขาและช่องทางออนไลน์",
                "objective": "เพื่อการวิเคราะห์พฤติกรรมการซื้อและคำนวณรายได้",
                "frequency": "Near Real-time (ทุก 15 นาที)", "geo": "ระดับสาขา/ประเทศ",
                "source": "POS Cloud Database", "format": "RDBMS / Parquet",
                "category": "ข้อมูลความลับทางธุรกิจและข้อมูลส่วนบุคคล",
                "license": "Internal Restrictive License", "score": 93.0, "classification": "ลับ (Confidential)"
            },
            {
                "title": "Customer Profile & Loyalty Membership Registry",
                "maintainer": "ฝ่ายการตลาดและบริหารลูกค้าสัมพันธ์ (CRM)",
                "tag_string": "CRM, ลูกค้า, แต้มสะสม",
                "notes": "ข้อมูลสมาชิก ข้อมูลติดต่อ พฤติกรรมการสะสมแต้ม และการให้ความยินยอม PDPA",
                "objective": "เพื่อการทำการตลาดแบบเฉพาะบุคคลและการสื่อสารสิทธิประโยชน์",
                "frequency": "Daily (รายวัน)", "geo": "ระดับประเทศ",
                "source": "CRM Database", "format": "RDBMS",
                "category": "ข้อมูลส่วนบุคคล (PDPA ม.24)",
                "license": "Internal CRM License", "score": 89.5, "classification": "ลับ (Confidential)"
            },
            {
                "title": "Central Inventory & Supply Chain Tracking",
                "maintainer": "ฝ่ายคลังสินค้าและการกระจายสินค้า",
                "tag_string": "สต็อก, สินค้าคงคลัง, SKU",
                "notes": "จำนวนสินค้าคงเหลือในคลังกลางและคลังสาขา อัตราการหมุนเวียนสินค้า",
                "objective": "เพื่อการเติมเต็มสินค้าอัตโนมัติและการวางแผนจัดซื้อ",
                "frequency": "Hourly (รายชั่วโมง)", "geo": "ระดับศูนย์กระจายสินค้า",
                "source": "WMS / ERP System", "format": "Database / API",
                "category": "ข้อมูลใช้ภายใน (Internal Use Only)",
                "license": "Internal Operations License", "score": 91.0, "classification": "ข้อมูลใช้ภายใน (Internal Use Only)"
            }
        ]
    },
    "manufacturing": {
        "name_th": "โรงงานผลิตและห่วงโซ่อุปทาน (Manufacturing & Supply Chain)",
        "regulatory_drivers": ["ISO 9001", "ISO 27001", "กฎหมายโรงงานและความปลอดภัยอุตสาหกรรม"],
        "standards": ["OPC-UA", "ISA-95", "MQTT"],
        "high_value_use_cases": [
            {
                "id": "MFG-01",
                "title": "Predictive Equipment Maintenance & OEE Optimization",
                "impact": 5, "feasibility": 4,
                "annual_benefit": 16_500_000.0, "cost": 2_600_000.0,
                "benefit_desc": "วิเคราะห์สัญญาณเซนเซอร์ IoT เครื่องจักร เพื่อเตือนการชำรุดล่วงหน้า ลด Unplanned Downtime 40%",
                "target_data": ["SCADA / PLC Logs", "Maintenance Records", "Production Output"]
            },
            {
                "id": "MFG-02",
                "title": "Computer Vision AI for Real-Time Defect Detection",
                "impact": 5, "feasibility": 4,
                "annual_benefit": 11_000_000.0, "cost": 2_100_000.0,
                "benefit_desc": "ใช้กล้อง AI ตรวจจับข้อบกพร่องชิ้นงานบนสายการผลิต ลดของเสีย (Scrap Rate) 30%",
                "target_data": ["Camera Image Streams", "QA Inspection Logs", "Defect Specs"]
            },
            {
                "id": "MFG-03",
                "title": "Supply Chain Lead-Time & Logistics Optimization",
                "impact": 4, "feasibility": 3,
                "annual_benefit": 7_200_000.0, "cost": 1_700_000.0,
                "benefit_desc": "พยากรณ์ความล่าช้าในการจัดส่งวัตถุดิบและคำนวณเส้นทางขนส่งประหยัดพลังงาน",
                "target_data": ["Supplier Shipping Feeds", "GPS Telematics", "Customs Clearance Data"]
            }
        ],
        "default_catalog": [
            {
                "title": "IoT Machine Sensor Telemetry Logs",
                "maintainer": "ฝ่ายวิศวกรรมและการบำรุงรักษา",
                "tag_string": "IoT, อุณหภูมิ, การสั่นสะเทือน, SCADA",
                "notes": "ข้อมูลสัญญาณเซนเซอร์จากเครื่องจักรหลักในสายการผลิต อัตราการหมุน อุณหภูมิ",
                "objective": "เพื่อการวิเคราะห์สุขภาพเครื่องจักรและป้องกันการหยุดชะงัก",
                "frequency": "Streaming / Sub-second", "geo": "ระดับโรงงาน/ไลน์ผลิต",
                "source": "Time-Series IoT Database (InfluxDB/Kafka)", "format": "Parquet / JSON",
                "category": "ข้อมูลความลับทางเทคนิค (Technical IP)",
                "license": "Proprietary License", "score": 95.0, "classification": "ลับมาก (Secret)"
            },
            {
                "title": "Quality Assurance & Defect Inspection History",
                "maintainer": "ฝ่ายควบคุมคุณภาพ (QA/QC)",
                "tag_string": "QA, QC, ตำหนิ, อัตราของเสีย",
                "notes": "ประวัติการตรวจสอบคุณภาพชิ้นงาน สาเหตุของเสีย และการเคลมจากลูกค้า",
                "objective": "เพื่อการปรับปรุงกระบวนการผลิตและการรับประกันคุณภาพ",
                "frequency": "Daily (รายวัน)", "geo": "ระดับโรงงาน",
                "source": "MES (Manufacturing Execution System)", "format": "RDBMS",
                "category": "ข้อมูลใช้ภายใน (Internal Use Only)",
                "license": "Internal QA License", "score": 88.5, "classification": "ข้อมูลใช้ภายใน (Internal Use Only)"
            },
            {
                "title": "Supplier Lead-Time & Logistics Performance",
                "maintainer": "ฝ่ายจัดซื้อและห่วงโซ่อุปทาน",
                "tag_string": "จัดซื้อ, ซัพพลายเออร์, ระยะเวลาส่งมอบ",
                "notes": "ประวัติการส่งมอบวัตถุดิบ ความตรงต่อเวลา และราคาจัดซื้อย้อนหลัง",
                "objective": "เพื่อการประเมินผู้ค้าและการบริหารความเสี่ยงห่วงโซ่อุปทาน",
                "frequency": "Weekly (รายสัปดาห์)", "geo": "ระดับประเทศ/คู่ค้า",
                "source": "ERP Procurement Module", "format": "RDBMS / CSV",
                "category": "ข้อมูลความลับทางการค้า (Commercial Secrets)",
                "license": "Restricted Commercial License", "score": 90.0, "classification": "ลับ (Confidential)"
            }
        ]
    },
    "public_sector": {
        "name_th": "หน่วยงานภาครัฐและรัฐวิสาหกิจ (Public Sector)",
        "regulatory_drivers": ["พ.ร.บ. ดิจิทัล 2562", "ประกาศ สพร. ธรรมาภิบาลข้อมูลภาครัฐ 2563", "พ.ร.บ. ข้อมูลข่าวสาร 2540"],
        "standards": ["มรด. (มาตรฐานรัฐบาลดิจิทัล)", "GD Catalog", "data.go.th Open Data"],
        "high_value_use_cases": [
            {
                "id": "PUB-01",
                "title": "Agency Data Catalog & Open Data Automated Pipeline",
                "impact": 5, "feasibility": 5,
                "annual_benefit": 9_000_000.0, "cost": 1_600_000.0,
                "benefit_desc": "จัดทำบัญชีข้อมูลหน่วยงานเชื่อมต่อ GD Catalog และ data.go.th ผ่านเกณฑ์ประเมิน 100%",
                "target_data": ["Registry Tables", "Statistical Summaries", "Public Reports"]
            },
            {
                "id": "PUB-02",
                "title": "Citizen Service Journey Analytics & One-Stop Portal",
                "impact": 5, "feasibility": 4,
                "annual_benefit": 14_000_000.0, "cost": 2_400_000.0,
                "benefit_desc": "วิเคราะห์ระยะเวลาการให้บริการประชาชน ลดขั้นตอนและเวลาติดต่อราชการลง 45%",
                "target_data": ["Queue System Logs", "Citizen Feedback", "e-Service Transactions"]
            },
            {
                "id": "PUB-03",
                "title": "Inter-Agency Secure Data Exchange (API Gateway)",
                "impact": 4, "feasibility": 4,
                "annual_benefit": 6_500_000.0, "cost": 1_500_000.0,
                "benefit_desc": "เชื่อมโยงแลกเปลี่ยนข้อมูลระหว่างหน่วยงานรัฐผ่าน Government Data Exchange ปลอดภัย 100%",
                "target_data": ["Identification Registry", "Permit & License Records"]
            }
        ],
        "default_catalog": [
            {
                "title": "Government Citizen Service Transaction Registry",
                "maintainer": "ศูนย์เทคโนโลยีสารสนเทศและการสื่อสาร",
                "tag_string": "บริการประชาชน, ธุรกรรม, e-Service",
                "notes": "สถิติการยื่นคำขอรับบริการ ใบอนุญาต และการชำระค่าธรรมเนียมผ่านระบบดิจิทัล",
                "objective": "เพื่อการติดตามประสิทธิภาพการบริการสาธารณะและการวางแผนกำลังคน",
                "frequency": "Monthly (รายเดือน)", "geo": "ระดับประเทศ",
                "source": "e-Service Transaction Database", "format": "RDBMS / JSON",
                "category": "ข้อมูลใช้ภายในและข้อมูลสถิติ",
                "license": "Government Open Data License", "score": 92.0, "classification": "ข้อมูลใช้ภายใน (Internal Use Only)"
            },
            {
                "title": "Public Sector Open Data Dataset (สถิติสาธารณะ)",
                "maintainer": "กลุ่มงานสารนิเทศและเผยแพร่ข้อมูล",
                "tag_string": "ข้อมูลเปิด, สถิติ, สพร, data.go.th",
                "notes": "ข้อมูลสถิติผลการดำเนินงานที่เปิดเผยต่อสาธารณะตาม พ.ร.บ. ข้อมูลข่าวสาร",
                "objective": "เพื่อความโปร่งใสและการนำข้อมูลไปใช้ประโยชน์ของภาคประชาชน",
                "frequency": "Quarterly (รายไตรมาส)", "geo": "ระดับประเทศ",
                "source": "Agency Open Data Portal", "format": "CSV / API",
                "category": "ข้อมูลสาธารณะ (Public Data)",
                "license": "DGA Open Government License", "score": 96.0, "classification": "ข้อมูลสาธารณะ (Public Data)"
            },
            {
                "title": "Official Identity & License Verification Registry",
                "maintainer": "สำนักทะเบียนและกำกับใบอนุญาต",
                "tag_string": "ทะเบียน, ตรวจสอบตัวตน, ใบอนุญาต",
                "notes": "ฐานข้อมูลการตรวจสอบสิทธิ์และสถานะใบอนุญาตประกอบวิชาชีพ/กิจการ",
                "objective": "เพื่อการบูรณาการข้อมูลข้ามหน่วยงานตามนโยบายรัฐบาลดิจิทัล",
                "frequency": "Daily (รายวัน)", "geo": "ระดับประเทศ",
                "source": "National Registry Database", "format": "RDBMS / API",
                "category": "ข้อมูลความลับทางราชการและข้อมูลส่วนบุคคล",
                "license": "Inter-Agency Restricted License", "score": 94.5, "classification": "ลับ (Confidential)"
            }
        ]
    },
    "bfsi": {
        "name_th": "การเงิน ธนาคาร และการประกันภัย (Banking, Finance & Insurance)",
        "regulatory_drivers": ["ประกาศ ธปท. ว่าด้วยการกำกับดูแลความเสี่ยงด้านเทคโนโลยี", "ประกาศ คปภ.", "PDPA ข้อมูลทางการเงิน"],
        "standards": ["ISO 20022", "PCI-DSS", "IFRS 9 / IFRS 17"],
        "high_value_use_cases": [
            {
                "id": "BFSI-01",
                "title": "Real-Time AI Fraud Detection & Anti-Money Laundering (AML)",
                "impact": 5, "feasibility": 4,
                "annual_benefit": 28_000_000.0, "cost": 3_500_000.0,
                "benefit_desc": "ตรวจจับธุรกรรมผิดปกติและเส้นทางการเงินที่น่าสงสัยแบบ Real-time ลดความเสียหาย 65%",
                "target_data": ["Core Banking Transactions", "ATM / Mobile App Telemetry", "Watchlist DB"]
            },
            {
                "id": "BFSI-02",
                "title": "Alternative Data Credit Scoring & Underwriting AI",
                "impact": 5, "feasibility": 4,
                "annual_benefit": 22_000_000.0, "cost": 3_100_000.0,
                "benefit_desc": "วิเคราะห์ความเสี่ยงสินเชื่อด้วยข้อมูลทางเลือก เพิ่มอัตราการอนุมัติ 20% โดย NPL ไม่เพิ่มขึ้น",
                "target_data": ["Credit Bureau Records", "Utility Bill Payments", "Merchant POS Cashflows"]
            },
            {
                "id": "BFSI-03",
                "title": "Automated Insurance Claims Processing & Fraud Flagging",
                "impact": 4, "feasibility": 4,
                "annual_benefit": 12_000_000.0, "cost": 2_200_000.0,
                "benefit_desc": "อนุมัติเคลมประกันภัยอัตโนมัติภายใน 5 นาที พร้อมคัดกรองเคสทุจริตความเสี่ยงสูง",
                "target_data": ["Claim Documentation", "Hospital Billing Feeds", "Vehicle Garage Invoices"]
            }
        ],
        "default_catalog": [
            {
                "title": "Core Banking Real-Time Transaction Ledger",
                "maintainer": "ฝ่ายระบบเทคโนโลยีธุรกรรมการเงิน",
                "tag_string": "บัญชี, โอนเงิน, ธุรกรรม, PCI-DSS",
                "notes": "บันทึกการทำธุรกรรมทางการเงินของลูกค้าทุกช่องทาง บัญชีเงินฝาก สินเชื่อ บัตรเครดิต",
                "objective": "เพื่อการบันทึกบัญชี การตรวจจับการฉ้อโกง และการรายงาน ธปท.",
                "frequency": "Real-time (ตามเวลาจริง)", "geo": "ระดับประเทศ/สากล",
                "source": "Core Banking Mainframe / Kafka", "format": "Database / Event Stream",
                "category": "ข้อมูลความลับทางการเงินสูงสุด (Financial Secrets)",
                "license": "Strict Banking Security License", "score": 98.0, "classification": "ลับที่สุด (Top Secret)"
            },
            {
                "title": "Customer Credit History & KYC Verification Data",
                "maintainer": "ฝ่ายวิเคราะห์สินเชื่อและบริหารความเสี่ยง",
                "tag_string": "KYC, เครดิตบูโร, ความเสี่ยง, สกอร์ริ่ง",
                "notes": "ข้อมูลการยืนยันตัวตน (e-KYC) ประวัติเครดิตบูโร และการประเมินความสามารถชำระหนี้",
                "objective": "เพื่อการพิจารณาอนุมัติสินเชื่อตามเกณฑ์ ธปท. และกฎหมาย PDPA",
                "frequency": "Daily (รายวัน)", "geo": "ระดับประเทศ",
                "source": "Credit Risk Data Mart", "format": "RDBMS / Parquet",
                "category": "ข้อมูลส่วนบุคคลทางการเงิน (Sensitive Financial Data)",
                "license": "Restricted Risk License", "score": 95.5, "classification": "ลับมาก (Secret)"
            },
            {
                "title": "Insurance Policy & Claims Settlement Records",
                "maintainer": "ฝ่ายปฏิบัติการสินไหมประกันภัย",
                "tag_string": "กรมธรรม์, เคลม, ประกันชีวิต, ประกันวินาศภัย",
                "notes": "รายละเอียดกรมธรรม์ ประวัติการยื่นเคลมค่ารักษา/อุบัติเหตุ และการจ่ายสินไหม",
                "objective": "เพื่อการบริหารจัดการสินไหม การตั้งสำรองตามมาตรฐาน IFRS 17",
                "frequency": "Daily (รายวัน)", "geo": "ระดับประเทศ",
                "source": "Insurance Core System", "format": "RDBMS",
                "category": "ข้อมูลความลับและข้อมูลส่วนบุคคล",
                "license": "Internal Insurance License", "score": 93.0, "classification": "ลับ (Confidential)"
            }
        ]
    }
}
