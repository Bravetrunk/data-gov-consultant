"""
Markdown Executive Presentation Deck Builder for data-gov-consultant Platform.
Compiles boardroom slide decks and audit memos.
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

    content = f"""# 📊 Executive Presentation Deck: Data & AI Transformation Strategy
**Client:** {client.name}  
**Engagement Team:** data-gov-consultant Virtual Transformation Practice  
**Date:** 2026-09-12 | Version 1.0 (Boardroom Edition)

---

## Slide 1: Executive Summary & The Imperative for Change
* **Where We Are Today (AS-IS):** ข้อมูลยังกระจัดกระจาย มีระดับวุฒิภาวะอยู่ที่ **ระดับ {maturity_score} ({maturity_narrative})** 
* **The Opportunity:** การปลดล็อกมูลค่าข้อมูลผ่าน 4 Sprints จะสร้างผลตอบแทนสุทธิรวม **{total_benefit/1_000_000:,.1f} ล้านบาท/ปี**
* **The Strategy:** ยึดหลัก **"Business-First & Right-Sized Tech"** ไม่ซื้อเครื่องมือเกินตัว แต่เน้นแก้ปัญหาหน้างานจริง
* **Investment & Payback:** เงินลงทุนเริ่มต้น **{total_cost/1_000_000:,.1f} ล้านบาท** คืนทุนเฉลี่ยภายใน **{avg_payback:.1f} เดือน**

---

## Slide 2: Top Identified Use Cases & Prioritization (2x2 Matrix)

| รหัส | โครงการ Use Case | ฝ่ายที่รับผิดชอบ | ผลประโยชน์/ปี (ลบ.) | ต้นทุน (ลบ.) | คืนทุน (เดือน) | ระดับความสำคัญ |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
"""
    for uc in use_cases:
        content += f"| **{uc.id}** | {uc.title} | {uc.business_unit} | **{uc.estimated_annual_benefit_thb/1_000_000:,.2f}** | {uc.implementation_cost_thb/1_000_000:,.2f} | {uc.payback_months:.1f} | `{uc.priority_tier}` |\n"

    content += f"""
> **💡 Key Takeaway:** โครงการ Quick Wins ในกลุ่ม Tier 1 จะคืนทุนเร็วที่สุดภายใน 3–6 เดือนแรก เพื่อนำกำไรมาหมุนเวียนสนับสนุนระบบในระยะยาว

---

## Slide 3: Data Governance Operating Model & RACI
```
        [ คณะกรรมการธรรมาภิบาลข้อมูล (Data Governance Council) ]
              ├── ประธาน: CEO / ผู้อำนวยการ
              └── กรรมการ: CIO, DPO, ผู้อำนวยการฝ่ายธุรกิจ
                                │
        [ หัวหน้าคณะบริกรข้อมูล (Lead Data Steward) ]
                                │
              ├── คณะบริกรข้อมูลธุรกิจ (Business Data Stewards)
              ├── วิศวกรข้อมูล & ผู้ดูแลระบบ (Data Custodians - IT)
              └── เจ้าหน้าที่คุ้มครองข้อมูลส่วนบุคคล (DPO / Legal)
```
* **RACI Matrix:** กำหนดผู้รับผิดชอบชัดเจนกว่า 40 กิจกรรมตามวงจรชีวิตข้อมูล 6 ขั้นตอน (Create, Store, Use, Publish, Archive, Destroy)
* **Zero Policy Shelfware:** เน้นกระบวนการที่คนหน้างานทำได้จริง ไม่สร้างความล่าช้าในกระบวนการทำงานปกติ

---

## Slide 4: Modern Data Lakehouse Architecture & Cloud TCO
* **สถาปัตยกรรมเป้าหมาย:** จัดตั้ง **Modern Data Lakehouse** เชื่อมโยงระบบ Transactional ต้นทาง (HIS, POS, ERP) ผ่าน Daily CDC สู่ Serving Layer
* **การเปรียบเทียบต้นทุนรวม 3 ปี (3-Year TCO Comparison):**

| ผู้ให้บริการคลาวด์ | ค่าบริการรายปี (ลบ.) | TCO รวม 3 ปี (ลบ.) | ข้อได้เปรียบเชิงกลยุทธ์ |
| :--- | :---: | :---: | :--- |
"""
    for t in tco_list:
        content += f"| **{t.provider}** | {t.annual_total_thb/1_000_000:,.2f} | **{t.three_year_tco_thb/1_000_000:,.2f}** | {t.pros} |\n"

    content += f"""
---

## Slide 5: AI Transformation & Scaling Roadmap (ISO 42001)
```
[ เฟสที่ 1: เดือน 1-3 ] ──> [ เฟสที่ 2: เดือน 4-6 ] ──> [ เฟสที่ 3: เดือน 7-12 ]
  Data Catalog 14 ฟิลด์      Predictive Models        Generative AI & MLOps
  ทำ Data Quality >80%      Automated Discharge        Clinical/Business Copilot
  PDPA Masking Sandbox      Claim Optimization         ISO 42001 Certification
```
* **The Bridge Gate:** จะไม่มีโมเดล AI ใดถูกนำไปใช้งาน หากชุดข้อมูลเทรนยังไม่ผ่านเกณฑ์ Data Quality 80% และผ่านการตัดตัวตน (De-identification) เรียบร้อย
* **Change Management:** จัดอบรม **Data & AI Literacy Curriculum** ให้พนักงานทุกคนเพื่อลดแรงต้านและสร้างวัฒนธรรม Data-Driven

---

## Slide 6: การอนุมัติที่ขอจากคณะกรรมการ (Requested Approvals)
1. **อนุมัติในหลักการ:** พิมพ์เขียวการเปลี่ยนผ่าน (Transformation Master Blueprint) และกรอบงบประมาณ
2. **ลงนามคำสั่ง:** คำสั่งแต่งตั้งคณะกรรมการธรรมาภิบาลข้อมูล (Council) และคณะบริกรข้อมูล (Steward Team)
3. **มอบอำนาจดำเนินการ:** อนุญาตให้ทีมงานเริ่มจัดทำ Pilot Data Catalog สำหรับ 3 ชุดข้อมูลสำคัญทันที
"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    return output_path
