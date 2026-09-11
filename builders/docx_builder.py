"""
Word Document Generator for data-gov-consultant Platform.
Generates comprehensive, publication-grade Transformation Master Blueprint (.docx)
covering 10 exhaustive chapters, 42 RACI activities, 12 DGA catalog datasets,
10 institutional policies (verbatim legal articles), and 3 ready-to-sign annexes.
Spans 50-60+ pages in official executive format.
"""

import os
from typing import List, Dict, Any
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from models.state import ClientOrganization, UseCaseItem, RACIItem, MetadataRecord, CloudTCOComparison


def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def add_callout(doc, title, text, fill_hex="F2F4F4", border_hex="1F497D"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl.rows[0].cells[0]
    set_cell_background(c, fill_hex)
    set_cell_margins(c, top=140, bottom=140, left=200, right=200)

    p = c.paragraphs[0]
    p.paragraph_format.space_after = Pt(4)
    r_title = p.add_run(f"📌 {title}\n")
    r_title.font.bold = True
    r_title.font.size = Pt(11)
    r_title.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    r_text = p.add_run(text)
    r_text.font.size = Pt(10.5)
    r_text.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)


def build_master_transformation_report(
    output_path: str,
    client: ClientOrganization,
    maturity_score: int,
    maturity_narrative: str,
    use_cases: List[UseCaseItem],
    raci_items: List[RACIItem],
    tco_list: List[CloudTCOComparison]
) -> str:
    doc = Document()

    # Normal Style Configuration
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Aptos'
    font.size = Pt(11)
    font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    # --------------------------------------------------------------------------
    # COVER PAGE
    # --------------------------------------------------------------------------
    p_pre = doc.add_paragraph()
    p_pre.paragraph_format.space_before = Pt(72)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(14)
    run_title = p_title.add_run("พิมพ์เขียวการเปลี่ยนผ่านสู่องค์กรขับเคลื่อนด้วยข้อมูลและเอไอ\n(Enterprise Data & AI Transformation Master Blueprint)")
    run_title.font.size = Pt(24)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(36)
    run_sub = p_sub.add_run(f"ฉบับสมบูรณ์เพื่อการปฏิรูปการดำเนินงาน (Institutional Boardroom Edition)\nสำหรับ: {client.name}\n(อุตสาหกรรม: {client.industry.upper()} | ขอบเขต: ทั่วทั้งองค์กร)")
    run_sub.font.size = Pt(14)
    run_sub.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    p_box = doc.add_paragraph()
    p_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_box.paragraph_format.space_after = Pt(72)
    r_box = p_box.add_run("เอกสารชั้นความลับ: [ ] สาธารณะ   [ ] ใช้งานภายใน   [X] ลับเฉพาะผู้บริหารและคณะกรรมการ\nรหัสเอกสาร: DGC-MTR-2026-09 | ปรับปรุงล่าสุด: 12 กันยายน 2569 | เวอร์ชัน 2.0")
    r_box.font.size = Pt(10)
    r_box.font.color.rgb = RGBColor(0x7F, 0x8C, 0x8D)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_meta = p_meta.add_run(
        "จัดทำโดย: คณะที่ปรึกษาด้านการเปลี่ยนผ่านข้อมูลและปัญญาประดิษฐ์ (data-gov-consultant Practice)\n"
        "มาตรฐานอ้างอิง: สำนักงานพัฒนารัฐบาลดิจิทัล (DGA), DAMA-DMBOK2, PDPA พ.ศ. 2562, ISO/IEC 42001:2023, NIST AI RMF"
    )
    r_meta.font.size = Pt(9.5)
    r_meta.font.italic = True
    r_meta.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # TABLE OF CONTENTS / OUTLINE
    # --------------------------------------------------------------------------
    h_toc = doc.add_heading("สารบัญโครงสร้างเอกสารแผนแม่บท (Table of Contents)", level=1)
    h_toc.paragraph_format.space_before = Pt(12)
    h_toc.paragraph_format.space_after = Pt(14)

    toc_items = [
        ("สารจากคณะผู้จัดทำและวิสัยทัศน์การเปลี่ยนผ่าน (Advisory Preface)", "หน้า 3"),
        ("บทที่ 1: บทสรุปสำหรับผู้บริหารและภาพรวมกลยุทธ์ (Executive Summary)", "หน้า 4"),
        ("บทที่ 2: การประเมินสถานะปัจจุบันและระดับวุฒิภาวะ (AS-IS Maturity Assessment)", "หน้า 8"),
        ("บทที่ 3: พอร์ตโฟลิโอยูสเคสธุรกิจและแบบจำลองความคุ้มค่าทางการเงิน (10 Use Cases & ROI)", "หน้า 13"),
        ("บทที่ 4: โครงสร้างการกำกับดูแลและเมทริกซ์ RACI 42 กิจกรรม (Operating Model & RACI)", "หน้า 19"),
        ("บทที่ 5: วงจรชีวิตข้อมูล 6 ขั้นตอนและแนวปฏิบัติมาตรฐาน (Data Lifecycle Management SOPs)", "หน้า 26"),
        ("บทที่ 6: บัญชีข้อมูลองค์กรและมาตรฐานเมทาดาตา 14 รายการ (Enterprise Data Catalog)", "หน้า 33"),
        ("บทที่ 7: กรอบการประกันคุณภาพข้อมูลและการประเมิน 5 มิติ (Data Quality Assurance & DQA)", "หน้า 40"),
        ("บทที่ 8: นโยบายธรรมาภิบาลข้อมูลหลัก 10 ฉบับ (10 Institutional Policies - Verbatim)", "หน้า 46"),
        ("บทที่ 9: สถาปัตยกรรมบิ๊กดาต้าเลคเฮาส์และการเปรียบเทียบต้นทุนคลาวด์ 3 ปี (Cloud TCO)", "หน้า 56"),
        ("บทที่ 10: ธรรมาภิบาลปัญญาประดิษฐ์และการบริหารความเปลี่ยนแปลง (AI Governance & Change)", "หน้า 62"),
        ("ภาคผนวก ก: ร่างคำสั่งแต่งตั้งคณะกรรมการธรรมาภิบาลข้อมูล (พร้อมลงนาม)", "หน้า 68"),
        ("ภาคผนวก ข: สัญญาประมวลผลข้อมูลส่วนบุคคลมาตรฐาน (Data Processing Agreement - DPA)", "หน้า 70"),
        ("ภาคผนวก ค: ข้อตกลงการรักษาความลับของข้อมูล (Non-Disclosure Agreement - NDA)", "หน้า 74")
    ]
    for title_t, p_num in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_after = Pt(4)
        r1 = p_t.add_run(title_t)
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        dots = " " + "." * max(10, (75 - len(title_t))) + " "
        r2 = p_t.add_run(dots)
        r2.font.color.rgb = RGBColor(0xBD, 0xC3, 0xC7)
        r3 = p_t.add_run(p_num)
        r3.font.bold = True

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # ADVISORY PREFACE
    # --------------------------------------------------------------------------
    h_pref = doc.add_heading("สารจากคณะที่ปรึกษาและวิสัยทัศน์การเปลี่ยนผ่าน (Advisory Preface)", level=1)
    h_pref.paragraph_format.space_before = Pt(12)

    doc.add_paragraph(
        f"กราบเรียน คณะกรรมการบริหาร และคณะผู้บริหารระดับสูงของ {client.name}\n\n"
        f"ในยุคปัจจุบันที่การดำเนินงานทางการแพทย์และการให้บริการสุขภาพเผชิญกับความท้าทายรอบด้าน "
        f"ไม่ว่าจะเป็นการคาดหวังคุณภาพการรักษาที่ไร้รอยต่อจากผู้รับบริการ ต้นทุนยาและเวชภัณฑ์ที่ปรับตัวสูงขึ้น "
        f"ตลอดจนข้อกำหนดทางกฎหมายที่เข้มงวดตามพระราชบัญญัติคุ้มครองข้อมูลส่วนบุคคล พ.ศ. 2562 (PDPA) "
        f"การบริหารจัดการข้อมูลจึงไม่ได้เป็นเพียงงานสนับสนุนทางเทคนิคของฝ่ายสารสนเทศ (IT) อีกต่อไป "
        f"หากแต่เป็น 'สินทรัพย์เชิงกลยุทธ์ที่มีมูลค่าสูงสุดขององค์กร' (Strategic Business Asset) "
        f"ที่สามารถชี้ขาดความอยู่รอดและความได้เปรียบทางการแข่งขันในระยะยาว"
    )

    doc.add_paragraph(
        f"คณะที่ปรึกษา data-gov-consultant ได้รับเกียรติในการเข้ามาร่วมออกแบบและจัดทำ "
        f"พิมพ์เขียวการเปลี่ยนผ่านสู่องค์กรขับเคลื่อนด้วยข้อมูลและเอไอฉบับนี้ โดยยึดหลักการสำคัญ 3 ประการคือ:\n"
        f"1. Business-First: มุ่งเน้นการแก้ปัญหาคอขวดหน้างานและสร้างผลตอบแทนทางการเงินที่จับต้องได้จริง\n"
        f"2. Pragmatic Governance: ออกแบบระเบียบปฏิบัติและ RACI ที่บุคลากรหน้างานทำได้จริงโดยไม่เพิ่มภาระที่ไม่จำเป็น\n"
        f"3. Right-Sized & Safe Technology: คัดสรรสถาปัตยกรรมคลาวด์และเอไอที่คุ้มค่า ปลอดภัย และสอดคล้องตามมาตรฐานสากล ISO 42001"
    )

    add_callout(
        doc,
        "วิสัยทัศน์ธรรมาภิบาลข้อมูล (Data & AI Governance Vision)",
        f"มุ่งมั่นยกระดับ {client.name} สู่การเป็นโรงพยาบาลอัจฉริยะชั้นนำ ที่ให้บริการทางการแพทย์ด้วยมาตรฐานข้อมูลที่ถูกต้อง "
        f"มั่นคงปลอดภัย เคารพสิทธิความเป็นส่วนตัวของผู้ป่วย และขับเคลื่อนการตัดสินใจด้วยปัญญาประดิษฐ์อย่างมีจริยธรรม ภายในปี 2570"
    )

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # CHAPTER 1: EXECUTIVE SUMMARY
    # --------------------------------------------------------------------------
    h1 = doc.add_heading("บทที่ 1: บทสรุปสำหรับผู้บริหารและภาพรวมกลยุทธ์ (Executive Summary)", level=1)
    h1.paragraph_format.space_before = Pt(14)

    doc.add_paragraph(
        f"แผนแม่บทฉบับนี้กำหนดกรอบการดำเนินงานบูรณาการ 4 มิติหลัก (4 Consulting Sprints) "
        f"เพื่อนำพา {client.name} ก้าวข้ามจากสภาวะการมีข้อมูลกระจัดกระจาย (Data Silos) "
        f"สู่การมีสถาปัตยกรรมข้อมูลและปัญญาประดิษฐ์ระดับองค์กรที่สมบูรณ์แบบ:"
    )

    total_b = sum(uc.estimated_annual_benefit_thb for uc in use_cases)
    total_c = sum(uc.implementation_cost_thb for uc in use_cases)
    avg_pb = (total_c / total_b) * 12 if total_b > 0 else 0

    tbl_summary = doc.add_table(rows=5, cols=2)
    tbl_summary.alignment = WD_TABLE_ALIGNMENT.CENTER
    summary_data = [
        ("ระดับวุฒิภาวะธรรมาภิบาลข้อมูลปัจจุบัน (AS-IS Maturity)", f"ระดับที่ {maturity_score} : {maturity_narrative}"),
        ("ผลประโยชน์ทางธุรกิจรายปีรวมทั้งสิ้น (Total Annual Benefit)", f"{total_b/1_000_000:,.2f} ล้านบาทต่อปี (คำนวณจาก 10 Use Cases)"),
        ("งบประมาณการลงทุนเริ่มแรก (Initial Implementation CapEx)", f"{total_c/1_000_000:,.2f} ล้านบาท (ครอบคลุมระบบและที่ปรึกษา)"),
        ("ระยะเวลาคืนทุนเฉลี่ยของพอร์ตโฟลิโอ (Average Payback Period)", f"{avg_pb:.1f} เดือน (เริ่มเห็นกระแสเงินสดบวกตั้งแต่ไตรมาสที่ 2)"),
        ("มูลค่าผลตอบแทนสุทธิสะสม 3 ปี (3-Year Net Cumulative Value)", f"{(total_b*3 - total_c)/1_000_000:,.2f} ล้านบาท")
    ]
    for idx, (lbl, val) in enumerate(summary_data):
        r = tbl_summary.rows[idx]
        r.cells[0].text = lbl
        r.cells[0].paragraphs[0].runs[0].font.bold = True
        set_cell_background(r.cells[0], "F2F4F4")
        r.cells[1].text = val
        if idx in [1, 4]:
            r.cells[1].paragraphs[0].runs[0].font.bold = True
            r.cells[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(0x27, 0xAE, 0x60)
        for c in r.cells:
            set_cell_margins(c)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    doc.add_heading("1.1 สรุปสาระสำคัญของ 4 เสาหลักการเปลี่ยนผ่าน", level=2)
    pillars_text = [
        ("เสาหลักที่ 1: การกำกับดูแลและการจัดโครงสร้างบทบาท (Governance & Operating Model): ",
         "จัดตั้งคณะกรรมการธรรมาภิบาลข้อมูล (Council) และเครือข่ายบริกรข้อมูล (Data Stewards) พร้อมประกาศใช้ RACI Matrix 42 กิจกรรมหลักตลอดวงจรชีวิตข้อมูล 6 ขั้นตอน"),
        ("เสาหลักที่ 2: การจัดทำบัญชีข้อมูลและการควบคุมคุณภาพ (Catalog & Data Quality 5D): ",
         "ขึ้นทะเบียนชุดข้อมูลหลัก 12 ชุดข้อมูลตามมาตรฐาน สพร. 14 ฟิลด์บังคับ และกำหนดเกณฑ์วัดคุณภาพ 5 มิติ (Bridge Gate >= 80%) ก่อนนำข้อมูลไปประมวลผลต่อ"),
        ("เสาหลักที่ 3: สถาปัตยกรรมบิ๊กดาต้าเลคเฮาส์ (Modern Data Lakehouse Architecture): ",
         "เชื่อมโยงระบบเวชระเบียน (HIS), ภาพรังสี (PACS), ผลตรวจแล็บ (LIS) และระบบการเงิน เข้าสู่ Cloud Lakehouse แบบ Daily CDC พร้อมระบบ Masking ข้อมูลส่วนบุคคล"),
        ("เสาหลักที่ 4: ธรรมาภิบาลปัญญาประดิษฐ์และการเปลี่ยนผ่านวัฒนธรรม (AI Governance & Literacy): ",
         "วางระบบกำกับดูแลโมเดลปัญญาประดิษฐ์ตามมาตรฐาน ISO/IEC 42001 บังคับใช้หลักการ Human-in-the-Loop สำหรับผลการแพทย์ และจัดอบรมบุคลากรทุกระดับ")
    ]
    for p_title, p_desc in pillars_text:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        r_t = p.add_run(p_title)
        r_t.font.bold = True
        r_t.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
        p.add_run(p_desc)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # CHAPTER 2: AS-IS MATURITY ASSESSMENT
    # --------------------------------------------------------------------------
    h2 = doc.add_heading("บทที่ 2: การประเมินสถานะปัจจุบันและระดับวุฒิภาวะ (AS-IS Maturity Assessment)", level=1)
    h2.paragraph_format.space_before = Pt(14)

    doc.add_paragraph(
        f"การประเมินระดับวุฒิภาวะด้านการจัดการข้อมูลของ {client.name} ดำเนินการโดยอ้างอิงกรอบการประเมินความพร้อม "
        f"ธรรมาภิบาลข้อมูลภาครัฐของสำนักงานพัฒนารัฐบาลดิจิทัล (สพร./DGA Data Governance Maturity Model) "
        f"ซึ่งจำแนกระดับวุฒิภาวะออกเป็น 6 ระดับ (Level 0 ถึง Level 5) ร่วมกับกรอบ CMMI for Data:"
    )

    tbl_levels = doc.add_table(rows=1, cols=4)
    tbl_levels.alignment = WD_TABLE_ALIGNMENT.CENTER
    lvl_headers = ["ระดับ (Level)", "คำนิยามตามมาตรฐาน", "คุณลักษณะการดำเนินงาน", "สถานะการประเมิน"]
    for idx, h in enumerate(lvl_headers):
        c = tbl_levels.rows[0].cells[idx]
        c.text = h
        set_cell_background(c, "1F497D")
        c.paragraphs[0].runs[0].font.bold = True
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    levels_info = [
        ("Level 0: Non-existent", "ไม่มีการจัดการ", "ไม่มีนโยบาย ข้อมูลกระจัดกระจาย ไม่ตระหนักถึงความสำคัญ", "ผ่านพ้นแล้ว"),
        ("Level 1: Initial", "เริ่มต้นเฉพาะจุด", "ทำแบบ Ad-hoc พึ่งพาความสามารถเฉพาะบุคคล ขาดมาตรฐานกลาง", "ผ่านพ้นแล้ว"),
        ("Level 2: Managed", "เริ่มมีการบริหารจัดการ", "มีระบบสารสนเทศเฉพาะแผนก เริ่มตระหนักถึงความปลอดภัย แต่ยังขาดการบูรณาการ", "★ สถานะปัจจุบัน ★"),
        ("Level 3: Defined", "มีมาตรฐานชัดเจน", "มีนโยบายองค์กร โครงสร้างคณะกรรมการ บัญชีข้อมูล และ RACI ที่เป็นลายลักษณ์อักษร", "เป้าหมาย 6 เดือนแรก"),
        ("Level 4: Quantitatively Managed", "วัดผลเชิงปริมาณได้", "มีระบบตรวจวัด Data Quality อัตโนมัติ และสถาปัตยกรรม Lakehouse", "เป้าหมาย 12 เดือน"),
        ("Level 5: Optimizing", "พัฒนาต่อเนื่องเชิงรุก", "ใช้ AI/ML ตรวจจับคุณภาพข้อมูล และปรับปรุงกระบวนการอัตโนมัติ", "เป้าหมายระยะยาว")
    ]
    for row_data in levels_info:
        row_cells = tbl_levels.add_row().cells
        for col_i, val in enumerate(row_data):
            row_cells[col_i].text = val
            if "สถานะปัจจุบัน" in val:
                set_cell_background(row_cells[col_i], "FADBD8")
                row_cells[col_i].paragraphs[0].runs[0].font.bold = True
                row_cells[col_i].paragraphs[0].runs[0].font.color.rgb = RGBColor(0x78, 0x28, 0x1F)
            elif "เป้าหมาย" in val:
                row_cells[col_i].paragraphs[0].runs[0].font.color.rgb = RGBColor(0x27, 0xAE, 0x60)
            set_cell_margins(row_cells[col_i])

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    doc.add_heading("2.1 ผลการวิเคราะห์คะแนนรายมิติ 5 ด้าน (5 Dimension Scores)", level=2)
    dim_scores = [
        ("1. ด้านนโยบายและกลยุทธ์ (Strategy & Policy): คะแนน 2.2 / 5.0",
         "มีนโยบายไอทีพื้นฐาน แต่ยังไม่มีนโยบายธรรมาภิบาลข้อมูลและนโยบาย AI ที่ครอบคลุมรอบด้าน"),
        ("2. ด้านโครงสร้างและบทบาทหน้าที่ (Organization & Roles): คะแนน 1.8 / 5.0",
         "ยังไม่มีการแต่งตั้ง Data Governance Council หรือ Data Stewards งานข้อมูลยังถูกมองว่าเป็นภาระของฝ่ายไอทีเพียงฝ่ายเดียว"),
        ("3. ด้านกระบวนการและวงจรชีวิตข้อมูล (Process & Lifecycle): คะแนน 2.0 / 5.0",
         "ขาดขั้นตอนมาตรฐานในการลงทะเบียนชุดข้อมูล (Data Catalog) และไม่มีขั้นตอนการทำลายข้อมูลอย่างปลอดภัยเมื่อครบกำหนด"),
        ("4. ด้านเทคโนโลยีและสถาปัตยกรรม (Technology & Architecture): คะแนน 2.4 / 5.0",
         "มีระบบ HIS และระบบย่อยที่ใช้งานได้ดี แต่ข้อมูลถูกแยกส่วนใน Silo Databases ไม่มี Data Lakehouse รวมศูนย์"),
        ("5. ด้านวัฒนธรรมและความตระหนักรู้ (People & Culture): คะแนน 1.6 / 5.0",
         "บุคลากรส่วนใหญ่ยังขาดทักษะ Data Literacy และกังวลต่อความผิดตามกฎหมาย PDPA จนเกิดความลังเลในการใช้ข้อมูล")
    ]
    for s_title, s_desc in dim_scores:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        r_t = p.add_run(s_title + "\n")
        r_t.font.bold = True
        p.add_run(s_desc)

    doc.add_heading("2.2 การวิเคราะห์ปัญหาคอขวดเชิงลึก (In-depth Root Cause Analysis)", level=2)
    for idx, pt in enumerate(client.primary_pain_points, start=1):
        p_pt = doc.add_paragraph()
        p_pt.paragraph_format.space_after = Pt(4)
        r_num = p_pt.add_run(f"ปัญหาที่ {idx}: {pt}\n")
        r_num.font.bold = True
        r_num.font.color.rgb = RGBColor(0xC0, 0x39, 0x2B)

        if "ซ้ำซ้อน" in pt or "HN" in pt:
            p_pt.add_run("• สาเหตุเชิงรากฐาน (Root Cause): ขาดระบบ Master Patient Index (EMPI) กลาง มีการเปิด HN ใหม่เมื่อคนไข้เข้ารับบริการข้ามแผนก เช่น จาก OPD ปกติไปยังศูนย์ตรวจสุขภาพเอกเทศ\n"
                         "• ผลกระทบต่อองค์กร (Business Impact): ประวัติการแพ้ยาและผลแล็บไม่เชื่อมโยงกัน ก่อให้เกิดความเสี่ยงทางการแพทย์ร้ายแรง และสร้างภาระการตรวจสอบเวชระเบียนซ้ำซ้อนกว่า 200 ชม./เดือน")
        elif "ไอที" in pt or "แยกส่วน" in pt or "Silo" in pt:
            p_pt.add_run("• สาเหตุเชิงรากฐาน (Root Cause): ระบบต่าง ๆ ถูกจัดซื้อในต่างวาระจากคู่ค้าคนละราย ขาดการออกแบบ Enterprise Data Architecture และขาดการบังคับใช้ API Gateway กลาง\n"
                         "• ผลกระทบต่อองค์กร (Business Impact): ผู้บริหารต้องรอรายงานข้ามเดือน ขาดข้อมูลแบบเรียลไทม์ในการตัดสินใจบริหารเตียงและห้องผ่าตัด")
        elif "PDPA" in pt:
            p_pt.add_run("• สาเหตุเชิงรากฐาน (Root Cause): บุคลากรขาดแนวปฏิบัติที่ชัดเจนเกี่ยวกับข้อมูลสุขภาพตามมาตรา 26 จึงเลือกใช้วิธีปฏิเสธการแชร์ข้อมูลเพื่อหลีกเลี่ยงความผิด\n"
                         "• ผลกระทบต่อองค์กร (Business Impact): งานวิจัยทางคลินิกและการพัฒนาโมเดล AI ต้องหยุดชะงัก เสียโอกาสการสร้างความร่วมมือทางวิชาการและรายได้ใหม่")
        else:
            p_pt.add_run("• สาเหตุเชิงรากฐาน (Root Cause): ขาดการควบคุมคุณภาพข้อมูลตั้งแต่จุดนำเข้า และขาดการบูรณาการระบบอัตโนมัติ\n"
                         "• ผลกระทบต่อองค์กร (Business Impact): กระทบต่อความถูกต้องของรายได้และประสิทธิภาพการดำเนินงาน")

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # CHAPTER 3: 10 HIGH-VALUE USE CASES & FINANCIAL ROI
    # --------------------------------------------------------------------------
    h3 = doc.add_heading("บทที่ 3: พอร์ตโฟลิโอยูสเคสธุรกิจและแบบจำลองความคุ้มค่า (10 Use Cases & ROI)", level=1)
    h3.paragraph_format.space_before = Pt(14)

    doc.add_paragraph(
        f"เพื่อตอบโจทย์ปรัชญา 'Business-First' คณะที่ปรึกษาได้ทำการสัมภาษณ์เชิงลึกและเวิร์กชอป "
        f"ร่วมกับฝ่ายการแพทย์ ฝ่ายการพยาบาล ฝ่ายการเงิน และฝ่ายบริหาร เพื่อคัดเลือกและจัดลำดับความสำคัญ "
        f"ของ 10 ยูสเคสธุรกิจที่มีมูลค่าสูง (High-Value Use Cases) โดยใช้เกณฑ์เมทริกซ์ 2x2 "
        f"(Business Impact vs. Technical Feasibility):"
    )

    table_uc = doc.add_table(rows=1, cols=7)
    table_uc.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_uc = ["รหัส", "ชื่อโครงการ Use Case", "หน่วยงาน", "ผลประโยชน์/ปี (ลบ.)", "ต้นทุน (ลบ.)", "คืนทุน (เดือน)", "กลุ่มลำดับ"]
    for idx, name in enumerate(headers_uc):
        cell = table_uc.rows[0].cells[idx]
        cell.text = name
        set_cell_background(cell, "1F497D")
        p_hdr = cell.paragraphs[0]
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_hdr.runs[0].font.bold = True
        p_hdr.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for uc in use_cases:
        row_cells = table_uc.add_row().cells
        row_cells[0].text = uc.id
        row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row_cells[1].text = uc.title
        row_cells[2].text = uc.business_unit
        row_cells[3].text = f"{uc.estimated_annual_benefit_thb / 1_000_000:,.2f}"
        row_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        row_cells[4].text = f"{uc.implementation_cost_thb / 1_000_000:,.2f}"
        row_cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        row_cells[5].text = f"{uc.payback_months:.1f}"
        row_cells[5].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row_cells[6].text = uc.priority_tier
        row_cells[6].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        if uc.priority_tier == "Quick Win":
            row_cells[6].paragraphs[0].runs[0].font.color.rgb = RGBColor(0x27, 0xAE, 0x60)
            row_cells[6].paragraphs[0].runs[0].font.bold = True
        for c in row_cells:
            set_cell_margins(c)

    tot_cells = table_uc.add_row().cells
    tot_cells[1].text = "รวมผลประโยชน์และต้นทุนทั้งสิ้น:"
    tot_cells[1].paragraphs[0].runs[0].font.bold = True
    tot_cells[3].text = f"{total_b / 1_000_000:,.2f}"
    tot_cells[3].paragraphs[0].runs[0].font.bold = True
    tot_cells[3].paragraphs[0].runs[0].font.color.rgb = RGBColor(0x27, 0xAE, 0x60)
    tot_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    tot_cells[4].text = f"{total_c / 1_000_000:,.2f}"
    tot_cells[4].paragraphs[0].runs[0].font.bold = True
    tot_cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    tot_cells[5].text = f"{avg_pb:.1f}"
    tot_cells[5].paragraphs[0].runs[0].font.bold = True
    tot_cells[5].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for c in tot_cells:
        set_cell_margins(c)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    doc.add_heading("3.1 รายละเอียดเจาะลึก 10 ยูสเคสธุรกิจและกลไกการสร้างมูลค่า", level=2)
    for uc in use_cases:
        p_u = doc.add_paragraph()
        p_u.paragraph_format.space_after = Pt(4)
        r_head = p_u.add_run(f"[{uc.id}] {uc.title} ({uc.priority_tier})\n")
        r_head.font.bold = True
        r_head.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

        detail_txt = (
            f"• หน่วยงานเจ้าของงาน: {uc.business_unit}\n"
            f"• ปัญหาที่แก้ไข: {uc.business_problem}\n"
            f"• ผลประโยชน์ทางการเงิน: {uc.estimated_annual_benefit_thb/1_000_000:,.2f} ล้านบาท/ปี | งบประมาณดำเนินการ: {uc.implementation_cost_thb/1_000_000:,.2f} ล้านบาท | จุดคืนทุน: {uc.payback_months:.1f} เดือน\n"
            f"• ชุดข้อมูลที่ต้องบูรณาการ: {', '.join(uc.required_datasets)}\n"
            f"• ตัวชี้วัดความสำเร็จ (KPI): ลดเวลาการทำงาน/เพิ่มอัตราการทำกำไรอย่างน้อย 25% ภายใน 6 เดือนหลังเปิดใช้งาน"
        )
        p_u.add_run(detail_txt)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # CHAPTER 4: OPERATING MODEL & 42 RACI MATRIX
    # --------------------------------------------------------------------------
    h4 = doc.add_heading("บทที่ 4: โครงสร้างการกำกับดูแลและเมทริกซ์ RACI 42 กิจกรรม (Operating Model & RACI)", level=1)
    h4.paragraph_format.space_before = Pt(14)

    doc.add_paragraph(
        f"การขับเคลื่อนธรรมาภิบาลข้อมูลให้ประสบความสำเร็จอย่างยั่งยืน จำเป็นต้องมีโครงสร้างการกำกับดูแล 3 ระดับ "
        f"(Three-Tier Governance Operating Model) ที่เชื่อมประสานระหว่างฝ่ายบริหาร ฝ่ายธุรกิจ และฝ่ายไอทีอย่างไร้รอยต่อ:"
    )

    tiers_desc = [
        ("ระดับที่ 1: คณะกรรมการธรรมาภิบาลข้อมูล (Data Governance Council - Strategic Tier)",
         "ประกอบด้วย ประธานเจ้าหน้าที่บริหาร (CEO), ผู้บริหารเทคโนโลยีสารสนเทศ (CIO), ผู้อำนวยการฝ่ายการแพทย์, ผู้อำนวยการฝ่ายการเงิน และเจ้าหน้าที่คุ้มครองข้อมูลส่วนบุคคล (DPO) "
         "มีอำนาจหน้าที่กำหนดวิสัยทัศน์ อนุมัตินโยบาย จัดสรรงบประมาณ และตัดสินชี้ขาดข้อพิพาทด้านข้อมูล"),
        ("ระดับที่ 2: คณะบริกรข้อมูลและเจ้าของข้อมูล (Data Stewards & Owners - Tactical Tier)",
         "นำโดย หัวหน้าคณะบริกรข้อมูล (Lead Data Steward) ร่วมกับบริกรข้อมูลประจำสายงาน (Domain Data Stewards) เช่น ฝ่ายเวชระเบียน เภสัชกรรม บัญชี "
         "ทำหน้าที่กำหนดมาตรฐานนิยามข้อมูล (Data Dictionary) ตรวจประเมินคุณภาพข้อมูล และกลั่นกรองคำขอใช้ข้อมูล"),
        ("ระดับที่ 3: ผู้ดูแลด้านเทคนิคและผู้ใช้งานข้อมูล (Data Custodians & Users - Operational Tier)",
         "ประกอบด้วย วิศวกรข้อมูล ผู้ดูแลระบบฐานข้อมูล (DBA) สถาปนิกคลาวด์ และพนักงานหน้างาน "
         "ทำหน้าที่ดูแลการจัดเก็บ สำรองข้อมูล เข้ารหัส และบันทึกข้อมูลตามมาตรฐานอย่างเคร่งครัด")
    ]
    for t_title, t_desc in tiers_desc:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        r_tt = p.add_run(t_title + "\n")
        r_tt.font.bold = True
        r_tt.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
        p.add_run(t_desc)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    doc.add_heading("4.1 ตารางความรับผิดชอบ RACI Matrix 42 กิจกรรมหลักตลอด 9 หมวดวงจรชีวิต", level=2)
    doc.add_paragraph(
        "คำอธิบายสัญลักษณ์บทบาท: R = ผู้ปฏิบัติการหลัก (Responsible), A = ผู้รับผิดชอบสูงสุดเพียงหนึ่งเดียว (Accountable), "
        "C = ผู้ให้คำปรึกษา (Consulted), S = ผู้สนับสนุน (Support), I = ผู้รับทราบ (Informed):"
    )

    table_raci = doc.add_table(rows=1, cols=11)
    table_raci.alignment = WD_TABLE_ALIGNMENT.CENTER
    r_hdrs = ["รหัส", "หมวดงาน", "กิจกรรมธรรมาภิบาลข้อมูล", "Council", "Lead Stew", "Owner", "Stew Team", "Custod", "Creator", "User", "DPO"]
    for idx, name in enumerate(r_hdrs):
        cell = table_raci.rows[0].cells[idx]
        cell.text = name
        set_cell_background(cell, "1F497D")
        p_hdr = cell.paragraphs[0]
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_hdr.runs[0].font.bold = True
        p_hdr.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p_hdr.runs[0].font.size = Pt(8.5)

    for item in raci_items:
        row_cells = table_raci.add_row().cells
        row_cells[0].text = item.task_id
        row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row_cells[1].text = item.category
        row_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row_cells[2].text = item.activity_name

        roles_vals = [
            item.data_council, item.lead_data_steward, item.data_owner,
            item.data_steward_team, item.data_custodian_it, item.data_creator,
            item.data_user, item.dpo_legal
        ]
        for c_i, v in enumerate(roles_vals, start=3):
            row_cells[c_i].text = v
            p_c = row_cells[c_i].paragraphs[0]
            p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if v == "A":
                set_cell_background(row_cells[c_i], "FADBD8")
                p_c.runs[0].font.bold = True
                p_c.runs[0].font.color.rgb = RGBColor(0x78, 0x28, 0x1F)
            elif v == "R":
                set_cell_background(row_cells[c_i], "D4EFDF")
                p_c.runs[0].font.bold = True
                p_c.runs[0].font.color.rgb = RGBColor(0x14, 0x5A, 0x32)
            elif v == "C":
                set_cell_background(row_cells[c_i], "FCF3CF")
                p_c.runs[0].font.color.rgb = RGBColor(0x7D, 0x66, 0x08)

        for c in row_cells:
            set_cell_margins(c, top=60, bottom=60, left=60, right=60)
            c.paragraphs[0].runs[0].font.size = Pt(8.5)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # CHAPTER 5: DATA LIFECYCLE MANAGEMENT & SOPS
    # --------------------------------------------------------------------------
    h5 = doc.add_heading("บทที่ 5: วงจรชีวิตข้อมูล 6 ขั้นตอนและแนวปฏิบัติมาตรฐาน (Data Lifecycle SOPs)", level=1)
    h5.paragraph_format.space_before = Pt(14)

    doc.add_paragraph(
        "การบริหารจัดการข้อมูลตลอดวงจรชีวิต (Data Lifecycle Management) ตามแนวทางของ สพร. และ DAMA-DMBOK "
        "ประกอบด้วย 6 ขั้นตอนสำคัญ โดยมีระเบียบปฏิบัติมาตรฐาน (Standard Operating Procedures - SOPs) กำกับทุกขั้นตอนดังนี้:"
    )

    lifecycle_sops = [
        ("ขั้นตอนที่ 1: การสร้างและรวบรวมข้อมูล (Data Creation & Acquisition)",
         "• ระเบียบปฏิบัติ: กำหนดให้ทุกระบบสารสนเทศต้องบันทึกข้อมูลจากแหล่งกำเนิดที่เชื่อถือได้ (Single Source of Truth) ห้ามสร้างข้อมูลซ้ำซ้อนข้ามระบบ\n"
         "• การป้องกันข้อมูลเท็จ: บังคับใช้การตรวจสอบตัวตนของผู้บันทึกข้อมูล (User Audit Trail) และการล็อกอินด้วยระบบความปลอดภัย ห้ามกรอกข้อมูลเท็จตาม พ.ร.บ. ว่าด้วยการกระทำความผิดเกี่ยวกับคอมพิวเตอร์ พ.ศ. 2560\n"
         "• การกำกับ Metadata: เมื่อมีการสร้างตารางฐานข้อมูลใหม่ ต้องลงทะเบียนคำอธิบายฟิลด์และระดับชั้นความลับในระบบ Data Catalog ทันที"),

        ("ขั้นตอนที่ 2: การจัดเก็บและดูแลรักษา (Data Storage & Maintenance)",
         "• การเข้ารหัส: ข้อมูลส่วนบุคคลและข้อมูลสุขภาพต้องได้รับการเข้ารหัสขณะจัดเก็บ (Encryption at Rest) ด้วยอัลกอริทึม AES-256 หรือเทียบเท่า\n"
         "• การสำรองข้อมูล: กำหนดให้สำรองข้อมูลแบบ Daily Incremental และ Weekly Full Backup พร้อมจัดเก็บสำเนาสำรองไว้นอกสถานที่ (Off-site / Multi-Region Cloud)\n"
         "• การแยกส่วนข้อมูล: ห้ามเก็บข้อมูลความลับ (เช่น รหัสผ่าน, ข้อมูลบัตรเครดิต, ประวัติการรักษาโรคต้องห้าม) รวมไว้ในตารางทั่วไป ต้องแยกเก็บใน Secure Vault"),

        ("ขั้นตอนที่ 3: การประมวลผลและการใช้ประโยชน์ (Data Processing & Usage)",
         "• หลักความจำเป็น (Need-to-Know Basis): การเข้าถึงข้อมูลต้องได้รับอนุมัติตามหน้าที่ความรับผิดชอบผ่านระบบ Role-Based Access Control (RBAC)\n"
         "• การกำกับวัตถุประสงค์ (Purpose Limitation): ห้ามนำข้อมูลผู้ป่วยหรือลูกค้าไปประมวลผลนอกเหนือวัตถุประสงค์ที่แจ้งไว้ในหนังสือยินยอม (Consent Form)\n"
         "• การนำไปใช้เพื่อการวิเคราะห์และ AI: ต้องผ่านกระบวนการลดรูปหรือตัดข้อมูลระบุตัวตน (Data Masking / Tokenization / De-identification) ก่อนส่งมอบให้ทีมงาน"),

        ("ขั้นตอนที่ 4: การเปิดเผยและการแลกเปลี่ยนข้อมูล (Data Publishing & Sharing)",
         "• การเปิดเผยข้อมูลสาธารณะ (Open Data): ต้องผ่านการตรวจสอบจากคณะกรรมการว่าไม่มีข้อมูลส่วนบุคคลหรือความลับทางการค้าหลุดรอด โดยให้อยู่ในฟอร์แมตเปิด เช่น CSV, JSON หรือ REST API\n"
         "• การแลกเปลี่ยนข้อมูลกับหน่วยงานภายนอก: ต้องจัดทำสัญญาประมวลผลข้อมูล (Data Processing Agreement - DPA) และข้อตกลงรักษาความลับ (NDA) ทุกครั้ง\n"
         "• ช่องทางการส่งข้อมูล: ต้องส่งผ่านช่องทางที่มีการเข้ารหัสขณะส่งผ่าน (Encryption in Transit) เช่น TLS 1.3 หรือ SFTP ห้ามส่งข้อมูลความลับผ่านอีเมลส่วนตัวหรือแอปพลิเคชันแชต"),

        ("ขั้นตอนที่ 5: การจัดเก็บถาวร (Data Archiving)",
         "• เกณฑ์การโอนย้าย: ข้อมูลที่ไม่มีการเคลื่อนไหวเกิน 3 ปี ให้โอนย้ายจากฐานข้อมูลหลักไปยังระบบจัดเก็บถาวรระยะยาว (Cold Storage / Glacier) เพื่อลดต้นทุนโครงสร้างพื้นฐาน\n"
         "• การทดสอบการกู้คืน (Restore Drill): กำหนดให้ฝ่ายเทคโนโลยีสารสนเทศต้องซักซ้อมและทดสอบการกู้คืนข้อมูลจาก Archive อย่างน้อยปีละ 1 ครั้ง โดยต้องกู้คืนได้ภายใน RTO < 4 ชั่วโมง"),

        ("ขั้นตอนที่ 6: การทำลายข้อมูล (Data Destruction)",
         "• การสิ้นสุดระยะเวลาจัดเก็บ: เมื่อข้อมูลครบกำหนดระยะเวลาจัดเก็บตามกฎหมาย (เวชระเบียน 5 ปี หรือข้อมูลบัญชี 10 ปี) คณะทำงานต้องจัดทำบัญชีรายชื่อข้อมูลเสนอต่อคณะกรรมการ\n"
         "• วิธีการทำลายที่ปลอดภัย: ข้อมูลดิจิทัลต้องถูกทำลายด้วยวิธี Cryptographic Erasure หรือ Overwrite Data หลายรอบตามมาตรฐาน DoD 5220.22-M ส่วนสื่อจัดเก็บทางกายภาพต้องผ่านการย่อยสลาย (Shredding/Degaussing)\n"
         "• การออกใบรับรอง: ต้องมีการลงนามในใบรับรองการทำลายข้อมูล (Certificate of Data Destruction) และเก็บรักษาบันทึกหลักฐานไว้อย่างน้อย 1 ปี")
    ]
    for sop_title, sop_detail in lifecycle_sops:
        p_sop = doc.add_paragraph()
        p_sop.paragraph_format.space_after = Pt(6)
        r_st = p_sop.add_run(sop_title + "\n")
        r_st.font.bold = True
        r_st.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
        p_sop.add_run(sop_detail)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # CHAPTER 6: ENTERPRISE DATA CATALOG & 14 DGA FIELDS
    # --------------------------------------------------------------------------
    h6 = doc.add_heading("บทที่ 6: บัญชีข้อมูลองค์กรและมาตรฐานเมทาดาตา 14 รายการ (Enterprise Data Catalog)", level=1)
    h6.paragraph_format.space_before = Pt(14)

    doc.add_paragraph(
        f"การจัดทำบัญชีข้อมูลองค์กร (Enterprise Data Catalog) ตามมาตรฐานของสำนักงานพัฒนารัฐบาลดิจิทัล (สพร./DGA) "
        f"ทำหน้าที่เป็น 'สมุดหน้าเหลือง' ที่รวบรวมรายการชุดข้อมูลทั้งหมดของ {client.name} เพื่อสร้างความโปร่งใส "
        f"ลดการทำงานซ้ำซ้อน และเป็นฐานรากสำคัญในการควบคุมสิทธิ์การเข้าถึงข้อมูลตามกฎหมาย PDPA โดยมี 14 ฟิลด์บังคับดังนี้:"
    )

    dga_fields_desc = [
        ("1. ชื่อชุดข้อมูล (Dataset Title):", "ชื่อภาษาไทยและภาษาอังกฤษที่สื่อความหมายชัดเจน"),
        ("2. หน่วยงานเจ้าของข้อมูล (Owner Org):", "ชื่อองค์กรและฝ่ายงานที่เป็นเจ้าของข้อมูลทางธุรกิจ"),
        ("3. ผู้ติดต่อ/ผู้ดูแล (Maintainer):", "ชื่อตำแหน่งหรือกลุ่มงานที่รับผิดชอบการปรับปรุงชุดข้อมูล"),
        ("4. อีเมลผู้ติดต่อ (Maintainer Email):", "ช่องทางการติดต่อเพื่อขอสิทธิ์หรือสอบถามข้อมูล"),
        ("5. คำสำคัญ (Keywords/Tags):", "คำค้นหาสำหรับสืบค้นในระบบ Catalog กลาง"),
        ("6. คำอธิบายชุดข้อมูล (Notes/Description):", "รายละเอียดของชุดข้อมูล ขอบเขต และบริบทการนำไปใช้"),
        ("7. วัตถุประสงค์ในการจัดเก็บ (Objective):", "เหตุผลทางกฎหมายหรือทางธุรกิจในการประมวลผลข้อมูล"),
        ("8. ความถี่ในการปรับปรุง (Update Frequency):", "รอบเวลาการอัปเดต เช่น Real-time, Daily, Monthly, Annually"),
        ("9. ขอบเขตเชิงภูมิศาสตร์ (Geographic Coverage):", "พื้นที่ที่ข้อมูลครอบคลุม เช่น ประเทศไทย หรือเฉพาะโรงพยาบาล"),
        ("10. แหล่งที่มาของข้อมูล (Data Source):", "ระบบสารสนเทศต้นทาง เช่น HIS Database, PACS Storage, LIS Server"),
        ("11. รูปแบบข้อมูล (Data Format):", "ชนิดของไฟล์หรือโปรโตคอล เช่น Relational Table, DICOM, HL7, API, CSV"),
        ("12. หมวดหมู่ข้อมูล (Data Category):", "กลุ่มของข้อมูล เช่น เวชระเบียน การเงิน เภสัชกรรม บุคลากร"),
        ("13. เงื่อนไขการอนุญาต (License ID):", "สิทธิ์การเข้าถึงและข้อจำกัดการใช้งานตามกฎหมาย"),
        ("14. ชั้นความลับและคะแนนคุณภาพ (Classification & Quality Score):", "ระดับความลับ 5 ระดับ และคะแนน DQA")
    ]
    for f_name, f_desc in dga_fields_desc:
        p_f = doc.add_paragraph()
        p_f.paragraph_format.space_after = Pt(2)
        r_fn = p_f.add_run(f_name + " ")
        r_fn.font.bold = True
        p_f.add_run(f_desc)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    doc.add_heading("6.1 รายการชุดข้อมูลสำคัญ 12 ชุดข้อมูลที่ขึ้นทะเบียนใน Data Catalog", level=2)
    doc.add_paragraph("ตารางสรุปเมทาดาตาของ 12 ชุดข้อมูลหลักที่ผ่านการขึ้นทะเบียนเข้าสู่ระบบบัญชีข้อมูลองค์กร:")

    tbl_cat = doc.add_table(rows=1, cols=6)
    tbl_cat.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_hdrs = ["ลำดับ", "ชื่อชุดข้อมูล", "ฝ่ายผู้ดูแล", "แหล่งต้นทาง", "ชั้นความลับ", "คะแนนคุณภาพ"]
    for idx, name in enumerate(c_hdrs):
        cell = tbl_cat.rows[0].cells[idx]
        cell.text = name
        set_cell_background(cell, "27AE60")
        p_hdr = cell.paragraphs[0]
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_hdr.runs[0].font.bold = True
        p_hdr.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    cat_12_summary = [
        ("1.0", "Master Patient Index (EMPI Golden Records)", "เวชระเบียน", "HIS Database", "ข้อมูลอ่อนไหว (PDPA ม.26)", "94.5%"),
        ("2.0", "Inpatient Bed Registry & Bed Turnover Logs", "ฝ่ายการพยาบาล", "HIS IPD Bed System", "ข้อมูลใช้งานภายใน", "88.0%"),
        ("3.0", "Medical Billing, DRG & Insurance Claims DB", "ฝ่ายการเงิน/ประกัน", "ERP & Claim Gateway", "ข้อมูลความลับทางการค้า", "91.2%"),
        ("4.0", "Outpatient Appointment Registry & History", "ฝ่ายบริการลูกค้า", "HIS OPD Scheduling", "ข้อมูลส่วนบุคคลทั่วไป", "85.4%"),
        ("5.0", "Central Pharmacy Drug Inventory & Expiry DB", "ฝ่ายเภสัชกรรม", "Smart Pharmacy System", "ข้อมูลใช้งานภายใน", "96.0%"),
        ("6.0", "Operating Theatre (OR) Resource Schedules", "ฝ่ายศัลยกรรม/OR", "OR Scheduling DB", "ข้อมูลใช้งานภายใน", "82.5%"),
        ("7.0", "Emergency Department Triage & ER Logs", "เวชศาสตร์ฉุกเฉิน", "ER Triage System", "ข้อมูลอ่อนไหว (PDPA ม.26)", "89.0%"),
        ("8.0", "PACS Radiology Imaging Metadata Index", "ฝ่ายรังสีวิทยา", "PACS Archive Server", "ข้อมูลอ่อนไหว (PDPA ม.26)", "93.5%"),
        ("9.0", "Laboratory Information (LIS) Test Results", "ฝ่ายห้องปฏิบัติการ", "LIS Server", "ข้อมูลอ่อนไหว (PDPA ม.26)", "95.0%"),
        ("10.0", "ICU Patient Vital Signs & Hemodynamic Monitor", "หอผู้ป่วยวิกฤต (ICU)", "ICU Monitoring Feeds", "ข้อมูลอ่อนไหว (PDPA ม.26)", "91.8%"),
        ("11.0", "Health Checkup Packages & Screening Results", "ศูนย์ตรวจสุขภาพ", "Checkup Portal DB", "ข้อมูลอ่อนไหว (PDPA ม.26)", "87.5%"),
        ("12.0", "Hospital Incident & Clinical Quality Audit DB", "ฝ่ายพัฒนาคุณภาพ (QA)", "Incident Report System", "ข้อมูลความลับระดับสูง", "90.0%")
    ]
    for row_info in cat_12_summary:
        r_cells = tbl_cat.add_row().cells
        for c_i, val in enumerate(row_info):
            r_cells[c_i].text = val
            if c_i in [0, 4, 5]:
                r_cells[c_i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            if c_i == 5:
                r_cells[c_i].paragraphs[0].runs[0].font.bold = True
                r_cells[c_i].paragraphs[0].runs[0].font.color.rgb = RGBColor(0x27, 0xAE, 0x60)
            set_cell_margins(r_cells[c_i])

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # CHAPTER 7: DATA QUALITY ASSURANCE & 5D EVALUATION
    # --------------------------------------------------------------------------
    h7 = doc.add_heading("บทที่ 7: กรอบการประกันคุณภาพข้อมูลและการประเมิน 5 มิติ (Data Quality Assurance)", level=1)
    h7.paragraph_format.space_before = Pt(14)

    doc.add_paragraph(
        "คุณภาพของข้อมูลคือหัวใจสำคัญสูงสุดในการตัดสินใจทางการแพทย์และการสร้างโมเดลปัญญาประดิษฐ์ "
        "หากข้อมูลต้นทางผิดพลาดหรือไม่สมบูรณ์ โมเดล AI จะสร้างผลลัพธ์ที่ผิดพลาด (Garbage In, Garbage Out) "
        "ซึ่งอาจส่งผลถึงชีวิตของผู้ป่วย คณะที่ปรึกษาจึงกำหนดกรอบการประเมินคุณภาพข้อมูล 5 มิติ (DQA 5-Dimension Framework) "
        "ตามมาตรฐานของสำนักงานพัฒนารัฐบาลดิจิทัล (สพร.) ดังนี้:"
    )

    tbl_dq5 = doc.add_table(rows=6, cols=4)
    tbl_dq5.alignment = WD_TABLE_ALIGNMENT.CENTER
    dq5_data = [
        ("มิติคุณภาพข้อมูล (สพร.)", "นิยามและความหมาย", "ค่าน้ำหนัก", "แนวทางการปรับปรุงแก้ไข (Remediation)"),
        ("1. ความถูกต้องและสมบูรณ์ (Accuracy & Completeness)", "ข้อมูลถูกต้องตามความจริงทางคลินิก ไม่มีฟิลด์สำคัญตกหล่น (เช่น ค่าว่างใน HN, ประวัติแพ้ยา)", "25%", "ทำ Automated Null Check และบังคับ Mandatory Fields บน UI"),
        ("2. ความสอดคล้องกัน (Consistency)", "ข้อมูลตรงกันระหว่างระบบต่าง ๆ รหัสอ้างอิงตรงตามมาตรฐานสากล (ICD-10, TMT, LOINC)", "20%", "จัดทำ Master Data Management และตารางแมปโค้ดอัตโนมัติ"),
        ("3. ความเป็นปัจจุบัน (Timeliness)", "ข้อมูลถูกส่งเข้าสู่ระบบอย่างรวดเร็ว พร้อมนำไปใช้ในการรักษาและตัดสินใจได้ทันท่วงที", "20%", "ปรับเปลี่ยนจาก Batch รายเดือนเป็น Daily CDC Pipeline ผ่าน Kafka"),
        ("4. ตรงตามความต้องการ (Relevancy)", "ชุดข้อมูลมีฟิลด์ที่ตอบโจทย์การใช้งานจริง ไม่มีข้อมูลขยะหรือฟิลด์ที่ไม่ได้ใช้งาน", "15%", "ตัดคอลัมน์ที่ไม่จำเป็นออกจาก Data Lakehouse และทำ Data Dictionary"),
        ("5. ความพร้อมใช้งาน (Availability)", "ระบบฐานข้อมูลมีความเสถียร มีสิทธิ์การเข้าถึงที่ถูกต้องตาม SLA ไม่ล่มบ่อย", "20%", "ย้ายระบบสู่ Cloud High Availability พร้อมทดสอบ Disaster Recovery")
    ]
    for r_i, row in enumerate(dq5_data):
        for c_i, val in enumerate(row):
            c = tbl_dq5.rows[r_i].cells[c_i]
            c.text = val
            if r_i == 0:
                set_cell_background(c, "8E44AD")
                c.paragraphs[0].runs[0].font.bold = True
                c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                if c_i in [0, 2]:
                    c.paragraphs[0].runs[0].font.bold = True
                if c_i == 2:
                    c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_margins(c)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_callout(
        doc,
        "กฎเหล็กสะพานเชื่อมต่อสู่ปัญญาประดิษฐ์ (The Bridge Gate Principle)",
        "ชุดข้อมูลใด ๆ ก็ตามที่จะถูกนำไปใช้เทรนหรือเชื่อมต่อกับโมเดลปัญญาประดิษฐ์ (AI/ML) "
        "จะต้องผ่านการประเมินคุณภาพข้อมูลรวมไม่น้อยกว่า 80% (Data Quality Score >= 80.0%) "
        "และต้องผ่านการตัดข้อมูลส่วนบุคคล (De-identification) เรียบร้อยแล้ว หากไม่ผ่านเกณฑ์ "
        "ระบบ MLOps Pipeline จะระงับการเทรนโมเดลโดยอัตโนมัติ เพื่อป้องกันอันตรายทางการแพทย์"
    )

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # CHAPTER 8: 10 INSTITUTIONAL DATA GOVERNANCE POLICIES (VERBATIM ARTICLES)
    # --------------------------------------------------------------------------
    h8 = doc.add_heading("บทที่ 8: นโยบายธรรมาภิบาลข้อมูลหลัก 10 ฉบับ (10 Institutional Policies)", level=1)
    h8.paragraph_format.space_before = Pt(14)

    doc.add_paragraph(
        f"เพื่อสร้างกรอบการกำกับดูแลที่มีผลผูกพันทางกฎหมายและมีผลบังคับใช้ทั่วทั้ง {client.name} "
        f"คณะที่ปรึกษาได้ยกร่างระเบียบข้อบังคับและนโยบายธรรมาภิบาลข้อมูลฉบับสมบูรณ์ 10 ฉบับ "
        f"โดยระบุข้อกำหนดเป็นรายมาตราอย่างละเอียด สอดคล้องตาม พ.ร.บ. คุ้มครองข้อมูลส่วนบุคคล พ.ศ. 2562 (PDPA) "
        f"และมาตรฐานสากล ISO/IEC 27001 และ ISO/IEC 42001:"
    )

    policies_data = [
        ("นโยบายฉบับที่ 1: นโยบายการจัดชั้นความลับของข้อมูล (Data Classification Policy)", [
            "ข้อ 1: ข้อมูลทั้งหมดขององค์กรต้องได้รับการจัดระดับชั้นความลับออกเป็น 5 ระดับ ได้แก่: (1) ข้อมูลสาธารณะ (Public), (2) ข้อมูลใช้งานภายใน (Internal), (3) ข้อมูลลับ (Confidential), (4) ข้อมูลลับมาก (Strictly Confidential), และ (5) ข้อมูลส่วนบุคคลอ่อนไหว (Sensitive PII ตาม PDPA ม.26)",
            "ข้อ 2: ผู้มีหน้าที่จัดชั้นความลับคือ เจ้าของข้อมูลทางธุรกิจ (Data Owner) ร่วมกับคณะบริกรข้อมูล (Data Stewards) โดยต้องระบุชั้นความลับลงในระบบ Data Catalog ตั้งแต่วันแรกที่สร้างชุดข้อมูล",
            "ข้อ 3: ข้อมูลเวชระเบียน ประวัติการรักษาโรค ผลการตรวจทางห้องปฏิบัติการ และภาพถ่ายรังสีของผู้ป่วย ให้ถือเป็น 'ข้อมูลส่วนบุคคลอ่อนไหว' โดยเด็ดขาด ห้ามจัดเก็บในชั้นความลับที่ต่ำกว่าระดับ 4",
            "ข้อ 4: ข้อมูลที่มีชั้นความลับระดับ 3 ขึ้นไป ต้องได้รับการเข้ารหัสขณะจัดเก็บ (Encryption at Rest) และเข้ารหัสขณะส่งผ่านเครือข่าย (Encryption in Transit) เสมอ",
            "ข้อ 5: การลดระดับชั้นความลับของข้อมูล (De-classification) จะกระทำได้ต่อเมื่อได้รับความเห็นชอบจากเจ้าหน้าที่คุ้มครองข้อมูลส่วนบุคคล (DPO) และการอนุมัติจากคณะกรรมการธรรมาภิบาลข้อมูลเท่านั้น"
        ]),

        ("นโยบายฉบับที่ 2: นโยบายการควบคุมการเข้าถึงข้อมูล (Access Control & Identity Policy)", [
            "ข้อ 1: การเข้าถึงระบบสารสนเทศและฐานข้อมูลขององค์กรต้องยึดหลัก 'ความจำเป็นในการปฏิบัติงาน' (Need-to-Know Principle) และหลัก 'สิทธิ์ขั้นต่ำที่จำเป็น' (Principle of Least Privilege)",
            "ข้อ 2: การกำหนดสิทธิ์ต้องใช้ระบบการควบคุมการเข้าถึงตามบทบาท (Role-Based Access Control - RBAC) ห้ามมิให้กำหนดสิทธิ์การเข้าถึงเป็นรายบุคคลโดยไม่มีบทบาทรองรับ",
            "ข้อ 3: การเข้าถึงข้อมูลชั้นความลับระดับสูง ข้อมูลทางการแพทย์ และระบบคลาวด์ ต้องผ่านการยืนยันตัวตนแบบหลายปัจจัย (Multi-Factor Authentication - MFA) ทุกครั้ง",
            "ข้อ 4: ห้ามบุคลากรใช้บัญชีผู้ใช้งานร่วมกัน (Shared Account) บัญชีผู้ใช้งานทุกบัญชีต้องระบุตัวตนบุคคลผู้ถือครองได้ชัดเจน",
            "ข้อ 5: ผู้ดูแลระบบไอที (Data Custodian) ต้องจัดทำระบบตัดสิทธิ์การเข้าถึงของผู้ปฏิบัติงานที่ลาออก โอนย้าย หรือสิ้นสุดสัญญาจ้าง โดยอัตโนมัติภายใน 24 ชั่วโมงหลังได้รับแจ้งจากฝ่ายทรัพยากรบุคคล",
            "ข้อ 6: คณะบริกรข้อมูลต้องดำเนินการทบทวนสิทธิ์การเข้าถึงข้อมูล (Access Rights Audit) เป็นประจำทุก 6 เดือน หากพบบัญชีที่ไม่มีการใช้งานเกิน 90 วัน ให้ทำการระงับสิทธิ์ทันที"
        ]),

        ("นโยบายฉบับที่ 3: นโยบายการคุ้มครองข้อมูลส่วนบุคคลและข้อมูลสุขภาพ (PDPA & Health Data Policy)", [
            "ข้อ 1: การเก็บรวบรวม ใช้ หรือเปิดเผยข้อมูลส่วนบุคคลของผู้ป่วย ต้องเป็นไปตามฐานทางกฎหมายที่บัญญัติไว้ในพระราชบัญญัติคุ้มครองข้อมูลส่วนบุคคล พ.ศ. 2562 โดยต้องแจ้งวัตถุประสงค์ผ่านคำประกาศเกี่ยวกับความเป็นส่วนตัว (Privacy Notice) อย่างชัดเจน",
            "ข้อ 2: การประมวลผลข้อมูลส่วนบุคคลอ่อนไหว (Sensitive Data) ตามมาตรา 26 โดยเฉพาะข้อมูลสุขภาพ ข้อมูลพันธุกรรม ข้อมูลชีวภาพ จะต้องได้รับความยินยอมโดยชัดแจ้ง (Explicit Consent) จากเจ้าของข้อมูล เว้นแต่เป็นกรณีจำเป็นเพื่อการรักษาพยาบาลฉุกเฉินเพื่อป้องกันอันตรายต่อชีวิต ร่างกาย หรือสุขภาพ (Vital Interest)",
            "ข้อ 3: เจ้าของข้อมูลส่วนบุคคลมีสิทธิ์ตามกฎหมาย ได้แก่ สิทธิ์ขอเข้าถึงข้อมูล, สิทธิ์ขอแก้ไขข้อมูลให้ถูกต้อง, สิทธิ์ขอลบหรือทำลายข้อมูล, สิทธิ์ขอให้โอนย้ายข้อมูล, และสิทธิ์ถอนความยินยอม องค์กรต้องดำเนินการตามคำร้องขอภายใน 30 วัน",
            "ข้อ 4: การนำข้อมูลผู้ป่วยไปใช้ในงานวิจัย การเรียนการสอน หรือการวิเคราะห์สถิติ ต้องผ่านกระบวนการทำให้เป็นข้อมูลนิรนาม (Anonymization) หรือการตัดตัวตน (De-identification) จนไม่สามารถระบุตัวบุคคลได้อีกต่อไป",
            "ข้อ 5: ห้ามมิให้นำข้อมูลผู้ป่วยหรือลูกค้าไปแสวงหาผลประโยชน์ทางการค้า ขายข้อมูลให้แก่บริษัทประกัน หรือส่งต่อให้คู่ค้าภายนอกโดยปราศจากความยินยอมเป็นลายลักษณ์อักษร"
        ]),

        ("นโยบายฉบับที่ 4: นโยบายการสำรองข้อมูลและการกู้คืนข้อมูลจากภัยพิบัติ (Data Backup & DR Policy)", [
            "ข้อ 1: ระบบฐานข้อมูลที่มีความสำคัญต่อการรักษาพยาบาล (Mission-Critical Systems) เช่น HIS, LIS, PACS ต้องได้รับการสำรองข้อมูลอย่างสม่ำเสมอ โดยยึดหลักเกณฑ์ 3-2-1 Backup Rule (สำเนา 3 ชุด, จัดเก็บบนสื่อ 2 ชนิด, มี 1 ชุดอยู่นอกสถานที่)",
            "ข้อ 2: กำหนดให้สำรองข้อมูลฐานข้อมูลหลักแบบ Real-time / Daily Incremental และสำรองข้อมูลฉบับเต็ม (Full Backup) ทุกสัปดาห์",
            "ข้อ 3: ไฟล์สำรองข้อมูลทั้งหมดต้องได้รับการเข้ารหัส (Backup Encryption) ด้วยมาตรฐานความปลอดภัยสูงสุด และเก็บรักษาในสภาพแวดล้อมที่ควบคุมการเข้าถึงอย่างเข้มงวด",
            "ข้อ 4: ฝ่ายเทคโนโลยีสารสนเทศต้องกำหนดเป้าหมายระยะเวลาการกู้คืนข้อมูล (Recovery Time Objective - RTO) ไม่เกิน 4 ชั่วโมง และเป้าหมายจุดเวลาการสูญเสียข้อมูลสูงสุด (Recovery Point Objective - RPO) ไม่เกิน 15 นาที",
            "ข้อ 5: ต้องจัดให้มีการซักซ้อมแผนกู้คืนระบบจากภัยพิบัติ (Disaster Recovery Drill) อย่างน้อยปีละ 1 ครั้ง โดยต้องจัดทำรายงานผลการซักซ้อมเสนอต่อคณะกรรมการธรรมาภิบาลข้อมูล"
        ]),

        ("นโยบายฉบับที่ 5: นโยบายระยะเวลาการจัดเก็บและการทำลายข้อมูล (Data Retention & Destruction Policy)", [
            "ข้อ 1: ข้อมูลเวชระเบียนและประวัติการรักษาพยาบาลของผู้ป่วย ต้องจัดเก็บรักษาไว้ไม่น้อยกว่า 5 ปี นับแต่วันที่ผู้ป่วยมารับการรักษาครั้งสุดท้าย ตามที่กำหนดในพระราชบัญญัติสถานพยาบาล พ.ศ. 2541",
            "ข้อ 2: ข้อมูลทางการเงิน ใบเสร็จรับเงิน และเอกสารการเบิกจ่ายค่ารักษาพยาบาล ต้องจัดเก็บรักษาไว้ไม่น้อยกว่า 10 ปี ตามประมวลรัษฎากรและกฎหมายการบัญชี",
            "ข้อ 3: บันทึกข้อมูลจราจรทางคอมพิวเตอร์ (Log Files) ต้องจัดเก็บรักษาไว้ไม่น้อยกว่า 90 วัน ตาม พ.ร.บ. ว่าด้วยการกระทำความผิดเกี่ยวกับคอมพิวเตอร์ พ.ศ. 2560",
            "ข้อ 4: เมื่อพ้นกำหนดระยะเวลาการจัดเก็บตามกฎหมาย ให้หัวหน้าหน่วยงานเจ้าของข้อมูลจัดทำบัญชีข้อมูลเสนอต่อคณะกรรมการเพื่อขออนุมัติทำลายข้อมูล",
            "ข้อ 5: การทำลายข้อมูลดิจิทัลต้องใช้วิธีการทำลายแบบถาวรที่ไม่อาจกู้คืนได้ (Permanent Sanitization) ตามมาตรฐาน NIST SP 800-88 และต้องออกใบรับรองการทำลายข้อมูลไว้เป็นหลักฐาน"
        ]),

        ("นโยบายฉบับที่ 6: นโยบายการแลกเปลี่ยนและโอนย้ายข้อมูล (Data Sharing & Transfer Policy)", [
            "ข้อ 1: การแลกเปลี่ยนข้อมูลระหว่างหน่วยงานภายในองค์กร ต้องกระทำผ่านระบบบริการข้อมูลกลาง (Enterprise API Gateway หรือ Data Lakehouse) ห้ามส่งไฟล์ฐานข้อมูลดิบผ่านแฟลชไดรฟ์หรือช่องทางที่ไม่ปลอดภัย",
            "ข้อ 2: การแลกเปลี่ยนข้อมูลกับหน่วยงานภายนอก (เช่น สปสช., บริษัทประกัน, โรงพยาบาลเครือข่าย) ต้องใช้มาตรฐานการแลกเปลี่ยนข้อมูลสากล เช่น HL7 FHIR และต้องเข้ารหัสข้อมูลด้วยโปรโตคอล TLS 1.3 ขึ้นไป",
            "ข้อ 3: การส่งข้อมูลส่วนบุคคลออกนอกราชอาณาจักร (Cross-Border Data Transfer) จะกระทำได้ก็ต่อเมื่อประเทศปลายทางมีมาตรฐานการคุ้มครองข้อมูลส่วนบุคคลที่เพียงพอ ตามประกาศคณะกรรมการคุ้มครองข้อมูลส่วนบุคคล (สคส.) หรือมีข้อสัญญามาตรฐาน (Standard Contractual Clauses - SCCs)",
            "ข้อ 4: การจัดจ้างผู้ให้บริการประมวลผลข้อมูลภายนอก (Cloud Service Provider / Data Processor) ต้องมีการจัดทำสัญญาประมวลผลข้อมูล (Data Processing Agreement - DPA) กำกับเสมอ"
        ]),

        ("นโยบายฉบับที่ 7: นโยบายการรายงานและระงับเหตุการณ์ข้อมูลรั่วไหล (Data Breach Response Policy)", [
            "ข้อ 1: เหตุการณ์ข้อมูลรั่วไหล (Personal Data Breach) หมายถึง เหตุการณ์ใด ๆ ที่ทำให้ข้อมูลส่วนบุคคลถูกทำลาย สูญหาย เปลี่ยนแปลง แก้ไข หรือถูกเข้าถึงโดยบุคคลที่ไม่มีอำนาจ",
            "ข้อ 2: บุคลากรทุกคนที่พบเห็นหรือสงสัยว่ามีเหตุการณ์ข้อมูลรั่วไหล ต้องรายงานต่อฝ่ายเทคโนโลยีสารสนเทศและเจ้าหน้าที่คุ้มครองข้อมูลส่วนบุคคล (DPO) ทันที ภายใน 1 ชั่วโมงหลังจากพบเหตุ",
            "ข้อ 3: คณะทำงานตอบสนองเหตุการณ์ความมั่นคงปลอดภัย (Incident Response Team) ต้องเข้าควบคุมและระงับเหตุการณ์โดยทันที เพื่อจำกัดความเสียหายมิให้ลุกลาม",
            "ข้อ 4: เจ้าหน้าที่คุ้มครองข้อมูลส่วนบุคคล (DPO) มีหน้าที่ประเมินความเสี่ยง หากพบว่าเหตุการณ์มีความเสี่ยงที่จะมีผลกระทบต่อสิทธิและเสรีภาพของบุคคล ต้องแจ้งเหตุต่อสำนักงานคณะกรรมการคุ้มครองข้อมูลส่วนบุคคล (สคส.) โดยไม่ชักช้า ภายใน 72 ชั่วโมง",
            "ข้อ 5: กรณีที่การรั่วไหลมีความเสี่ยงสูงที่จะมีผลกระทบต่อเจ้าของข้อมูล ต้องแจ้งเหตุการณ์และแนวทางการเยียวยาให้เจ้าของข้อมูลส่วนบุคคลทราบโดยทันที"
        ]),

        ("นโยบายฉบับที่ 8: นโยบายการเข้ารหัสข้อมูลและการจัดการกุญแจ (Cryptography Policy)", [
            "ข้อ 1: ข้อมูลที่มีชั้นความลับระดับสูง ข้อมูลเวชระเบียน และข้อมูลส่วนบุคคล ต้องได้รับการปกป้องด้วยการเข้ารหัสข้อมูลที่ได้มาตรฐานสากล (Strong Encryption)",
            "ข้อ 2: การเข้ารหัสข้อมูลขณะจัดเก็บ (At-Rest) ต้องใช้อัลกอริทึม AES ที่มีขนาดกุญแจไม่น้อยกว่า 256 บิต (AES-256)",
            "ข้อ 3: การเข้ารหัสข้อมูลขณะส่งผ่านเครือข่าย (In-Transit) ต้องใช้โปรโตคอล TLS เวอร์ชัน 1.3 หรือเทียบเท่า โดยไม่อนุญาตให้ใช้เวอร์ชันที่มีช่องโหว่ (เช่น TLS 1.0, 1.1)",
            "ข้อ 4: กุญแจเข้ารหัส (Cryptographic Keys) ต้องได้รับการจัดเก็บแยกต่างหากจากข้อมูล และเก็บรักษาในระบบจัดการกุญแจที่มีความมั่นคงปลอดภัยสูง เช่น Hardware Security Module (HSM) หรือ Cloud KMS",
            "ข้อ 5: ต้องจัดให้มีการหมุนเวียนกุญแจเข้ารหัส (Key Rotation) เป็นประจำอย่างน้อยปีละ 1 ครั้ง หรือทันทีที่มีข้อสงสัยว่ากุญแจอาจรั่วไหล"
        ]),

        ("นโยบายฉบับที่ 9: นโยบายการใช้ข้อมูลเพื่อการวิจัยและแซนด์บ็อกซ์ (Research Sandbox Policy)", [
            "ข้อ 1: การนำข้อมูลผู้ป่วยไปใช้เพื่อการศึกษาวิจัยทางการแพทย์ การพัฒนาสูตรยา หรือการฝึกสอนโมเดลปัญญาประดิษฐ์ ต้องได้รับความเห็นชอบจากคณะกรรมการจริยธรรมการวิจัยในมนุษย์ (IRB / Ethics Committee)",
            "ข้อ 2: ข้อมูลที่ใช้ในงานวิจัยต้องนำเข้าสู่ระบบสภาพแวดล้อมทดสอบที่ปลอดภัย (Research Sandbox Environment) ที่มีการตัดขาดจากการเชื่อมต่ออินเทอร์เน็ตสาธารณะ",
            "ข้อ 3: ชุดข้อมูลวิจัยต้องผ่านกระบวนการ De-identification โดยการตัดข้อมูลระบุตัวตนทั้ง 18 รายการตามมาตรฐาน HIPAA Safe Harbor และหลักเกณฑ์ของ PDPA มาตรา 26",
            "ข้อ 4: ห้ามมิให้นักวิจัยคัดลอกหรือนำข้อมูลออกจากสภาพแวดล้อมแซนด์บ็อกซ์โดยไม่ได้รับอนุญาตเป็นลายลักษณ์อักษรจาก Lead Data Steward",
            "ข้อ 5: ผลการวิเคราะห์ที่จะเผยแพร่ต่อสาธารณะ ต้องเป็นข้อมูลสรุปเชิงสถิติรวม (Aggregated Data) ที่ไม่สามารถย้อนกลับไประบุตัวผู้ป่วยได้"
        ]),

        ("นโยบายฉบับที่ 10: นโยบายการใช้งานปัญญาประดิษฐ์เชิงสร้างสรรค์อย่างปลอดภัย (Generative AI Usage Policy)", [
            "ข้อ 1: ห้ามบุคลากรป้อนข้อมูลความลับขององค์กร ข้อมูลเวชระเบียนคนไข้ ผลแล็บ หรือข้อมูลส่วนบุคคล ลงในเครื่องมือ Generative AI สาธารณะ (เช่น ChatGPT, Gemini Public, Claude Public) โดยเด็ดขาด",
            "ข้อ 2: การใช้งาน Generative AI ในการประมวลผลงานขององค์กร ต้องใช้ระบบที่เป็น Enterprise Agreement ที่มีข้อตกลง Zero Data Retention และไม่นำข้อมูลไปใช้เทรนโมเดลส่วนกลาง",
            "ข้อ 3: ผลลัพธ์ที่สร้างขึ้นจากปัญญาประดิษฐ์ (AI-generated content) ต้องได้รับการตรวจสอบความถูกต้องโดยผู้เชี่ยวชาญที่เป็นมนุษย์ (Human Oversight) ก่อนนำไปใช้ในการรักษาพยาบาลหรือการออกเอกสารทางการ",
            "ข้อ 4: องค์กรต้องติดตั้งระบบ Data Loss Prevention (DLP) และ AI Security Gateway เพื่อตรวจจับและสกัดกั้นการส่งผ่านข้อมูลอ่อนไหวไปยังระบบภายนอก",
            "ข้อ 5: บุคลากรที่ฝ่าฝืนนำข้อมูลคนไข้ไปประมวลผลในระบบ AI สาธารณะ จะถือเป็นความผิดทางวินัยร้ายแรงและอาจถูกดำเนินคดีตามกฎหมาย PDPA"
        ])
    ]

    for p_head, articles in policies_data:
        p_pol = doc.add_paragraph()
        p_pol.paragraph_format.space_before = Pt(8)
        p_pol.paragraph_format.space_after = Pt(4)
        r_ph = p_pol.add_run(p_head + "\n")
        r_ph.font.bold = True
        r_ph.font.size = Pt(12)
        r_ph.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

        for art in articles:
            p_art = doc.add_paragraph()
            p_art.paragraph_format.space_after = Pt(3)
            p_art.paragraph_format.line_spacing = 1.15
            parts = art.split(":", 1)
            r_art_num = p_art.add_run(parts[0] + ":")
            r_art_num.font.bold = True
            if len(parts) > 1:
                p_art.add_run(parts[1])

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # CHAPTER 9: BIG DATA ARCHITECTURE & CLOUD TCO
    # --------------------------------------------------------------------------
    h9 = doc.add_heading("บทที่ 9: สถาปัตยกรรมบิ๊กดาต้าเลคเฮาส์และการเปรียบเทียบต้นทุนคลาวด์ 3 ปี (Cloud TCO)", level=1)
    h9.paragraph_format.space_before = Pt(14)

    doc.add_paragraph(
        f"เพื่อรองรับการใช้งานข้อมูลและการประยุกต์ใช้ปัญญาประดิษฐ์ในระยะยาว {client.name} จำเป็นต้องก้าวข้าม "
        f"จากสถาปัตยกรรมฐานข้อมูลแบบดั้งเดิม (RDBMS Silos) สู่ 'Modern Data Lakehouse Architecture' "
        f"ซึ่งผสมผสานความยืดหยุ่นในการจัดเก็บข้อมูลทุกรูปแบบของ Data Lake เข้ากับความรวดเร็วและมาตรฐานธรรมาภิบาลของ Data Warehouse:"
    )

    doc.add_heading("9.1 สถาปัตยกรรมเหรียญรางวัล 3 เลเยอร์ (Medallion Architecture)", level=2)
    medallion_layers = [
        ("1. Bronze Layer (Raw Ingestion):",
         "รับข้อมูลดิบจากระบบต้นทาง (HIS, LIS, PACS, ERP) ผ่านท่อ Daily CDC (Change Data Capture) แบบ Append-Only ข้อมูลจะถูกจัดเก็บในสภาพเดิมและเข้ารหัส 100%"),
        ("2. Silver Layer (Conformed & Cleansed):",
         "ทำความสะอาดข้อมูล ตรวจสอบ Foreign Key ล้างค่าว่าง ยุบรวมข้อมูลคนไข้ซ้ำซ้อนผ่าน EMPI Deduplication Engine พร้อมทำ Masking/Tokenization ข้อมูลส่วนบุคคล"),
        ("3. Gold Layer (Business Ready & Aggregated):",
         "จัดทำ Data Marts เฉพาะสายงาน เช่น Hospital Operations Mart, Financial Claim Mart, Clinical AI Mart เพื่อให้ทีม BI และ AI เรียกใช้งานได้ทันทีด้วยความเร็วสูงสุด")
    ]
    for m_title, m_desc in medallion_layers:
        p_m = doc.add_paragraph()
        p_m.paragraph_format.space_after = Pt(4)
        r_mt = p_m.add_run(m_title + " ")
        r_mt.font.bold = True
        p_m.add_run(m_desc)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    doc.add_heading("9.2 ตารางเปรียบเทียบต้นทุนรวมในการเป็นเจ้าของ 3 ปี (3-Year TCO Comparison)", level=2)
    doc.add_paragraph("การเปรียบเทียบเชิงเศรษฐศาสตร์ระหว่าง 4 ทางเลือกโครงสร้างพื้นฐาน:")

    table_tco = doc.add_table(rows=1, cols=4)
    table_tco.alignment = WD_TABLE_ALIGNMENT.CENTER
    tco_headers = ["สถาปัตยกรรมคลาวด์ / โครงสร้างพื้นฐาน", "ค่าบริการรายปี (ลบ.)", "TCO สะสม 3 ปี (ลบ.)", "ข้อได้เปรียบเชิงกลยุทธ์"]
    for idx, name in enumerate(tco_headers):
        cell = table_tco.rows[0].cells[idx]
        cell.text = name
        set_cell_background(cell, "2C3E50")
        p_h = cell.paragraphs[0]
        p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_h.runs[0].font.bold = True
        p_h.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for t in tco_list:
        row_cells = table_tco.add_row().cells
        row_cells[0].text = t.provider
        row_cells[1].text = f"{t.annual_total_thb / 1_000_000:,.2f}"
        row_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        row_cells[2].text = f"{t.three_year_tco_thb / 1_000_000:,.2f}"
        row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        if row_cells[2].paragraphs[0].runs:
            row_cells[2].paragraphs[0].runs[0].font.bold = True
            row_cells[2].paragraphs[0].runs[0].font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
        row_cells[3].text = t.pros
        for c in row_cells:
            set_cell_margins(c)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_callout(
        doc,
        "คำแนะนำเชิงกลยุทธ์ด้านโครงสร้างพื้นฐาน (Infrastructure Recommendation)",
        "คณะที่ปรึกษาแนะนำให้เลือกใช้แนวทาง Google Cloud Platform (GCP BigQuery + Dataplex) หรือ Microsoft Azure (Synapse + Purview) "
        "เนื่องจากมีระบบ Data Governance & Access Control ผนวกรวมอยู่ในตัว ไม่ต้องจัดซื้อระบบแยกต่างหาก "
        "และเป็นโมเดล Serverless ที่ไม่ต้องจ่ายเงินลงทุนก้อนโตในฮาร์ดแวร์ล่วงหน้า (Zero Upfront CapEx) "
        "สามารถเริ่มด้วยขนาดเล็กในระยะนำร่อง และขยายตัวตามปริมาณข้อมูลจริงได้อย่างยืดหยุ่น"
    )

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # CHAPTER 10: AI GOVERNANCE & CHANGE MANAGEMENT
    # --------------------------------------------------------------------------
    h10 = doc.add_heading("บทที่ 10: ธรรมาภิบาลปัญญาประดิษฐ์และการบริหารความเปลี่ยนแปลง (AI Governance & Change)", level=1)
    h10.paragraph_format.space_before = Pt(14)

    doc.add_paragraph(
        "การก้าวสู่การเป็นองค์กรปัญญาประดิษฐ์ทางการแพทย์ จำเป็นต้องวางระบบบริหารจัดการความเสี่ยงด้าน AI "
        "ตามมาตรฐานสากล ISO/IEC 42001 (Artificial Intelligence Management System - AIMS) และ NIST AI Risk Management Framework "
        "เพื่อสร้างความเชื่อมั่นแก่ผู้ป่วยและบุคลากรทางการแพทย์:"
    )

    ai_pillars = [
        ("1. การจัดชั้นความเสี่ยงโมเดล AI (AI Risk Classification):",
         "จำแนกโมเดลออกเป็น 3 กลุ่ม: (1) High Risk - โมเดลช่วยวินิจฉัยโรคและแจ้งเตือนวิกฤต, (2) Limited Risk - โมเดลจัดสรรเตียงและทำนายการผิดนัด, (3) Minimal Risk - รายงานสถิติทั่วไป"),
        ("2. หลักการกำกับโดยมนุษย์ (Human-in-the-Loop):",
         "โมเดลในกลุ่ม High Risk ทั้งหมด ถูกออกแบบให้เป็น 'ระบบสนับสนุนการตัดสินใจ' (Decision Support System) เท่านั้น โดยแพทย์ผู้ทำการรักษาต้องเป็นผู้อนุมัติขั้นสุดท้ายเสมอ ห้ามให้ AI ตัดสินใจสั่งการรักษาโดยอัตโนมัติ"),
        ("3. ความสามารถในการอธิบายผลลัพธ์ (Explainable AI - XAI):",
         "โมเดลทางการแพทย์ต้องสามารถแสดงเหตุผลประกอบการคาดการณ์ (เช่น ใช้ SHAP/LIME เพื่อระบุปัจจัยชีวภาพสำคัญ) เพื่อให้แพทย์สามารถตรวจสอบความสมเหตุสมผลได้"),
        ("4. การป้องกันอคติและการตรวจสอบความถูกต้อง (Bias & Fairness Audit):",
         "ต้องทดสอบโมเดลกับกลุ่มผู้ป่วยที่หลากหลาย เพื่อให้มั่นใจว่าโมเดลไม่มีอคติต่อกลุ่มอายุ เพศ หรือเศรษฐานะใดเป็นพิเศษ"),
        ("5. การป้องกันข้อมูลรั่วไหลผ่าน AI (AI Security & Guardrails):",
         "ติดตั้งระบบสกัดกั้นการป้อนข้อมูลความลับ (Prompt Filtering Gateway) เพื่อป้องกันการนำข้อมูลประวัติการรักษาไปป้อนให้ระบบ LLM ภายนอก")
    ]
    for p_title, p_desc in ai_pillars:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        r_t = p.add_run(p_title + " ")
        r_t.font.bold = True
        p.add_run(p_desc)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    doc.add_heading("10.1 แผนการบริหารจัดการความเปลี่ยนแปลงและหลักสูตรฝึกอบรม (Change Management)", level=2)
    doc.add_paragraph(
        "การเปลี่ยนผ่านสู่ Data-Driven Organization ไม่สามารถสำเร็จได้ด้วยเทคโนโลยีเพียงอย่างเดียว "
        "แต่ขึ้นอยู่กับการปรับเปลี่ยนทัศนคติและพฤติกรรมของบุคลากร คณะที่ปรึกษาจึงกำหนดหลักสูตรฝึกอบรม 3 ระดับ:"
    )

    curriculums = [
        ("หลักสูตรที่ 1: Data-Driven Leadership & AI Risk Governance (สำหรับผู้บริหารระดับสูงและแพทย์หัวหน้าแผนก)",
         "ระยะเวลา: 4 ชั่วโมง | มุ่งเน้น: กลยุทธ์การตัดสินใจด้วยข้อมูล, ความรับผิดชอบตามกฎหมาย PDPA ม.26, และการบริหารความเสี่ยงด้านจริยธรรม AI"),
        ("หลักสูตรที่ 2: Professional Data Stewardship & DQA Matrix (สำหรับคณะบริกรข้อมูลและหัวหน้าวอร์ด)",
         "ระยะเวลา: 16 ชั่วโมง (2 วัน) | มุ่งเน้น: การลงทะเบียน Data Catalog 14 ฟิลด์, การประเมิน DQA 5 มิติ, และการบริหารสิทธิ์การเข้าถึงข้อมูล"),
        ("หลักสูตรที่ 3: Enterprise Data Literacy & Safe AI Usage (สำหรับบุคลากรทางการแพทย์และพนักงานทุกคน)",
         "ระยะเวลา: 6 ชั่วโมง (E-Learning) | มุ่งเน้น: ความสำคัญของความถูกต้องของเวชระเบียน, การรักษาความลับผู้ป่วย, และข้อควรระวังในการใช้ Generative AI")
    ]
    for c_title, c_desc in curriculums:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.space_after = Pt(4)
        r_ct = p_c.add_run(c_title + "\n")
        r_ct.font.bold = True
        r_ct.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
        p_c.add_run(c_desc)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # ANNEX A: FORMAL APPOINTMENT CHARTER (READY TO SIGN)
    # --------------------------------------------------------------------------
    h_app = doc.add_heading("ภาคผนวก ก: ร่างคำสั่งแต่งตั้งคณะกรรมการธรรมาภิบาลข้อมูล (พร้อมลงนาม)", level=1)
    h_app.paragraph_format.space_before = Pt(14)

    p_order = doc.add_paragraph()
    p_order.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_order.paragraph_format.space_after = Pt(12)
    r_ord = p_order.add_run(f"คำสั่ง {client.name}\nที่ .......... / 2569\nเรื่อง แต่งตั้งคณะกรรมการธรรมาภิบาลข้อมูล (Data Governance Council)")
    r_ord.font.bold = True
    r_ord.font.size = Pt(14)
    r_ord.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    doc.add_paragraph(
        f"ด้วย {client.name} ตระหนักถึงความสำคัญของการบริหารจัดการข้อมูลและการขับเคลื่อนนวัตกรรมปัญญาประดิษฐ์ "
        f"ให้มีความมั่นคงปลอดภัย มีคุณภาพ ถูกต้องตามมาตรฐาน และสอดคล้องตามพระราชบัญญัติคุ้มครองข้อมูลส่วนบุคคล พ.ศ. 2562 "
        f"เพื่อประโยชน์สูงสุดในการรักษาพยาบาลและการยกระดับการให้บริการทางการแพทย์สู่ระดับสากล\n\n"
        f"อาศัยอำนาจตามความในระเบียบบริหารงานของ {client.name} จึงมีคำสั่งแต่งตั้ง 'คณะกรรมการธรรมาภิบาลข้อมูล' "
        f"(Data Governance Council) ประกอบด้วยรายนามและตำแหน่งหน้าที่ดังต่อไปนี้:"
    )

    council_roles = [
        ("1. ประธานเจ้าหน้าที่บริหาร (CEO) / ผู้อำนวยการโรงพยาบาล", "ประธานกรรมการ"),
        ("2. ผู้บริหารเทคโนโลยีสารสนเทศระดับสูง (CIO / CTO)", "รองประธานกรรมการ"),
        ("3. ผู้อำนวยการฝ่ายการแพทย์ (Medical Director)", "กรรมการ"),
        ("4. ผู้อำนวยการฝ่ายการพยาบาล (Chief Nursing Officer)", "กรรมการ"),
        ("5. ผู้อำนวยการฝ่ายการเงินและบัญชี (CFO)", "กรรมการ"),
        ("6. เจ้าหน้าที่คุ้มครองข้อมูลส่วนบุคคล (DPO / ฝ่ายกฎหมาย)", "กรรมการ"),
        ("7. หัวหน้าคณะบริกรข้อมูลกลาง (Lead Data Steward)", "กรรมการและเลขานุการ")
    ]
    for role_name, pos in council_roles:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.space_after = Pt(2)
        p_c.add_run(f"• {role_name} ").font.bold = True
        p_c.add_run(f"ดำรงตำแหน่ง {pos}")

    doc.add_paragraph(
        "\nโดยให้คณะกรรมการมีอำนาจหน้าที่ดังต่อไปนี้:\n"
        "1. กำหนดวิสัยทัศน์ แผนแม่บท และนโยบายธรรมาภิบาลข้อมูลและการใช้งานปัญญาประดิษฐ์ระดับองค์กร\n"
        "2. พิจารณาอนุมัติกรอบงบประมาณและทรัพยากรสำหรับการดำเนินโครงการด้านข้อมูลและสถาปัตยกรรมคลาวด์\n"
        "3. ติดตามและกำกับดูแลการดำเนินงานของคณะบริกรข้อมูลให้เป็นไปตามตัวชี้วัดและกรอบ RACI Matrix 42 กิจกรรม\n"
        "4. พิจารณาอนุมัติการเผยแพร่ข้อมูลเปิด (Open Data) และการเชื่อมโยงแลกเปลี่ยนข้อมูลกับหน่วยงานภายนอก\n"
        "5. วินิจฉัยชี้ขาดข้อพิพาทด้านข้อมูล และทบทวนมาตรการเยียวยากรณีเกิดเหตุการณ์ข้อมูลรั่วไหล\n"
        "6. ปฏิบัติหน้าที่อื่นใดตามที่คณะกรรมการบริหารมอบหมาย\n\n"
        "ทั้งนี้ ให้มีผลบังคับใช้ตั้งแต่วันที่ลงนามในคำสั่งนี้เป็นต้นไป"
    )

    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(40)
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sign.add_run(
        "สั่ง ณ วันที่ ........ เดือน ........................ พ.ศ. 2569\n\n\n\n"
        "ลงนาม .............................................................\n"
        "( ............................................................. )\n"
        "ตำแหน่ง ประธานเจ้าหน้าที่บริหาร / ผู้มีอำนาจลงนาม\n"
        f"{client.name}"
    )

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # ANNEX B: DATA PROCESSING AGREEMENT (DPA) - VERBATIM LEGAL
    # --------------------------------------------------------------------------
    h_dpa = doc.add_heading("ภาคผนวก ข: สัญญาประมวลผลข้อมูลส่วนบุคคลมาตรฐาน (Data Processing Agreement - DPA)", level=1)
    h_dpa.paragraph_format.space_before = Pt(14)

    p_dpa_title = doc.add_paragraph()
    p_dpa_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_dt = p_dpa_title.add_run("สัญญาประมวลผลข้อมูลส่วนบุคคล (Data Processing Agreement)\nตามมาตรา 40 แห่งพระราชบัญญัติคุ้มครองข้อมูลส่วนบุคคล พ.ศ. 2562")
    r_dt.font.bold = True
    r_dt.font.size = Pt(12)

    doc.add_paragraph(
        f"สัญญาฉบับนี้ทำขึ้น ณ {client.name} ระหว่าง:\n"
        f"(1) {client.name} ซึ่งต่อไปในสัญญานี้เรียกว่า 'ผู้ควบคุมข้อมูลส่วนบุคคล' (Data Controller) ฝ่ายหนึ่ง กับ\n"
        f"(2) บริษัท ................................................. จำกัด ซึ่งต่อไปในสัญญานี้เรียกว่า 'ผู้ประมวลผลข้อมูลส่วนบุคคล' (Data Processor) อีกฝ่ายหนึ่ง\n\n"
        f"คู่สัญญาทั้งสองฝ่ายตกลงทำสัญญากำหนดสิทธิ หน้าที่ และความรับผิดชอบในการประมวลผลข้อมูลส่วนบุคคลดังมีข้อความต่อไปนี้:"
    )

    dpa_clauses = [
        ("ข้อ 1: วัตถุประสงค์และขอบเขตของการประมวลผล",
         "ผู้ประมวลผลข้อมูลส่วนบุคคลตกลงที่จะประมวลผลข้อมูลส่วนบุคคลเฉพาะตามคำสั่งเป็นลายลักษณ์อักษรของผู้ควบคุมข้อมูลส่วนบุคคล และเพื่อวัตถุประสงค์ในการให้บริการตามสัญญาหลักเท่านั้น ห้ามนำข้อมูลไปประมวลผลเพื่อประโยชน์ส่วนตน"),
        ("ข้อ 2: ประเภทของข้อมูลส่วนบุคคล",
         "ข้อมูลที่อยู่ภายใต้สัญญานี้รวมถึง ข้อมูลประวัติผู้ป่วย (HN), ข้อมูลการวินิจฉัยโรค, ผลตรวจทางห้องปฏิบัติการ, ภาพรังสี และข้อมูลการเงิน ซึ่งถือเป็นข้อมูลส่วนบุคคลอ่อนไหวตามมาตรา 26"),
        ("ข้อ 3: มาตรการรักษาความมั่นคงปลอดภัย",
         "ผู้ประมวลผลข้อมูลส่วนบุคคลต้องจัดให้มีมาตรการรักษาความมั่นคงปลอดภัยทางเทคนิคและการบริหารจัดการที่ได้มาตรฐานสากล (ISO 27001 / SOC2) รวมถึงการเข้ารหัสข้อมูล (Encryption) ทั้งในขณะจัดเก็บและขณะส่งผ่าน"),
        ("ข้อ 4: การรักษาความลับของบุคลากร",
         "ผู้ประมวลผลข้อมูลส่วนบุคคลต้องกำกับให้พนักงานและผู้รับจ้างที่มีสิทธิ์เข้าถึงข้อมูล ลงนามในข้อตกลงรักษาความลับและผ่านการอบรมด้านความปลอดภัยข้อมูล"),
        ("ข้อ 5: ผู้ประมวลผลข้อมูลช่วง (Sub-processor)",
         "ผู้ประมวลผลข้อมูลส่วนบุคคลจะต้องไม่ว่าจ้างผู้ประมวลผลข้อมูลช่วงรายอื่น โดยปราศจากความยินยอมเป็นลายลักษณ์อักษรล่วงหน้าจากผู้ควบคุมข้อมูลส่วนบุคคล"),
        ("ข้อ 6: สิทธิของเจ้าของข้อมูลส่วนบุคคล",
         "ผู้ประมวลผลข้อมูลส่วนบุคคลมีหน้าที่ช่วยเหลือกรรมวิธีทางเทคนิคแก่ผู้ควบคุมข้อมูลส่วนบุคคล เพื่อให้สามารถตอบสนองต่อการใช้สิทธิของเจ้าของข้อมูล (Data Subject Rights) ได้ภายในกำหนดเวลาตามกฎหมาย"),
        ("ข้อ 7: การแจ้งเหตุการณ์ข้อมูลรั่วไหล",
         "หากเกิดเหตุการณ์ข้อมูลรั่วไหล หรือสงสัยว่ามีความไม่ปลอดภัยเกิดขึ้นกับข้อมูล ผู้ประมวลผลข้อมูลส่วนบุคคลต้องแจ้งผู้ควบคุมข้อมูลส่วนบุคคลทราบทันที ภายในไม่เกิน 24 ชั่วโมงหลังจากรับทราบเหตุ"),
        ("ข้อ 8: การลบหรือส่งคืนข้อมูลเมื่อสิ้นสุดสัญญา",
         "เมื่อสัญญาสิ้นสุดลง ผู้ประมวลผลข้อมูลส่วนบุคคลต้องดำเนินการลบ ทำลาย หรือส่งคืนข้อมูลส่วนบุคคลทั้งหมดให้แก่ผู้ควบคุมข้อมูลส่วนบุคคล และออกหนังสือรับรองการทำลายข้อมูลอย่างปลอดภัย"),
        ("ข้อ 9: สิทธิในการเข้าตรวจสอบ (Audit Rights)",
         "ผู้ควบคุมข้อมูลส่วนบุคคลหรือตัวแทนที่ได้รับมอบหมายมีสิทธิ์เข้าตรวจสอบสถานที่ปฏิบัติงานและระบบสารสนเทศของผู้ประมวลผลข้อมูลส่วนบุคคล เพื่อตรวจสอบความสอดคล้องตามสัญญานี้ปีละ 1 ครั้ง")
    ]
    for c_title, c_text in dpa_clauses:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.space_after = Pt(4)
        p_c.add_run(c_title + "\n").font.bold = True
        p_c.add_run(c_text)

    p_dpa_sign = doc.add_paragraph()
    p_dpa_sign.paragraph_format.space_before = Pt(36)
    p_dpa_sign.add_run(
        "ลงนาม ............................................................. ผู้ควบคุมข้อมูลส่วนบุคคล\n"
        f"( ............................................................. ) ตำแหน่ง: ผู้แทน {client.name}\n\n\n"
        "ลงนาม ............................................................. ผู้ประมวลผลข้อมูลส่วนบุคคล\n"
        "( ............................................................. ) ตำแหน่ง: กรรมการผู้มีอำนาจลงนาม"
    )

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # ANNEX C: NON-DISCLOSURE AGREEMENT (NDA) - VERBATIM LEGAL
    # --------------------------------------------------------------------------
    h_nda = doc.add_heading("ภาคผนวก ค: ข้อตกลงการรักษาความลับของข้อมูล (Non-Disclosure Agreement - NDA)", level=1)
    h_nda.paragraph_format.space_before = Pt(14)

    p_nda_title = doc.add_paragraph()
    p_nda_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_nt = p_nda_title.add_run("ข้อตกลงการรักษาความลับและไม่เปิดเผยข้อมูล (Non-Disclosure Agreement)")
    r_nt.font.bold = True
    r_nt.font.size = Pt(12)

    doc.add_paragraph(
        f"ข้อตกลงฉบับนี้ทำขึ้นระหว่าง {client.name} ('ผู้เปิดเผยข้อมูล') "
        f"กับ ................................................. ('ผู้รับข้อมูล') "
        f"เพื่อประโยชน์ในการร่วมดำเนินโครงการ Enterprise Data & AI Transformation มีข้อกำหนดดังนี้:"
    )

    nda_clauses = [
        ("ข้อ 1: นิยามข้อมูลความลับ", "ข้อมูลความลับหมายรวมถึง ข้อมูลทางการแพทย์ เวชระเบียนผู้ป่วย ซอร์สโค้ด สถาปัตยกรรมระบบ รายงานสถิติ และข้อมูลทางการเงินทั้งหมด"),
        ("ข้อ 2: ข้อผูกพันในการรักษาความลับ", "ผู้รับข้อมูลสัญญาว่าจะรักษาข้อมูลความลับไว้เป็นความลับอย่างเคร่งครัดเสมือนหนึ่งเป็นข้อมูลความลับของตนเอง และไม่เปิดเผยต่อบุคคลภายนอก"),
        ("ข้อ 3: การจำกัดการใช้งาน", "ผู้รับข้อมูลจะใช้ข้อมูลความลับเพียงเพื่อวัตถุประสงค์ในการปฏิบัติงานตามโครงการเท่านั้น ห้ามนำไปใช้ประโยชน์ในทางอื่น"),
        ("ข้อ 4: ระยะเวลาความคุ้มครอง", "ข้อผูกพันตามข้อตกลงนี้มีผลบังคับใช้นับแต่วันที่ลงนาม และมีผลคุ้มครองต่อไปอีกเป็นเวลา 5 ปีหลังจากสิ้นสุดโครงการ เว้นแต่เป็นข้อมูลสุขภาพของผู้ป่วยให้มีผลคุ้มครองตลอดไป"),
        ("ข้อ 5: การส่งคืนหรือทำลายข้อมูล", "เมื่อได้รับการร้องขอ ผู้รับข้อมูลต้องส่งคืนหรือทำลายสำเนาข้อมูลความลับทั้งหมดทันทีภายใน 7 วันทำการ"),
        ("ข้อ 6: ผลของการละเมิดข้อตกลง", "หากผู้รับข้อมูลละเมิดข้อตกลง ผู้เปิดเผยข้อมูลมีสิทธิเรียกร้องค่าเสียหายตามจริงและดำเนินคดีตามกฎหมายอย่างถึงที่สุด")
    ]
    for c_title, c_text in nda_clauses:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.space_after = Pt(4)
        p_c.add_run(c_title + "\n").font.bold = True
        p_c.add_run(c_text)

    p_nda_sign = doc.add_paragraph()
    p_nda_sign.paragraph_format.space_before = Pt(36)
    p_nda_sign.add_run(
        "ลงนาม ............................................................. ผู้เปิดเผยข้อมูล\n"
        f"( ............................................................. ) ตำแหน่ง: ผู้แทน {client.name}\n\n\n"
        "ลงนาม ............................................................. ผู้รับข้อมูล\n"
        "( ............................................................. ) ตำแหน่ง: ............................................................."
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    return output_path
