"""
Extended Healthcare & Enterprise Domain Data for GovAgent.
Contains 10 Use Cases, 42 RACI Lifecycle Activities, and 12 Data Catalog Records.
"""

from models.state import UseCaseItem, RACIItem, MetadataRecord

HEALTHCARE_10_USE_CASES = [
    UseCaseItem(
        id="HC-01",
        title="Predictive Bed Occupancy & Discharge Analytics",
        business_unit="ฝ่ายการพยาบาลและการบริหารเตียง",
        business_problem="ผู้ป่วยฉุกเฉินและผู้ป่วยนัดผ่าตัดรอเตียงนานเกิน 6 ชม. เนื่องจากอัตราการครองเตียงไม่เรียลไทม์",
        impact_score=5,
        feasibility_score=4,
        estimated_annual_benefit_thb=8_500_000.0,
        implementation_cost_thb=1_900_000.0,
        payback_months=2.7,
        priority_tier="Quick Win",
        required_datasets=["Inpatient Bed Registry", "Nurse Shift Logs", "Doctor Discharge Orders"]
    ),
    UseCaseItem(
        id="HC-02",
        title="Medical Billing & DRG Claims Optimization",
        business_unit="ฝ่ายการเงินและประกันสุขภาพ",
        business_problem="รหัสโรค ICD-10 และหัตถการไม่ครบถ้วน ทำให้ถูกหักเงินเคลมตกจาก สปสช. และบริษัทประกันกว่า 15 ลบ./ปี",
        impact_score=5,
        feasibility_score=5,
        estimated_annual_benefit_thb=15_000_000.0,
        implementation_cost_thb=2_800_000.0,
        payback_months=2.2,
        priority_tier="Quick Win",
        required_datasets=["Discharge Summaries", "Medical Billing & Claims", "ICD-10 Mapping Tables"]
    ),
    UseCaseItem(
        id="HC-03",
        title="Master Patient Index (EMPI) & Deduplication Engine",
        business_unit="ฝ่ายเวชระเบียนและสารสนเทศ",
        business_problem="มีคนไข้เปิด HN ซ้ำซ้อนระหว่าง OPD, แผนกตรวจสุขภาพ และศูนย์ความงามกว่า 25,000 ราย ทำให้ประวัติแพ้ยาไม่เชื่อมกัน",
        impact_score=5,
        feasibility_score=4,
        estimated_annual_benefit_thb=11_200_000.0,
        implementation_cost_thb=2_400_000.0,
        payback_months=2.6,
        priority_tier="Quick Win",
        required_datasets=["OPD Master Demographics", "Corporate Checkup DB", "Aesthetics & Wellness CRM"]
    ),
    UseCaseItem(
        id="HC-04",
        title="Clinical AI De-identification & Research Sandbox",
        business_unit="ฝ่ายวิชาการและศูนย์นวัตกรรมการแพทย์",
        business_problem="นักวิจัยทางการแพทย์ไม่สามารถดึงข้อมูลประวัติคนไข้ไปวิจัยได้เพราะติดข้อกฎหมาย PDPA ม.26",
        impact_score=4,
        feasibility_score=4,
        estimated_annual_benefit_thb=6_000_000.0,
        implementation_cost_thb=1_800_000.0,
        payback_months=3.6,
        priority_tier="Strategic Bet",
        required_datasets=["EMR Clinical Notes", "PACS Radiology Feeds", "Pathology Lab Records"]
    ),
    UseCaseItem(
        id="HC-05",
        title="Smart Pharmacy Inventory & Automated Replenishment",
        business_unit="ฝ่ายเภสัชกรรมและคลังยา",
        business_problem="ยาและเวชภัณฑ์มูลค่าสูงบางรายการหมดอายุค้างสต็อก ขณะที่ยาจำเป็นบางตัวขาดสต็อกฉุกเฉิน",
        impact_score=4,
        feasibility_score=5,
        estimated_annual_benefit_thb=7_800_000.0,
        implementation_cost_thb=1_600_000.0,
        payback_months=2.5,
        priority_tier="Quick Win",
        required_datasets=["Pharmacy Dispensing Logs", "Central Drug Inventory", "Expiry Date Master"]
    ),
    UseCaseItem(
        id="HC-06",
        title="Outpatient Appointment No-Show Predictor & Smart Scheduling",
        business_unit="ฝ่ายบริการลูกค้าและคลินิกผู้ป่วยนอก",
        business_problem="อัตราคนไข้ผิดนัด (No-Show Rate) สูงถึง 22% ทำให้แพทย์ว่างงานและห้องตรวจสูญเสียรายได้",
        impact_score=4,
        feasibility_score=4,
        estimated_annual_benefit_thb=5_400_000.0,
        implementation_cost_thb=1_400_000.0,
        payback_months=3.1,
        priority_tier="Quick Win",
        required_datasets=["Appointment History", "SMS Notification Logs", "Patient Demographics"]
    ),
    UseCaseItem(
        id="HC-07",
        title="Operating Theatre (OR) Schedule & Resource Optimizer",
        business_unit="ฝ่ายศัลยกรรมและห้องผ่าตัด",
        business_problem="ห้องผ่าตัดมีอัตราการใช้งานเฉลี่ยเพียง 62% มีการเลื่อนคิวผ่าตัดกะทันหันเนื่องจากจัดคิวไม่ลงตัว",
        impact_score=5,
        feasibility_score=3,
        estimated_annual_benefit_thb=12_000_000.0,
        implementation_cost_thb=3_200_000.0,
        payback_months=3.2,
        priority_tier="Strategic Bet",
        required_datasets=["Surgical Bookings", "Anesthesia Logs", "Post-Op Recovery Bed Status"]
    ),
    UseCaseItem(
        id="HC-08",
        title="Radiology Triage AI (Emergency CT/X-Ray Screening)",
        business_unit="ฝ่ายรังสีวิทยาและเวชศาสตร์ฉุกเฉิน",
        business_problem="รังสีแพทย์ไม่เพียงพอในเวรดึก ทำให้ผลอ่านภาพเอกซเรย์สมองในเคสอุบัติเหตุฉุกเฉินล่าช้า",
        impact_score=5,
        feasibility_score=3,
        estimated_annual_benefit_thb=9_500_000.0,
        implementation_cost_thb=2_900_000.0,
        payback_months=3.7,
        priority_tier="Strategic Bet",
        required_datasets=["DICOM Imaging Data", "Radiology Reports", "Emergency Triage Scores"]
    ),
    UseCaseItem(
        id="HC-09",
        title="Sepsis Early-Warning & Deterioration Alert Engine",
        business_unit="หออภิบาลผู้ป่วยวิกฤต (ICU) และอายุรกรรม",
        business_problem="การตรวจพบภาวะติดเชื้อในกระแสเลือด (Sepsis) ล่าช้า เพิ่มอัตราการเสียชีวิตและค่ารักษาพยาบาลวิกฤต",
        impact_score=5,
        feasibility_score=3,
        estimated_annual_benefit_thb=8_000_000.0,
        implementation_cost_thb=2_500_000.0,
        payback_months=3.8,
        priority_tier="Strategic Bet",
        required_datasets=["Vital Signs Monitor Feeds", "Lab CBC/Lactate Results", "Nursing Assessments"]
    ),
    UseCaseItem(
        id="HC-10",
        title="Patient Lifetime Value & Preventive Wellness CRM",
        business_unit="ฝ่ายการตลาดและพัฒนาธุรกิจสุขภาพ",
        business_problem="คนไข้ที่มาตรวจสุขภาพประจำปีไม่เคยถูกติดตามให้กลับมารักษาต่อยอด เสียโอกาสรายได้กว่า 30 ลบ./ปี",
        impact_score=4,
        feasibility_score=5,
        estimated_annual_benefit_thb=10_500_000.0,
        implementation_cost_thb=2_100_000.0,
        payback_months=2.4,
        priority_tier="Quick Win",
        required_datasets=["Annual Checkup Lab Profiles", "CRM Marketing Records", "Health Packages Registry"]
    )
]

