# 🤖 AI Agent Playbook for data-gov-consultant
### Step-by-Step Prompt Templates & Autonomous Workflows for AI Agents (Claude Code, OpenAI Codex, GitHub Copilot CLI, Cursor, Antigravity)

คู่มือฉบับนี้จัดทำขึ้นเพื่อให้ **AI Coding Agents** (เช่น Claude Code, Codex, GitHub Copilot, Cursor) สามารถทำงานร่วมกับระบบ `data-gov-consultant` ได้อย่างไร้รอยต่อ ตั้งแต่การ Onboarding ลูกค้า, การสั่งรันสปรินต์ที่ปรึกษา, ไปจนถึงการตรวจสอบและปรับแต่งเอกสารส่งมอบ

---

## 🎯 Playbook 1: การใช้งานผ่าน Claude Code CLI (`claude`)

### สเต็ปที่ 1: การสั่งรัน Discovery & Engagement เริ่มต้น
พิมพ์คำสั่งนี้ในหน้าต่างของ Claude Code:
```text
Role: You are the Lead Engagement Partner in the data-gov-consultant practice.
Task: Run a complete 4-sprint transformation engagement for a new client.

Client Profile:
- Name: โรงพยาบาลมหานครแคร์ (Mahanakorn Care Hospital)
- Industry: healthcare
- Size: Large Enterprise (500 เตียง)
- Budget: 1,800,000,000 THB
- Key Issues: ข้อมูลประวัติการรักษา (EMR) แยกส่วนกับระบบภาพ PACS, การส่งเคลมงบประมาณประกันสุขภาพรหัสโรค ICD-10 ไม่สมบูรณ์, ความกังวลด้าน PDPA ม.26

Instruction:
1. Run the engagement using: `node bin/cli.js run --name "โรงพยาบาลมหานครแคร์" --industry healthcare --budget 1800000000`
2. Once generated, inspect the files in `output/` and provide me with an executive summary highlighting the top 3 use cases and their expected 3-year financial ROI.
```

---

### สเต็ปที่ 2: การสั่งให้ Claude Code ปรับแต่งนโยบายและสถาปัตยกรรมเฉพาะจุด
```text
เปิดไฟล์ output/03_TRANSFORMATION_MASTER_BLUEPRINT.docx และ output/02_GOVERNANCE_RACI_&_DATA_CATALOG.xlsx
ช่วยตรวจสอบและเพิ่มข้อกำหนดดังต่อไปนี้:
1. เพิ่มกระบวนการขอใช้ข้อมูลเพื่อการวิจัยคลินิก (Clinical Research Data Sandbox) โดยต้องผ่านคณะกรรมการจริยธรรมในมนุษย์ (IRB)
2. กำหนดนโยบาย Data Masking สำหรับข้อมูลผลเลือดและประวัติสุขภาพจิต (PDPA ม.26)
3. ปรับบทบาทในตาราง RACI ให้หัวหน้ากลุ่มงานเภสัชกรรมเป็น Data Owner ของข้อมูลการจ่ายยาและคลังยา
```

---

## 🎯 Playbook 2: การใช้งานผ่าน GitHub Copilot CLI / OpenAI Codex

### สเต็ปที่ 1: การสั่งสร้าง Industry Accelerator ใหม่ด้วย Codex
เมื่อมีลูกค้าในอุตสาหกรรมที่ยังไม่มีในระบบ (เช่น อสังหาริมทรัพย์, พลังงาน, การศึกษา):
```text
เขียนฟังก์ชันและข้อมูลคลังความรู้สำหรับอุตสาหกรรมใหม่ "energy_utilities" (พลังงานและสาธารณูปโภค) ลงใน config/knowledge_base.py:
1. Regulatory Drivers: พระราชบัญญัติการประกอบกิจการพลังงาน, กฎหมายสิ่งแวดล้อม, PDPA ข้อมูลผู้ใช้ไฟฟ้า/พลังงาน
2. Standards: IEC 61850, CIM (Common Information Model), ISO 50001
3. High-Value Use Cases:
   - Smart Meter (AMI) Real-Time Data Streaming & Load Forecasting
   - Predictive Asset Health for Power Transformers & Substations
   - Carbon Emission & Renewable Energy Credit (REC) Tracking
4. กำหนดตัวเลข Benefit, Cost และ Payback ที่สอดคล้องกับงบประมาณระดับ 3,000 ล้านบาท
```

---

### สเต็ปที่ 2: การสั่งให้ Codex รัน Data Quality Verification Test
```text
เขียนสคริปต์ทดสอบอัตโนมัติใน tests/test_data_quality_formulas.py เพื่อตรวจสอบว่า:
1. ไฟล์ output/01_FINANCIAL_ROI_&_CLOUD_TCO_MODEL.xlsx มีผลรวมตัวเลข 3-Year TCO ถูกต้องตามสูตร =SUM(B4:E4)*12*3
2. ไฟล์ output/02_GOVERNANCE_RACI_&_DATA_CATALOG.xlsx มีชุดข้อมูลที่มี Data Quality Score >= 80% ครบทุกรายการ
3. รันการทดสอบด้วยคำสั่ง: `.venv/bin/python -m pytest tests/`
```

---

## 🎯 Playbook 3: การใช้งานผ่าน Antigravity / Cursor Composer

สำหรับ Developer ที่ทำงานใน IDE:
```text
@data-gov-consultant ฉันต้องการสร้างข้อเสนอโครงการ (Proposal Deck) สำหรับเข้าประมูลงานธรรมาภิบาลข้อมูลของหน่วยงานภาครัฐ:
1. รันการให้คำปรึกษาด้วยคำสั่ง: `node bin/cli.js run --name "กรมบริการดิจิทัลภาครัฐ" --industry public_sector --budget 800000000`
2. ดึงข้อมูลจาก output/04_EXECUTIVE_BOARD_DECK.md มาสรุปเป็น 3 ข้อเสนอคุณค่าหลัก (Value Propositions):
   - การปฏิบัติตามเกณฑ์ สพร. และ GD Catalog แบบ 100%
   - การประเมินคุณภาพข้อมูล 5 มิติ (DQA/DQC) ตามเกณฑ์ สสช.
   - การลดระยะเวลาส่งมอบงานเหลือเพียง 5 วันทำการ
```

---

## 💡 สรุป Best Practices สำหรับ AI Agents
* **Always Run Gatekeeper Checks:** ก่อนส่งเอกสารให้ผู้ใช้ ให้แน่ใจว่าได้ตรวจสอบความสอดคล้องกันระหว่างเล่ม Word (`.docx`) กับตารางตัวเลขใน Excel (`.xlsx`) เสมอ
* **Right-Sized Tone:** ในการสนทนากับผู้บริหาร ให้ใช้ภาษาแบบ Management Consultant (เน้นผลลัพธ์ทางธุรกิจ, ตัวเลข ROI, และความเสี่ยงทางกฎหมาย) มากกว่าศัพท์เทคนิคเชิงลึก
