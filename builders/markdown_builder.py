"""
Markdown Executive Presentation Deck Builder for data-gov-consultant Platform.
Compiles boardroom slide decks (14 slides) for C-Suite and Board of Directors.
"""

import os
from typing import List, Dict, Any
from models.state import ClientOrganization, UseCaseItem, RACIItem, MetadataRecord, CloudTCOComparison


def build_executive_deck_markdown(
    output_path: str,
    client: ClientOrganization,
    maturity_score: int,
    maturity_narrative: str,
    use_cases: List[UseCaseItem],
    tco_list: List[CloudTCOComparison]
) -> str:
    total_benefit = sum(uc.estimated_annual_benefit_thb for uc in use_cases)
    total_cost = sum(uc.implementation_cost_thb for uc in use_cases)
    avg_payback = (total_cost / total_benefit) * 12 if total_benefit > 0 else 0
    three_year_net = (total_benefit * 3) - total_cost

    content = f"""# 📊 Executive Presentation Deck: Data & AI Transformation Strategy
**Client Organization:** {client.name}  
**Consulting Engagement:** data-gov-consultant Virtual AI-Native Practice  
**Date:** 2026-09-12 | Version 2.0 (Comprehensive Boardroom Edition)  
**Security Classification:** Highly Confidential (C-Suite & Board of Directors Only)

---

## Slide 1: Title & Strategic Context
### ยกระดับองค์กรสู่การขับเคลื่อนด้วยข้อมูลและปัญญาประดิษฐ์ (Data-Driven & AI-Native Hospital)
* **บริบทเชิงกลยุทธ์:** ในยุค Value-Based Healthcare และการแข่งขันทางการแพทย์ที่รุนแรง โรงพยาบาลไม่สามารถบริหารงานด้วยสัญชาตญาณหรือรายงานย้อนหลังได้อีกต่อไป
* **พันธกิจหลัก:** เปลี่ยนผ่าน {client.name} จากองค์กรที่ "มีข้อมูลมากแต่ใช้ประโยชน์ไม่ได้" สู่ "ศูนย์กลางการตัดสินใจด้วยข้อมูลแบบเรียลไทม์"
* **หลักการดำเนินงาน:** ยึดมั่นแนวคิด **"Business-First & Right-Sized Technology"** ไม่เน้นซื้อเครื่องมือราคาแพงเกินความจำเป็น แต่เน้นแก้ปัญหาการดำเนินงานจริงและสร้างผลกำไรสุทธิ

---

## Slide 2: Executive Summary & Financial Value Creation
### สรุปความคุ้มค่าทางการเงินและผลกระทบเชิงธุรกิจ
* **ผลตอบแทนทางการเงินสะสม 3 ปี (3-Year Net Cumulative Value):** **{three_year_net/1_000_000:,.1f} ล้านบาท**
* **ผลประโยชน์ทางธุรกิจรายปี (Annual Net Benefit):** **{total_benefit/1_000_000:,.1f} ล้านบาท/ปี**
* **งบประมาณการลงทุนเริ่มแรก (CapEx & Implementation):** **{total_cost/1_000_000:,.1f} ล้านบาท**
* **ระยะเวลาคืนทุนเฉลี่ยของพอร์ตโฟลิโอ (Average Payback Period):** **{avg_payback:.1f} เดือน**
* **ดัชนีชี้วัดความพร้อมธรรมาภิบาลข้อมูล:** ยกระดับจาก **Level {maturity_score}** สู่ **Level 4 (Managed & Quantitatively Controlled)** ภายใน 12 เดือน

---

## Slide 3: Current State Assessment (AS-IS Diagnosis)
### การประเมินสถานะปัจจุบันและระดับวุฒิภาวะ (DGA Maturity Level 2)
* **ระดับวุฒิภาวะปัจจุบัน:** **ระดับที่ {maturity_score} : {maturity_narrative}**
* **ปัญหาคอขวดวิกฤต (Critical Bottlenecks Identified):**
  1. **Master Data Fragmentation:** ข้อมูลคนไข้แยกส่วนระหว่างระบบเวชระเบียน (HIS OPD/IPD), ศูนย์ตรวจสุขภาพ และคลินิกความงาม มี HN ซ้ำซ้อนกว่า 25,000 รายชื่อ
  2. **Clinical Data Trapped in Silos:** ข้อมูลภาพรังสี (PACS) และผลตรวจห้องปฏิบัติการ (LIS) ไม่เชื่อมโยงแบบเรียลไทม์ แพทย์ต้องสลับหน้าจอตรวจหลายระบบ
  3. **Revenue Leakage:** การให้รหัสโรค (ICD-10) และหัตถการทางการแพทย์ไม่ครบถ้วน ทำให้ถูกหักเงินเคลมประกันสุขภาพกว่า 15 ล้านบาท/ปี
  4. **PDPA Regulatory Friction:** บุคลากรขาดความมั่นใจในกฎหมาย PDPA ม.26 ทำให้เกิดความล่าช้าในการนำข้อมูลไปใช้วิเคราะห์วิจัย
  5. **Capacity Bottlenecks:** ผู้ป่วยรอเตียงนานเกิน 6 ชม. และอัตราการใช้งานห้องผ่าตัดเฉลี่ยเพียง 62% สูญเสียโอกาสรายได้มหาศาล

---

## Slide 4: Strategic Priorities: Business-First vs Tool-First
### การวางกรอบความคิดและจัดลำดับความสำคัญ
```
[ แนวทางแบบเก่า (Tool-First - เสี่ยงล้มเหลวสูง) ]
  ซื้อ Software หรูราคาแพง ──> พยายามยัดข้อมูลเข้าไป ──> ขาดคนดูแล ──> กลายเป็นระบบร้าง (Shelfware)

[ แนวทางของ data-gov-consultant (Business-First - คืนทุนจริง) ]
  ระบุปัญหาธุรกิจ & Use Cases ──> ออกแบบ RACI คนหน้างาน ──> ลงทะเบียน Data Catalog ──> ต่อท่อ Cloud Lakehouse
```
* **Bridge Gate Principle:** จะไม่มีการจัดซื้อซอฟต์แวร์หรือสร้างโมเดล AI ใด ๆ จนกว่าจะผ่านการตรวจสอบคุณภาพข้อมูล (Data Quality > 80%) และระบุผู้รับผิดชอบ (Data Steward) ชัดเจน

---

## Slide 5: Top 10 High-Value Use Cases Portfolio
### พอร์ตโฟลิโอ 10 ยูสเคสธุรกิจและการวิเคราะห์จุดคุ้มทุน

| รหัส | โครงการ Use Case ทางธุรกิจ | ฝ่ายงานที่รับผิดชอบ | ผลประโยชน์/ปี (ลบ.) | ต้นทุน (ลบ.) | คืนทุน (เดือน) | ระดับความสำคัญ |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
"""

    for uc in use_cases:
        content += f"| **{uc.id}** | {uc.title} | {uc.business_unit} | **{uc.estimated_annual_benefit_thb/1_000_000:,.2f}** | {uc.implementation_cost_thb/1_000_000:,.2f} | {uc.payback_months:.1f} | `{uc.priority_tier}` |\n"

    content += f"""
* **รวมผลประโยชน์ทั้งสิ้น:** **{total_benefit/1_000_000:,.2f} ล้านบาท/ปี** | **รวมต้นทุน:** **{total_cost/1_000_000:,.2f} ล้านบาท**

---

## Slide 6: Quick Wins (Phase 1) vs Strategic Bets (Phase 2)
### การแบ่งระยะเพื่อสร้างกระแสเงินสดหมุนเวียน (Self-Funding S-Curve)

* **กลุ่มที่ 1: Quick Wins (เริ่มเห็นผลในเดือนที่ 3–6):**
  * **HC-01 (Bed Occupancy & Discharge Analytics):** ลดเวลารอเตียง คืนทุนใน 2.7 เดือน (ผลประโยชน์ 8.5 ลบ./ปี)
  * **HC-02 (Medical Billing & DRG Claims Optimization):** อุดรอยรั่วเบิกเคลมประกัน คืนทุนใน 2.2 เดือน (ผลประโยชน์ 15.0 ลบ./ปี)
  * **HC-03 (Master Patient Index EMPI):** ยุบรวมข้อมูลคนไข้ซ้ำซ้อน คืนทุนใน 2.6 เดือน (ผลประโยชน์ 11.2 ลบ./ปี)
  * **HC-05 (Smart Pharmacy Replenishment):** บริหารคลังยามูลค่าสูง คืนทุนใน 2.5 เดือน (ผลประโยชน์ 7.8 ลบ./ปี)
  * **HC-06 (Outpatient No-Show Predictor):** ลดอัตราเบี้ยวนัดห้องตรวจ คืนทุนใน 3.1 เดือน (ผลประโยชน์ 5.4 ลบ./ปี)
  * **HC-10 (Preventive Wellness CRM):** เพิ่มอัตราคนไข้ตรวจสุขภาพกลับมารักษาต่อยอด คืนทุนใน 2.4 เดือน (ผลประโยชน์ 10.5 ลบ./ปี)
* **กลุ่มที่ 2: Strategic Bets (ต่อยอดขยายผลในเดือนที่ 7–18):**
  * **HC-04 (Clinical AI Research Sandbox):** ปลดล็อกงานวิจัยการแพทย์ตาม PDPA ม.26 (ผลประโยชน์ 6.0 ลบ./ปี)
  * **HC-07 (Operating Theatre Optimizer):** จัดคิวห้องผ่าตัดอัจฉริยะ (ผลประโยชน์ 12.0 ลบ./ปี)
  * **HC-08 (Radiology Triage AI):** คัดกรองภาพสมองฉุกเฉินเวรดึก (ผลประโยชน์ 9.5 ลบ./ปี)
  * **HC-09 (Sepsis Deterioration Alert):** แจ้งเตือนภาวะติดเชื้อในกระแสเลือดล่วงหน้า (ผลประโยชน์ 8.0 ลบ./ปี)

---

## Slide 7: Enterprise Data Governance Operating Model
### โครงสร้างการกำกับดูแลข้อมูล 3 ระดับ (3-Tier Governance Structure)
```
          ┌───────────────────────────────────────────────────────────┐
          │  คณะกรรมการธรรมาภิบาลข้อมูล (Data Governance Council)     │
          │  • ประธาน: ประธานเจ้าหน้าที่บริหาร (CEO) / ผู้อำนวยการ    │
          │  • กรรมการ: CIO/CTO, ผอ.การแพทย์, ผอ.การเงิน, DPO/ฝ่ายกฎหมาย│
          └─────────────────────────────┬─────────────────────────────┘
                                        │ กำกับนโยบาย & อนุมัติงบ
                                        ▼
          ┌───────────────────────────────────────────────────────────┐
          │  หัวหน้าคณะบริกรข้อมูลกลาง (Lead Data Steward)             │
          │  ทำหน้าที่ประสานงานระหว่างฝ่ายธุรกิจและฝ่ายไอที            │
          └──────────────┬─────────────────────────────┬──────────────┘
                         │                             │
                         ▼                             ▼
        ┌──────────────────────────────┐ ┌──────────────────────────────┐
        │ คณะบริกรข้อมูล (Data Stewards) │ │ ผู้ดูแลเทคนิค (Custodians)   │
        │ • บริกรฝ่ายเวชระเบียน         │ │ • วิศวกรข้อมูล (Data Eng)    │
        │ • บริกรฝ่ายเภสัชกรรม          │ │ • ผู้ดูแลระบบฐานข้อมูล (DBA)  │
        │ • บริกรฝ่ายการเงิน/เคลม       │ │ • สถาปนิกคลาวด์ (Cloud Arch) │
        └──────────────────────────────┘ └──────────────────────────────┘
```

---

## Slide 8: 42-Activity RACI Matrix Across 9 Data Lifecycle Domains
### การกำหนดความรับผิดชอบที่โปร่งใส ไร้รอยต่อ
* **ครอบคลุม 9 หมวดวงจรชีวิต:** Planning (4), Create (5), Store (6), Use (6), Publish (5), Archive (2), Destroy (3), Exchange (3), Quality (4), AI Model (5) รวมทั้งสิ้น 42 กิจกรรม
* **Single Point of Accountability:** ทุกกิจกรรมมีผู้รับผิดชอบหลัก **(Accountable - A)** เพียง 1 ตำแหน่งเสมอ ป้องกันปัญหาการโยนความรับผิดชอบ
* **เกณฑ์การมีส่วนร่วมของ DPO:** เจ้าหน้าที่คุ้มครองข้อมูลส่วนบุคคล (DPO) มีบทบาท **Accountable (A)** หรือ **Responsible (R)** ในกิจกรรมที่มีความเสี่ยงด้านสิทธิและข้อมูลอ่อนไหวทางการแพทย์

---

## Slide 9: Modern Data Lakehouse Architecture
### สถาปัตยกรรมทะเลสาบข้อมูล 4 เลเยอร์ (Medallion Architecture)
```
[ Data Sources ]       [ Bronze Layer ]       [ Silver Layer ]       [ Gold Layer / Serving ]
• HIS (OPD/IPD)  ───>  Raw Ingestion    ───>  Conformed & Clean ───>  Business Data Marts
• LIS (Lab Results)    Daily CDC Stream       Deduplicated HN        • BI Dashboards (Power BI)
• PACS (Radiology)     Append-Only            Standardized Code      • Predictive AI Models
• ERP / Billing        Encrypted Bucket       PDPA Tokenized         • Clinical Research API
```
* **Zero Disruption to Transactional Systems:** ดึงข้อมูลผ่าน Change Data Capture (CDC) นอกเวลาเร่งด่วน ไม่ส่งผลกระทบต่อระบบหน้างานของแพทย์และพยาบาล
* **Built-in De-identification Engine:** ตัดชื่อ-นามสกุล และเลขประจำตัว 13 หลักตั้งแต่เข้าสู่ Silver Layer รองรับการนำไปใช้ของทีม Data Science ได้อย่างปลอดภัย

---

## Slide 10: 3-Year Cloud TCO Comparison
### การเปรียบเทียบต้นทุนรวมในการเป็นเจ้าของ (TCO) ระหว่างทางเลือกต่าง ๆ

| ทางเลือกสถาปัตยกรรม | ค่าบริการรายปี (ลบ.) | TCO รวม 3 ปี (ลบ.) | ข้อได้เปรียบเชิงกลยุทธ์ | ข้อจำกัดที่ต้องบริหารจัดการ |
| :--- | :---: | :---: | :--- | :--- |
"""

    for t in tco_list:
        content += f"| **{t.provider}** | {t.annual_total_thb/1_000_000:,.2f} | **{t.three_year_tco_thb/1_000_000:,.2f}** | {t.pros} | {t.cons} |\n"

    content += f"""
* **ข้อเสนอแนะของทีมที่ปรึกษา:** แนะนำเริ่มต้นด้วย **Google Cloud Platform (GCP)** หรือ **Microsoft Azure** เนื่องจากมีระบบ Data Catalog & Access Control ในตัว และไม่ต้องมีงบลงทุนฮาร์ดแวร์ล่วงหน้า (Zero Initial Hardware CapEx)

---

## Slide 11: Enterprise Data Quality Assurance (5 Dimensions)
### กรอบการประกันคุณภาพข้อมูลและเช็กลิสต์ปฏิบัติการ 24 ข้อ

| มิติคุณภาพข้อมูล (สพร.) | นิยามและความสำคัญ | ค่าน้ำหนัก | เป้าหมายขั้นต่ำ | การตรวจวัดและแก้ไข |
| :--- | :--- | :---: | :---: | :--- |
| **1. Accuracy & Completeness** | ความถูกต้องของค่าและไม่มีฟิลด์สำคัญตกหล่น | 25% | >= 95% | ตั้ง UI Validation บนหน้าจอ HIS และเช็ก Mod 11 เลขบัตร |
| **2. Consistency** | ความสอดคล้องของรหัสอ้างอิงและข้ามตาราง | 20% | >= 90% | บังคับใช้ Master Code ยา (TMT) และโรค (ICD-10) |
| **3. Timeliness** | ข้อมูลเป็นปัจจุบันและพร้อมใช้งานตามเวลา | 20% | >= 90% | ปรับ Latency การส่งข้อมูลจากรายเดือนเป็นรายวัน (Daily) |
| **4. Relevancy** | ข้อมูลตรงกับความต้องการใช้งานจริง | 15% | >= 85% | จัดทำ Data Catalog 14 ฟิลด์เพื่อลดความสับสน |
| **5. Availability** | ระบบมีความเสถียรและเรียกใช้ได้ตาม SLA | 20% | >= 99.9% | ทำ High Availability บน Cloud และทดสอบ DR ประจำปี |

* **The Bridge Gate Score:** กำหนดเกณฑ์คุณภาพรวม **>= 80%** สำหรับทุกชุดข้อมูลก่อนอนุญาตให้เชื่อมเข้าโมเดล AI

---

## Slide 12: AI Governance & ISO 42001 Framework
### การกำกับดูแลปัญญาประดิษฐ์ทางการแพทย์อย่างปลอดภัยและมีจริยธรรม
* **ISO/IEC 42001 Standard:** นำกรอบระบบการจัดการปัญญาประดิษฐ์ (AIMS) มาบังคับใช้ทุกโครงการ
* **3-Tier AI Risk Classification:**
  1. **High Risk (AI วินิจฉัยภาพรังสี / แจ้งเตือนวิกฤต):** บังคับใช้กฎ **Human-in-the-Loop** 100% แพทย์ต้องยืนยันผลเสมอ
  2. **Limited Risk (AI ทำนายการผิดนัด / จัดสรรคิวเตียง):** มีระบบบันทึก Audit Log และการตรวจสอบย้อนหลังทุกเดือน
  3. **Minimal Risk (BI Dashboards รายงานผลทั่วไป):** ตรวจสอบความถูกต้องตามรอบปกติ
* **Prompt & LLM Security Firewall:** ติดตั้งเกราะป้องกันข้อมูลรั่วไหล ห้ามบุคลากรคัดลอกประวัติผู้ป่วยลงในเครื่องมือ Public Generative AI

---

## Slide 13: 18-Month Transformation Roadmap & Milestones
### แผนปฏิบัติการเปลี่ยนผ่าน 3 ระยะ

```
[ ระยะที่ 1: เดือน 1–3 (Foundation & Quick Wins) ]
  • ลงนามแต่งตั้งคณะกรรมการธรรมาภิบาลข้อมูล (Council) และบริกรข้อมูล (Stewards)
  • จัดทำ Data Catalog 14 ฟิลด์สำหรับ 12 ชุดข้อมูลสำคัญ
  • นำร่องระบบแก้ปัญหา HN ซ้ำซ้อน (EMPI) และระบบลดเตียงรอ (Bed Occupancy)

[ ระยะที่ 2: เดือน 4–8 (Scaling & Cloud Lakehouse) ]
  • วางระบบ Modern Data Lakehouse บนคลาวด์ พร้อมเชื่อมท่อ Daily CDC
  • เปิดใช้งานระบบ Billing Claims Optimization (สร้างรายได้คืนทุนทันที)
  • ฝึกอบรม Data & AI Literacy ให้บุคลากรทุกระดับ

[ ระยะที่ 3: เดือน 9–18 (AI Modernization & ISO 42001) ]
  • ติดตั้งโมเดลทำนายทางคลินิก (Radiology Triage AI & Sepsis Early-Warning)
  • ขอรับรองมาตรฐานสากล ISO/IEC 42001 สำหรับระบบ AI การแพทย์
  • เปิดตัว Enterprise BI Self-Service ให้ทุกแผนกทำรายงานได้เอง
```

---

## Slide 14: Action Plan & Formal Board Decisions Required Today
### มติที่ขออนุมัติจากคณะกรรมการบริหารในวันนี้

1. **อนุมัติในหลักการ (Approval in Principle):** พิมพ์เขียวแผนแม่บทการเปลี่ยนผ่านสู่องค์กรขับเคลื่อนด้วยข้อมูล (Transformation Master Blueprint) และกรอบงบประมาณสะสม 3 ปี
2. **ลงนามคำสั่งอย่างเป็นทางการ (Formal Appointment):** ลงนามคำสั่งแต่งตั้งคณะกรรมการธรรมาภิบาลข้อมูล (Data Governance Council) และคณะบริกรข้อมูล (Data Steward Team) ตามร่างเอกสารแนบ
3. **อนุมัติโครงการนำร่อง (Pilot Project Authorization):** มอบอำนาจให้ทีมงานเริ่มดำเนินการจัดตั้ง Data Catalog และเชื่อมต่อท่อส่งข้อมูล 3 ชุดข้อมูลสำคัญ (EMPI, Bed Registry, Billing) ภายใน 30 วัน
"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return output_path