FULL_42_RACI_ACTIVITIES = [
    # 1. Planning & Strategy
    RACIItem(task_id="PL-01", category="Planning", activity_name="กำหนดวิสัยทัศน์ พันธกิจ และเป้าหมายธรรมาภิบาลข้อมูลระดับองค์กร",
             data_council="A", lead_data_steward="R", data_owner="C", data_steward_team="S", data_custodian_it="I", data_creator="I", data_user="I", dpo_legal="C"),
    RACIItem(task_id="PL-02", category="Planning", activity_name="จัดทำและทบทวนแผนแม่บทการจัดการข้อมูลประจำปี (Annual Data Master Plan)",
             data_council="A", lead_data_steward="R", data_owner="C", data_steward_team="S", data_custodian_it="S", data_creator="I", data_user="I", dpo_legal="I"),
    RACIItem(task_id="PL-03", category="Planning", activity_name="ประเมินระดับความพร้อมธรรมาภิบาลข้อมูล (DGA Readiness Assessment 0-5)",
             data_council="I", lead_data_steward="A", data_owner="C", data_steward_team="R", data_custodian_it="S", data_creator="I", data_user="I", dpo_legal="C"),
    RACIItem(task_id="PL-04", category="Planning", activity_name="จัดสรรงบประมาณและทรัพยากรบุคคลสำหรับโครงการธรรมาภิบาลข้อมูล",
             data_council="A", lead_data_steward="C", data_owner="C", data_steward_team="I", data_custodian_it="C", data_creator="I", data_user="I", dpo_legal="I"),

    # 2. Data Creation & Acquisition
    RACIItem(task_id="CR-01", category="Create", activity_name="กำหนดนิยามข้อมูลและคำอธิบายชุดข้อมูล (Metadata 14 รายการของ สพร.)",
             data_council="I", lead_data_steward="A", data_owner="C", data_steward_team="R", data_custodian_it="S", data_creator="S", data_user="I", dpo_legal="I"),
    RACIItem(task_id="CR-02", category="Create", activity_name="ออกแบบโครงสร้างและแบบจำลองข้อมูล (Data Modeling & Schema Design)",
             data_council="I", lead_data_steward="C", data_owner="A", data_steward_team="C", data_custodian_it="R", data_creator="I", data_user="I", dpo_legal="I"),
    RACIItem(task_id="CR-03", category="Create", activity_name="กำหนดสิทธิ์ในการสร้าง/บันทึกข้อมูลและทบทวนสิทธิ์ประจำปี",
             data_council="I", lead_data_steward="I", data_owner="A", data_steward_team="C", data_custodian_it="R", data_creator="I", data_user="I", dpo_legal="C"),
    RACIItem(task_id="CR-04", category="Create", activity_name="ตรวจสอบแหล่งที่มาของข้อมูล (Single Source of Truth) ห้ามบันทึกข้อมูลเท็จ",
             data_council="I", lead_data_steward="C", data_owner="A", data_steward_team="R", data_custodian_it="S", data_creator="R", data_user="I", dpo_legal="C"),
    RACIItem(task_id="CR-05", category="Create", activity_name="ลงทะเบียนชุดข้อมูลใหม่เข้าสู่ระบบบัญชีข้อมูล (Data Catalog Registration)",
             data_council="I", lead_data_steward="A", data_owner="C", data_steward_team="R", data_custodian_it="S", data_creator="I", data_user="I", dpo_legal="I"),

    # 3. Data Storage & Infrastructure
    RACIItem(task_id="ST-01", category="Store", activity_name="จัดชั้นความลับของข้อมูล 5 ระดับ (Data Classification Standards)",
             data_council="I", lead_data_steward="C", data_owner="A", data_steward_team="S", data_custodian_it="S", data_creator="I", data_user="I", dpo_legal="R"),
    RACIItem(task_id="ST-02", category="Store", activity_name="เข้ารหัสข้อมูลที่มีชั้นความลับ (Data Encryption at Rest & in Transit)",
             data_council="I", lead_data_steward="I", data_owner="C", data_steward_team="I", data_custodian_it="R", data_creator="I", data_user="I", dpo_legal="A"),
    RACIItem(task_id="ST-03", category="Store", activity_name="กำหนดและควบคุมระยะเวลาการจัดเก็บข้อมูล (Data Retention Schedule)",
             data_council="A", lead_data_steward="C", data_owner="R", data_steward_team="S", data_custodian_it="S", data_creator="I", data_user="I", dpo_legal="R"),
    RACIItem(task_id="ST-04", category="Store", activity_name="สำรองข้อมูลระบบสารสนเทศ (Data Backup) และตรวจสอบความสมบูรณ์",
             data_council="I", lead_data_steward="I", data_owner="I", data_steward_team="I", data_custodian_it="R", data_creator="I", data_user="I", dpo_legal="I"),
    RACIItem(task_id="ST-05", category="Store", activity_name="แยกจัดเก็บข้อมูลส่วนบุคคลและข้อมูลอ่อนไหว (Sensitive Data Partitioning)",
             data_council="I", lead_data_steward="C", data_owner="A", data_steward_team="C", data_custodian_it="R", data_creator="I", data_user="I", dpo_legal="R"),
    RACIItem(task_id="ST-06", category="Store", activity_name="เก็บบันทึกข้อมูลจราจรคอมพิวเตอร์ (Log Retention >= 90 วัน)",
             data_council="I", lead_data_steward="I", data_owner="I", data_steward_team="I", data_custodian_it="R", data_creator="I", data_user="I", dpo_legal="I"),

    # 4. Data Processing & Usage
    RACIItem(task_id="US-01", category="Use", activity_name="อนุมัติคำขอเข้าถึงข้อมูลตามหน้าที่ความรับผิดชอบ (Need-to-Know Principle)",
             data_council="I", lead_data_steward="I", data_owner="A", data_steward_team="C", data_custodian_it="R", data_creator="I", data_user="R", dpo_legal="C"),
    RACIItem(task_id="US-02", category="Use", activity_name="ทบทวนสิทธิ์การเข้าถึงข้อมูลประจำปี (Annual Access Rights Audit)",
             data_council="I", lead_data_steward="A", data_owner="R", data_steward_team="S", data_custodian_it="R", data_creator="I", data_user="I", dpo_legal="C"),
    RACIItem(task_id="US-03", category="Use", activity_name="ควบคุมไม่ให้นำข้อมูลความลับไปใช้ในอุปกรณ์ส่วนตัวหรือพื้นที่สาธารณะ",
             data_council="I", lead_data_steward="C", data_owner="A", data_steward_team="C", data_custodian_it="S", data_creator="I", data_user="R", dpo_legal="C"),
    RACIItem(task_id="US-04", category="Use", activity_name="ทำ Data Masking / Tokenization สำหรับการออกรายงานและแดชบอร์ด BI",
             data_council="I", lead_data_steward="C", data_owner="A", data_steward_team="S", data_custodian_it="R", data_creator="I", data_user="I", dpo_legal="R"),
    RACIItem(task_id="US-05", category="Use", activity_name="ตรวจสอบการประมวลผลข้อมูลตามวัตถุประสงค์ความยินยอม (Consent Tracking)",
             data_council="I", lead_data_steward="C", data_owner="A", data_steward_team="S", data_custodian_it="I", data_creator="I", data_user="I", dpo_legal="R"),
    RACIItem(task_id="US-06", category="Use", activity_name="ระงับการใช้ข้อมูลส่วนบุคคลเมื่อเจ้าของข้อมูลถอนความยินยอม (Consent Revocation)",
             data_council="I", lead_data_steward="C", data_owner="A", data_steward_team="S", data_custodian_it="R", data_creator="I", data_user="I", dpo_legal="R"),

    # 5. Data Publishing & Open Data
    RACIItem(task_id="PB-01", category="Publish", activity_name="คัดเลือกชุดข้อมูลที่มีคุณค่าสูง (High Value Datasets) เพื่อเปิดเผยต่อสาธารณะ",
             data_council="A", lead_data_steward="R", data_owner="C", data_steward_team="S", data_custodian_it="I", data_creator="I", data_user="I", dpo_legal="C"),
    RACIItem(task_id="PB-02", category="Publish", activity_name="ตรวจสอบไม่ให้มีข้อมูลส่วนบุคคล (PII) หลุดในชุดข้อมูลเปิด (Open Data Audit)",
             data_council="I", lead_data_steward="C", data_owner="A", data_steward_team="S", data_custodian_it="I", data_creator="I", data_user="I", dpo_legal="R"),
    RACIItem(task_id="PB-03", category="Publish", activity_name="แปลงข้อมูลเปิดให้อยู่ในรูปแบบ Machine-Readable (CSV, JSON, API)",
             data_council="I", lead_data_steward="I", data_owner="C", data_steward_team="C", data_custodian_it="R", data_creator="I", data_user="I", dpo_legal="I"),
    RACIItem(task_id="PB-04", category="Publish", activity_name="ขออนุมัติการเผยแพร่ข้อมูลเปิดจากคณะกรรมการธรรมาภิบาลข้อมูล",
             data_council="A", lead_data_steward="R", data_owner="C", data_steward_team="S", data_custodian_it="I", data_creator="I", data_user="I", dpo_legal="I"),
    RACIItem(task_id="PB-05", category="Publish", activity_name="เชื่อมต่อชุดข้อมูลเปิดเข้าสู่ระบบ data.go.th และ GD Catalog",
             data_council="I", lead_data_steward="A", data_owner="C", data_steward_team="C", data_custodian_it="R", data_creator="I", data_user="I", dpo_legal="I"),

    # 6. Data Archiving & Disposal
    RACIItem(task_id="AR-01", category="Archive", activity_name="ตรวจสอบและย้ายข้อมูลที่พ้นช่วงใช้งานเข้าสู่ Cold Storage (Data Archiving)",
             data_council="I", lead_data_steward="I", data_owner="A", data_steward_team="C", data_custodian_it="R", data_creator="I", data_user="I", dpo_legal="I"),
    RACIItem(task_id="AR-02", category="Archive", activity_name="ทดสอบการกู้คืนข้อมูลถาวร (Disaster Recovery / Restore Drill) อย่างน้อยปีละ 1 ครั้ง",
             data_council="I", lead_data_steward="I", data_owner="I", data_steward_team="I", data_custodian_it="R", data_creator="I", data_user="I", dpo_legal="I"),
    RACIItem(task_id="DS-01", category="Destroy", activity_name="แต่งตั้งคณะกรรมการตรวจสอบและทำลายข้อมูลที่หมดความจำเป็นตามกฎหมาย",
             data_council="A", lead_data_steward="R", data_owner="C", data_steward_team="S", data_custodian_it="I", data_creator="I", data_user="I", dpo_legal="C"),
    RACIItem(task_id="DS-02", category="Destroy", activity_name="ทำลายข้อมูลตามมาตรฐานความมั่นคงปลอดภัย (Sanitization / Shredding)",
             data_council="I", lead_data_steward="I", data_owner="A", data_steward_team="C", data_custodian_it="R", data_creator="I", data_user="I", dpo_legal="I"),
    RACIItem(task_id="DS-03", category="Destroy", activity_name="จัดเก็บบันทึกประวัติและหลักฐานการทำลายข้อมูล (Destruction Log >= 1 ปี)",
             data_council="I", lead_data_steward="A", data_owner="C", data_steward_team="C", data_custodian_it="R", data_creator="I", data_user="I", dpo_legal="R"),

    # 7. Data Sharing & Interoperability
    RACIItem(task_id="SH-01", category="Exchange", activity_name="จัดทำสัญญาประมวลผลข้อมูล (DPA) และข้อตกลงรักษาความลับ (NDA) กับคู่ค้า",
             data_council="I", lead_data_steward="C", data_owner="A", data_steward_team="I", data_custodian_it="I", data_creator="I", data_user="I", dpo_legal="R"),
    RACIItem(task_id="SH-02", category="Exchange", activity_name="กำหนดมาตรฐานทางเทคนิคสำหรับการแลกเปลี่ยนข้อมูล (API, HL7 FHIR, XML, JSON)",
             data_council="I", lead_data_steward="C", data_owner="C", data_steward_team="C", data_custodian_it="R", data_creator="I", data_user="I", dpo_legal="I"),
    RACIItem(task_id="SH-03", category="Exchange", activity_name="จัดทำระบบบันทึกประวัติการรับ-ส่งข้อมูลข้ามหน่วยงาน (Data Exchange Log)",
             data_council="I", lead_data_steward="I", data_owner="I", data_steward_team="I", data_custodian_it="R", data_creator="I", data_user="I", dpo_legal="I"),

    # 8. Data Quality Assurance
    RACIItem(task_id="DQ-01", category="Quality", activity_name="กำหนดเกณฑ์วัดและสูตรคำนวณคุณภาพข้อมูล 5 มิติ (DQA Matrix)",
             data_council="I", lead_data_steward="A", data_owner="C", data_steward_team="R", data_custodian_it="S", data_creator="I", data_user="I", dpo_legal="I"),
    RACIItem(task_id="DQ-02", category="Quality", activity_name="ดำเนินการตรวจประเมินคุณภาพข้อมูลด้วยตนเอง (DQA Checklist) ทุกไตรมาส",
             data_council="I", lead_data_steward="A", data_owner="C", data_steward_team="R", data_custodian_it="S", data_creator="S", data_user="C", dpo_legal="I"),
    RACIItem(task_id="DQ-03", category="Quality", activity_name="จัดทำแผนปฏิบัติการปรับปรุงคุณภาพข้อมูล (Data Cleansing Action Plan)",
             data_council="I", lead_data_steward="A", data_owner="R", data_steward_team="R", data_custodian_it="S", data_creator="S", data_user="I", dpo_legal="I"),
    RACIItem(task_id="DQ-04", category="Quality", activity_name="จัดทำระบบแจ้งเตือนข้อผิดพลาดของข้อมูลอัตโนมัติ (Automated Data Observability)",
             data_council="I", lead_data_steward="I", data_owner="C", data_steward_team="C", data_custodian_it="R", data_creator="I", data_user="I", dpo_legal="I"),

    # 9. AI Modeling & Ethics Governance
    RACIItem(task_id="AI-01", category="AI Model", activity_name="จัดทำทะเบียนระบบปัญญาประดิษฐ์และจัดชั้นความเสี่ยง AI ตาม ISO 42001",
             data_council="A", lead_data_steward="R", data_owner="C", data_steward_team="S", data_custodian_it="S", data_creator="I", data_user="I", dpo_legal="C"),
    RACIItem(task_id="AI-02", category="AI Model", activity_name="ตรวจสอบชุดข้อมูลเทรนโมเดล AI (Training Data Lineage & Bias Audit)",
             data_council="I", lead_data_steward="A", data_owner="C", data_steward_team="R", data_custodian_it="S", data_creator="I", data_user="R", dpo_legal="C"),
    RACIItem(task_id="AI-03", category="AI Model", activity_name="ทำ Anonymization / De-identification ข้อมูลคนไข้ก่อนส่งให้ทีม AI",
             data_council="I", lead_data_steward="C", data_owner="A", data_steward_team="R", data_custodian_it="S", data_creator="I", data_user="I", dpo_legal="R"),
    RACIItem(task_id="AI-04", category="AI Model", activity_name="กำหนดนโยบาย Human-in-the-Loop สำหรับผลลัพธ์การตัดสินใจทางการแพทย์ของ AI",
             data_council="A", lead_data_steward="C", data_owner="R", data_steward_team="S", data_custodian_it="I", data_creator="I", data_user="R", dpo_legal="C"),
    RACIItem(task_id="AI-05", category="AI Model", activity_name="เฝ้าระวังการรั่วไหลของข้อมูลความลับผ่าน Generative AI Prompts",
             data_council="I", lead_data_steward="I", data_owner="C", data_steward_team="C", data_custodian_it="R", data_creator="I", data_user="R", dpo_legal="A")
]

HEALTHCARE_12_CATALOG_RECORDS = [
    MetadataRecord(
        no=1.0, title="Master Patient Index & Demographics (EMPI Golden Records)",
        owner_org="โรงพยาบาลเอกชนธนบุรีเวชการ", maintainer="กลุ่มงานเวชระเบียนและทะเบียนประวัติ",
        maintainer_email="empi@thonburimed.co.th", tag_string="HN, ผู้ป่วย, ประวัติ, ข้อมูลหลัก, Golden Record",
        notes="ฐานข้อมูลคนไข้กลางที่รวมประวัติและตัดความซ้ำซ้อน 1 คนต่อ 1 HN มีเลขบัตร ปชช. วันเกิด และข้อมูลติดต่อ",
        objective="เพื่อใช้เป็น Single Source of Truth สำหรับการระบุตัวตนคนไข้ทั่วทั้งโรงพยาบาล",
        update_frequency="Real-time (ตามเวลาจริง)", geo_coverage="ระดับสถานพยาบาล/ประเทศ",
        data_source="Enterprise Master Patient Index (EMPI) System", data_format="RDBMS / JSON",
        data_category="ข้อมูลส่วนบุคคลและข้อมูลอ่อนไหว (PDPA ม.26)", license_id="Strict Internal Medical License",
        data_quality_score=94.5, classification_level="ลับมาก (Secret)"
    ),
    MetadataRecord(
        no=2.0, title="Electronic Medical Records (EMR) Clinical Summaries",
        owner_org="โรงพยาบาลเอกชนธนบุรีเวชการ", maintainer="กลุ่มงานสารสนเทศทางการแพทย์และอายุรกรรม",
        maintainer_email="emr@thonburimed.co.th", tag_string="EMR, ประวัติการรักษา, การวินิจฉัย, แพ้ยา",
        notes="บันทึกประวัติการตรวจรักษาของแพทย์ สรุปการวินิจฉัยโรค ประวัติการแพ้ยา และคำสั่งการรักษา",
        objective="เพื่อการรักษาพยาบาล การส่งต่อ และการวิจัยทางคลินิก",
        update_frequency="Daily (รายวัน)", geo_coverage="ระดับสถานพยาบาล",
        data_source="HIS Core EMR Database", data_format="RDBMS / JSON",
        data_category="ข้อมูลส่วนบุคคลอ่อนไหว (PDPA ม.26)", license_id="Restricted Clinical License",
        data_quality_score=92.0, classification_level="ลับ (Confidential)"
    ),
    MetadataRecord(
        no=3.0, title="Outpatient Department (OPD) Visit & Encounter Logs",
        owner_org="โรงพยาบาลเอกชนธนบุรีเวชการ", maintainer="ฝ่ายการพยาบาลผู้ป่วยนอก",
        maintainer_email="opd@thonburimed.co.th", tag_string="OPD, ตรวจรักษา, คลินิก, คิวตรวจ",
        notes="ข้อมูลการเข้ารับบริการผู้ป่วยนอก ระยะเวลารอคอย แผนกตรวจ และสถานะการรับยา",
        objective="เพื่อการติดตามขั้นตอนบริการและการบริหารจัดการคิวตรวจ",
        update_frequency="Near Real-time", geo_coverage="ระดับแผนกตรวจ",
        data_source="OPD Clinic Management System", data_format="RDBMS",
        data_category="ข้อมูลใช้ภายใน (Internal Use Only)", license_id="Internal Operations License",
        data_quality_score=89.5, classification_level="ข้อมูลใช้ภายใน (Internal Use Only)"
    ),
    MetadataRecord(
        no=4.0, title="Inpatient Department (IPD) Admission & Bed Registry",
        owner_org="โรงพยาบาลเอกชนธนบุรีเวชการ", maintainer="ฝ่ายการพยาบาลผู้ป่วยในและการบริหารเตียง",
        maintainer_email="ipd_bed@thonburimed.co.th", tag_string="IPD, นอนโรงพยาบาล, ครองเตียง, หอผู้ป่วย",
        notes="สถานะการครองเตียง การรับผู้ป่วยเข้าพัก การย้ายหอผู้ป่วย และการจำหน่ายกลับบ้าน",
        objective="เพื่อการบริหารจัดการเตียงและการพยากรณ์ความต้องการบุคลากรพยาบาล",
        update_frequency="Real-time (ตามเวลาจริง)", geo_coverage="ระดับหอผู้ป่วย",
        data_source="Bed Management & ADT System", data_format="RDBMS",
        data_category="ข้อมูลใช้ภายใน (Internal Use Only)", license_id="Internal Operations License",
        data_quality_score=91.0, classification_level="ข้อมูลใช้ภายใน (Internal Use Only)"
    ),
    MetadataRecord(
        no=5.0, title="Laboratory Information System (LIS) Test Results",
        owner_org="โรงพยาบาลเอกชนธนบุรีเวชการ", maintainer="กลุ่มงานพยาธิวิทยาคลินิกและเทคนิคการแพทย์",
        maintainer_email="lab@thonburimed.co.th", tag_string="แล็บ, ตรวจเลือด, ปัสสาวะ, CBC, ผลตรวจ",
        notes="ผลการตรวจวิเคราะห์ทางห้องปฏิบัติการ ค่าอ้างอิงมาตรฐาน และการแจ้งเตือนค่าวิกฤต (Critical Values)",
        objective="เพื่อสนับสนุนการวินิจฉัยโรคและการติดตามผลการรักษาของแพทย์",
        update_frequency="Real-time (ตามเวลาจริง)", geo_coverage="ระดับสถานพยาบาล",
        data_source="LIS Laboratory Database", data_format="HL7 / RDBMS",
        data_category="ข้อมูลส่วนบุคคลอ่อนไหว (PDPA ม.26)", license_id="Restricted Clinical License",
        data_quality_score=96.0, classification_level="ลับ (Confidential)"
    ),
    MetadataRecord(
        no=6.0, title="Picture Archiving & Communication System (PACS) Metadata",
        owner_org="โรงพยาบาลเอกชนธนบุรีเวชการ", maintainer="ฝ่ายรังสีวิทยาและการถ่ายภาพทางการแพทย์",
        maintainer_email="pacs@thonburimed.co.th", tag_string="PACS, X-Ray, CT-Scan, MRI, DICOM",
        notes="ข้อมูลเมทาดาตาของภาพถ่ายรังสีทางการแพทย์ รายงานผลการอ่านภาพของรังสีแพทย์",
        objective="เพื่อการวินิจฉัยภาพถ่ายรังสีและต่อยอดสู่โมเดล AI ทางการแพทย์",
        update_frequency="Daily (รายวัน)", geo_coverage="ระดับสถานพยาบาล",
        data_source="PACS Enterprise Server", data_format="DICOM / JSON",
        data_category="ข้อมูลส่วนบุคคลอ่อนไหว (PDPA ม.26)", license_id="Restricted Clinical License",
        data_quality_score=95.0, classification_level="ลับ (Confidential)"
    ),
    MetadataRecord(
        no=7.0, title="Pharmacy Dispensing & Central Drug Inventory",
        owner_org="โรงพยาบาลเอกชนธนบุรีเวชการ", maintainer="ฝ่ายเภสัชกรรมและคลังเวชภัณฑ์",
        maintainer_email="pharmacy@thonburimed.co.th", tag_string="ยา, ใบสั่งยา, คลังยา, เวชภัณฑ์, TMT",
        notes="ประวัติการจ่ายยาให้ผู้ป่วย จำนวนยาคงเหลือในคลัง วันหมดอายุ และรหัสยามาตรฐาน TMT",
        objective="เพื่อการจ่ายยาอย่างถูกต้อง การป้องกันยาตีกัน และการสั่งซื้อยาอัตโนมัติ",
        update_frequency="Real-time (ตามเวลาจริง)", geo_coverage="ระดับห้องยา/คลังยา",
        data_source="Pharmacy Information System", data_format="RDBMS",
        data_category="ข้อมูลส่วนบุคคลและข้อมูลความลับทางการค้า", license_id="Internal Operations License",
        data_quality_score=97.5, classification_level="ลับ (Confidential)"
    ),
    MetadataRecord(
        no=8.0, title="Operating Room (OR) & Surgical Procedure Registry",
        owner_org="โรงพยาบาลเอกชนธนบุรีเวชการ", maintainer="ฝ่ายศัลยกรรมและหอผู้ป่วยผ่าตัด",
        maintainer_email="or@thonburimed.co.th", tag_string="ผ่าตัด, ห้องผ่าตัด, ดมยา, หัตถการ",
        notes="ตารางการใช้ห้องผ่าตัด ทีมแพทย์ศัลยกรรม ระยะเวลาผ่าตัด และบันทึกการดมยาสลบ",
        objective="เพื่อการวางแผนการใช้ห้องผ่าตัดและการรับรองมาตรฐานความปลอดภัยผู้ป่วย",
        update_frequency="Daily (รายวัน)", geo_coverage="ระดับห้องผ่าตัด",
        data_source="OR Management System", data_format="RDBMS",
        data_category="ข้อมูลส่วนบุคคลอ่อนไหวและข้อมูลใช้ภายใน", license_id="Restricted Clinical License",
        data_quality_score=93.5, classification_level="ลับ (Confidential)"
    ),
    MetadataRecord(
        no=9.0, title="Medical Billing, Insurance Claims & DRGs Settlement",
        owner_org="โรงพยาบาลเอกชนธนบุรีเวชการ", maintainer="ฝ่ายการเงินและประกันสุขภาพ",
        maintainer_email="claims@thonburimed.co.th", tag_string="Billing, เคลมประกัน, สปสช, กรมบัญชีกลาง, DRG",
        notes="รายการค่ารักษาพยาบาล รหัสโรค ICD-10/ICD-9-CM สถานะการอนุมัติเคลม และเงินชดเชย",
        objective="เพื่อการเรียกเก็บเงินจากผู้ป่วยและเบิกจ่ายจากกองทุนสุขภาพ/ประกันภัย",
        update_frequency="Monthly (รายเดือน)", geo_coverage="ระดับสถานพยาบาล",
        data_source="Billing & Revenue Management System", data_format="RDBMS / CSV",
        data_category="ข้อมูลความลับทางการเงินและข้อมูลส่วนบุคคล", license_id="Restricted Financial License",
        data_quality_score=94.0, classification_level="ลับ (Confidential)"
    ),
    MetadataRecord(
        no=10.0, title="Corporate & Annual Health Checkup Registry",
        owner_org="โรงพยาบาลเอกชนธนบุรีเวชการ", maintainer="ศูนย์ตรวจสุขภาพและอาชีวอนามัย (Check-up Center)",
        maintainer_email="checkup@thonburimed.co.th", tag_string="ตรวจสุขภาพ, ตรวจประจำปี, องค์กรคู่สัญญา",
        notes="ผลการตรวจสุขภาพประจำปีของพนักงานบริษัทคู่สัญญา ความเสี่ยงโรคเรื้อรัง",
        objective="เพื่อการออกสมุดรายงานผลสุขภาพและการออกแบบโปรแกรมส่งเสริมสุขภาพองค์กร",
        update_frequency="Daily (รายวัน)", geo_coverage="ระดับองค์กรคู่สัญญา",
        data_source="Checkup Information System", data_format="RDBMS / PDF",
        data_category="ข้อมูลส่วนบุคคลอ่อนไหว (PDPA ม.26)", license_id="Restricted Corporate License",
        data_quality_score=90.0, classification_level="ลับ (Confidential)"
    ),
    MetadataRecord(
        no=11.0, title="Emergency Room (ER) Triage & Resuscitation Logs",
        owner_org="โรงพยาบาลเอกชนธนบุรีเวชการ", maintainer="กลุ่มงานเวชศาสตร์ฉุกเฉินและอุบัติเหตุ (ER)",
        maintainer_email="er@thonburimed.co.th", tag_string="ER, ฉุกเฉิน, อุบัติเหตุ, Triage Level",
        notes="ระดับความเร่งด่วนของการรักษา (Emergency Severity Index) และเวลาตอบสนองของทีมกู้ชีพ",
        objective="เพื่อการประเมินคุณภาพการรักษาผู้ป่วยวิกฤตฉุกเฉินตามมาตรฐานสากล",
        update_frequency="Real-time (ตามเวลาจริง)", geo_coverage="ระดับแผนกฉุกเฉิน",
        data_source="Emergency Medical Log", data_format="RDBMS",
        data_category="ข้อมูลส่วนบุคคลอ่อนไหว (PDPA ม.26)", license_id="Internal Emergency License",
        data_quality_score=92.5, classification_level="ลับ (Confidential)"
    ),
    MetadataRecord(
        no=12.0, title="Patient Experience & Service Satisfaction Surveys",
        owner_org="โรงพยาบาลเอกชนธนบุรีเวชการ", maintainer="ฝ่ายบริหารคุณภาพโรงพยาบาลและลูกค้าสัมพันธ์ (CRM)",
        maintainer_email="satisfaction@thonburimed.co.th", tag_string="ความพึงพอใจ, ข้อร้องเรียน, NPS, คุณภาพบริการ",
        notes="คะแนนประเมินความพึงพอใจของคนไข้และญาติ ข้อเสนอแนะ และสถิติการจัดการข้อร้องเรียน",
        objective="เพื่อการพัฒนาคุณภาพการบริการโรงพยาบาล (HA / JCI Re-accreditation)",
        update_frequency="Monthly (รายเดือน)", geo_coverage="ระดับสถานพยาบาล",
        data_source="Patient Feedback Tablet & Survey System", data_format="RDBMS / CSV",
        data_category="ข้อมูลใช้ภายใน (Internal Use Only)", license_id="Internal Quality License",
        data_quality_score=95.0, classification_level="ข้อมูลใช้ภายใน (Internal Use Only)"
    )
]
