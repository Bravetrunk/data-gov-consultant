"""
Excel Workbook Generator for data-gov-consultant Platform.
Produces publication-grade, multi-tab Excel models with formulas and professional formatting.
"""

import os
from typing import List, Dict, Any
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from models.state import UseCaseItem, RACIItem, MetadataRecord, CloudTCOComparison


def apply_header_style(cell, text, fill_color="1F497D", font_color="FFFFFF"):
    cell.value = text
    cell.font = Font(name="Aptos", size=11, bold=True, color=font_color)
    cell.fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)


def apply_thin_border(cell):
    thin = Side(border_style="thin", color="D3D3D3")
    cell.border = Border(top=thin, left=thin, right=thin, bottom=thin)


def auto_fit_columns(ws, min_width=12, max_width=45):
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or '')
            if len(val_str) > max_len:
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = max(min_width, min(max_len + 3, max_width))


def build_financial_and_tco_workbook(
    output_path: str,
    client_name: str,
    use_cases: List[UseCaseItem],
    tco_list: List[CloudTCOComparison]
) -> str:
    wb = Workbook()

    # Sheet 1: Cover & Summary
    ws_cover = wb.active
    ws_cover.title = "Executive Summary"
    ws_cover.views.sheetView[0].showGridLines = True
    
    ws_cover.merge_cells("B2:G2")
    ws_cover["B2"] = f"EXECUTIVE FINANCIAL & CLOUD TCO REPORT - {client_name.upper()}"
    ws_cover["B2"].font = Font(name="Aptos", size=16, bold=True, color="1F497D")
    
    ws_cover["B4"] = "Prepared by:"
    ws_cover["C4"] = "data-gov-consultant AI-Native Transformation Practice"
    ws_cover["B5"] = "Engagement:"
    ws_cover["C5"] = "Enterprise Big Data, Data Governance & AI Transformation"
    ws_cover["B6"] = "Currency:"
    ws_cover["C6"] = "Thai Baht (THB)"

    for r in range(4, 7):
        ws_cover[f"B{r}"].font = Font(name="Aptos", size=11, bold=True)
        ws_cover[f"C{r}"].font = Font(name="Aptos", size=11)

    # Key Metrics Cards
    ws_cover["B9"] = "Total Identified Use Cases"
    ws_cover["B10"] = f"{len(use_cases)} Use Cases"
    ws_cover["B10"].font = Font(name="Aptos", size=18, bold=True, color="1F497D")

    ws_cover["D9"] = "Total Expected 3-Yr Benefits"
    ws_cover["D10"] = "=SUM('Use-Case Prioritization & ROI'!F4:F20)*3"
    ws_cover["D10"].number_format = "#,##0"
    ws_cover["D10"].font = Font(name="Aptos", size=18, bold=True, color="27AE60")

    ws_cover["F9"] = "Average Payback Period"
    ws_cover["F10"] = "=AVERAGE('Use-Case Prioritization & ROI'!H4:H20)"
    ws_cover["F10"].number_format = "0.0 'Months'"
    ws_cover["F10"].font = Font(name="Aptos", size=18, bold=True, color="D35400")

    # Sheet 2: Use Cases & ROI
    ws_roi = wb.create_sheet(title="Use-Case Prioritization & ROI")
    ws_roi.views.sheetView[0].showGridLines = True
    headers_roi = [
        "Use Case ID", "Use Case Title", "Business Unit", "Impact (1-5)",
        "Feasibility (1-5)", "Annual Benefit (THB)", "Implementation Cost (THB)",
        "Payback (Months)", "Priority Tier", "Required Datasets"
    ]
    for col_idx, h in enumerate(headers_roi, 1):
        cell = ws_roi.cell(row=3, column=col_idx)
        apply_header_style(cell, h, fill_color="1F497D")

    for i, uc in enumerate(use_cases, start=4):
        ws_roi.cell(row=i, column=1, value=uc.id).alignment = Alignment(horizontal="center")
        ws_roi.cell(row=i, column=2, value=uc.title)
        ws_roi.cell(row=i, column=3, value=uc.business_unit)
        ws_roi.cell(row=i, column=4, value=uc.impact_score).alignment = Alignment(horizontal="center")
        ws_roi.cell(row=i, column=5, value=uc.feasibility_score).alignment = Alignment(horizontal="center")
        
        # Numbers
        c_benefit = ws_roi.cell(row=i, column=6, value=uc.estimated_annual_benefit_thb)
        c_benefit.number_format = "#,##0"
        c_cost = ws_roi.cell(row=i, column=7, value=uc.implementation_cost_thb)
        c_cost.number_format = "#,##0"
        
        # Formula for Payback: =(Cost / Benefit) * 12
        c_payback = ws_roi.cell(row=i, column=8, value=f"=ROUND((G{i}/F{i})*12, 1)")
        c_payback.number_format = "0.0"
        c_payback.alignment = Alignment(horizontal="center")

        ws_roi.cell(row=i, column=9, value=uc.priority_tier).alignment = Alignment(horizontal="center")
        ws_roi.cell(row=i, column=10, value=", ".join(uc.required_datasets))

        for c in range(1, 11):
            apply_thin_border(ws_roi.cell(row=i, column=c))

    # Total row for ROI
    last_row = 3 + len(use_cases)
    tot_row = last_row + 1
    ws_roi.cell(row=tot_row, column=3, value="Total / Weighted Avg:").font = Font(name="Aptos", bold=True)
    ws_roi.cell(row=tot_row, column=6, value=f"=SUM(F4:F{last_row})").number_format = "#,##0"
    ws_roi.cell(row=tot_row, column=6).font = Font(name="Aptos", bold=True)
    ws_roi.cell(row=tot_row, column=7, value=f"=SUM(G4:G{last_row})").number_format = "#,##0"
    ws_roi.cell(row=tot_row, column=7).font = Font(name="Aptos", bold=True)
    ws_roi.cell(row=tot_row, column=8, value=f"=ROUND((G{tot_row}/F{tot_row})*12, 1)").number_format = "0.0"
    ws_roi.cell(row=tot_row, column=8).font = Font(name="Aptos", bold=True)

    # Sheet 3: Cloud TCO
    ws_tco = wb.create_sheet(title="Cloud TCO 3-Year Model")
    ws_tco.views.sheetView[0].showGridLines = True
    headers_tco = [
        "Infrastructure Architecture", "Storage (Monthly)", "Compute (Monthly)",
        "Network/Egress (Monthly)", "Licensing/Tools (Monthly)", "Annual TCO (THB)",
        "3-Year Total TCO (THB)", "Architectural Advantages", "Key Considerations"
    ]
    for col_idx, h in enumerate(headers_tco, 1):
        cell = ws_tco.cell(row=3, column=col_idx)
        apply_header_style(cell, h, fill_color="2C3E50")

    for i, t in enumerate(tco_list, start=4):
        ws_tco.cell(row=i, column=1, value=t.provider).font = Font(name="Aptos", bold=True)
        ws_tco.cell(row=i, column=2, value=t.storage_monthly_thb).number_format = "#,##0"
        ws_tco.cell(row=i, column=3, value=t.compute_monthly_thb).number_format = "#,##0"
        ws_tco.cell(row=i, column=4, value=t.network_monthly_thb).number_format = "#,##0"
        ws_tco.cell(row=i, column=5, value=t.license_monthly_thb).number_format = "#,##0"
        
        # Formulas
        ws_tco.cell(row=i, column=6, value=f"=SUM(B{i}:E{i})*12").number_format = "#,##0"
        ws_tco.cell(row=i, column=7, value=f"=F{i}*3").number_format = "#,##0"
        ws_tco.cell(row=i, column=7).font = Font(name="Aptos", bold=True, color="1F497D")
        
        ws_tco.cell(row=i, column=8, value=t.pros)
        ws_tco.cell(row=i, column=9, value=t.cons)

        for c in range(1, 10):
            apply_thin_border(ws_tco.cell(row=i, column=c))

    auto_fit_columns(ws_cover)
    auto_fit_columns(ws_roi)
    auto_fit_columns(ws_tco)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wb.save(output_path)
    return output_path


def build_governance_and_catalog_workbook(
    output_path: str,
    client_name: str,
    raci_items: List[RACIItem],
    catalog_items: List[MetadataRecord]
) -> str:
    wb = Workbook()

    # Sheet 1: Cover
    ws_cover = wb.active
    ws_cover.title = "Overview & Operating Model"
    ws_cover.views.sheetView[0].showGridLines = True
    
    ws_cover.merge_cells("B2:H2")
    ws_cover["B2"] = f"DATA GOVERNANCE OPERATING MODEL & DATA CATALOG - {client_name.upper()}"
    ws_cover["B2"].font = Font(name="Aptos", size=15, bold=True, color="1F497D")

    ws_cover["B4"] = "Standards Grounding:"
    ws_cover["C4"] = "DGA Thailand, DAMA-DMBOK, PDPA B.E. 2562, ISO/IEC 42001"
    ws_cover["B5"] = "Catalog Schema:"
    ws_cover["C5"] = "14 Mandatory Metadata Fields (สพร./DGA Standard)"
    ws_cover["B6"] = "Governance Structure:"
    ws_cover["C6"] = "Data Governance Council + Data Steward Network + Custodians"

    # Sheet 2: RACI Matrix
    ws_raci = wb.create_sheet(title="40+ Activity RACI Matrix")
    ws_raci.views.sheetView[0].showGridLines = True
    raci_headers = [
        "Task ID", "Category / Lifecycle", "Activity Name",
        "Data Governance Council", "Lead Data Steward", "Data Owner (Business)",
        "Data Steward Team", "Data Custodian (IT)", "Data Creator", "Data User", "DPO / Legal"
    ]
    for col_idx, h in enumerate(raci_headers, 1):
        cell = ws_raci.cell(row=3, column=col_idx)
        apply_header_style(cell, h, fill_color="1F497D")

    for i, r in enumerate(raci_items, start=4):
        ws_raci.cell(row=i, column=1, value=r.task_id).alignment = Alignment(horizontal="center")
        ws_raci.cell(row=i, column=2, value=r.category).alignment = Alignment(horizontal="center")
        ws_raci.cell(row=i, column=3, value=r.activity_name)
        
        roles = [
            r.data_council, r.lead_data_steward, r.data_owner,
            r.data_steward_team, r.data_custodian_it, r.data_creator,
            r.data_user, r.dpo_legal
        ]
        for c_idx, val in enumerate(roles, 4):
            c_cell = ws_raci.cell(row=i, column=c_idx, value=val)
            c_cell.alignment = Alignment(horizontal="center")
            if val == "A":
                c_cell.fill = PatternFill(start_color="FADBD8", end_color="FADBD8", fill_type="solid")  # Light red
                c_cell.font = Font(name="Aptos", bold=True, color="78281F")
            elif val == "R":
                c_cell.fill = PatternFill(start_color="D4EFDF", end_color="D4EFDF", fill_type="solid")  # Light green
                c_cell.font = Font(name="Aptos", bold=True, color="145A32")

        for c in range(1, 12):
            apply_thin_border(ws_raci.cell(row=i, column=c))

    # Sheet 3: Data Catalog (14 DGA Fields)
    ws_cat = wb.create_sheet(title="Data Catalog (14 DGA Fields)")
    ws_cat.views.sheetView[0].showGridLines = True
    cat_headers = [
        "No.", "Dataset Title (ชื่อชุดข้อมูล)", "Owner Org (องค์กร)", "Maintainer (ผู้ติดต่อ)",
        "Maintainer Email", "Keywords (คำสำคัญ)", "Notes (คำอธิบาย)", "Objective (วัตถุประสงค์)",
        "Frequency", "Geo Coverage", "Data Source", "Format", "Classification Level",
        "License", "Quality Score (%)"
    ]
    for col_idx, h in enumerate(cat_headers, 1):
        cell = ws_cat.cell(row=3, column=col_idx)
        apply_header_style(cell, h, fill_color="27AE60")

    for i, m in enumerate(catalog_items, start=4):
        ws_cat.cell(row=i, column=1, value=m.no).alignment = Alignment(horizontal="center")
        ws_cat.cell(row=i, column=2, value=m.title).font = Font(name="Aptos", bold=True)
        ws_cat.cell(row=i, column=3, value=m.owner_org)
        ws_cat.cell(row=i, column=4, value=m.maintainer)
        ws_cat.cell(row=i, column=5, value=m.maintainer_email)
        ws_cat.cell(row=i, column=6, value=m.tag_string)
        ws_cat.cell(row=i, column=7, value=m.notes)
        ws_cat.cell(row=i, column=8, value=m.objective)
        ws_cat.cell(row=i, column=9, value=m.update_frequency).alignment = Alignment(horizontal="center")
        ws_cat.cell(row=i, column=10, value=m.geo_coverage)
        ws_cat.cell(row=i, column=11, value=m.data_source)
        ws_cat.cell(row=i, column=12, value=m.data_format).alignment = Alignment(horizontal="center")
        ws_cat.cell(row=i, column=13, value=m.classification_level)
        ws_cat.cell(row=i, column=14, value=m.license_id)
        
        q_cell = ws_cat.cell(row=i, column=15, value=m.data_quality_score)
        q_cell.number_format = "0.0'%'"
        q_cell.alignment = Alignment(horizontal="center")
        if m.data_quality_score >= 80.0:
            q_cell.font = Font(name="Aptos", bold=True, color="27AE60")
        else:
            q_cell.font = Font(name="Aptos", bold=True, color="C0392B")

        for c in range(1, 16):
            apply_thin_border(ws_cat.cell(row=i, column=c))

    # Sheet 4: Data Quality 5-Dimension Evaluation
    ws_dq = wb.create_sheet(title="Data Quality 5D Evaluation")
    ws_dq.views.sheetView[0].showGridLines = True
    dq_headers = [
        "Dimension", "Thai Definition", "Standard Weight",
        "Target Dataset 1 Score", "Target Dataset 2 Score", "Weighted Overall", "Remediation Guidance"
    ]
    for col_idx, h in enumerate(dq_headers, 1):
        cell = ws_dq.cell(row=3, column=col_idx)
        apply_header_style(cell, h, fill_color="8E44AD")

    dq_rows = [
        ("Accuracy & Completeness", "ความถูกต้องและสมบูรณ์", 0.25, 92.5, 88.0, "=D4*C4", "ทำ Automated Null Check และ Foreign Key Integrity ใน ETL"),
        ("Consistency", "ความสอดคล้องกัน", 0.20, 85.0, 90.0, "=D5*C5", "ปรับมาตรฐานรหัสอ้างอิงให้ตรงกับ Master Data และรหัสสากล"),
        ("Timeliness", "ความเป็นปัจจุบัน", 0.20, 95.0, 80.0, "=D6*C6", "ย้ายจาก Batch สิ้นเดือนเป็น Daily CDC Pipeline ผ่าน Kafka/Airflow"),
        ("Relevancy", "ตรงตามความต้องการ", 0.15, 90.0, 95.0, "=D7*C7", "ตัดฟิลด์ Unused ออกจากรายงานเพื่อลด Overhead ของฐานข้อมูล"),
        ("Availability", "ความพร้อมใช้งาน", 0.20, 94.0, 85.0, "=D8*C8", "เปิดบริการผ่าน REST API / Data Lakehouse สำหรับทีม AI")
    ]
    for idx, r_data in enumerate(dq_rows, start=4):
        for c_idx, val in enumerate(r_data, start=1):
            cell = ws_dq.cell(row=idx, column=c_idx, value=val)
            if c_idx == 3:
                cell.number_format = "0.0%"
                cell.alignment = Alignment(horizontal="center")
            elif c_idx in [4, 5]:
                cell.number_format = "0.0"
                cell.alignment = Alignment(horizontal="center")
            elif c_idx == 6:
                cell.number_format = "0.0"
                cell.alignment = Alignment(horizontal="center")
                cell.font = Font(name="Aptos", bold=True)
            apply_thin_border(cell)

    # Summary Row for DQ
    ws_dq.cell(row=9, column=2, value="Weighted Total Score:").font = Font(name="Aptos", bold=True)
    ws_dq.cell(row=9, column=3, value="=SUM(C4:C8)").number_format = "0.0%"
    ws_dq.cell(row=9, column=3).font = Font(name="Aptos", bold=True)
    ws_dq.cell(row=9, column=6, value="=SUM(F4:F8)").number_format = "0.0"
    ws_dq.cell(row=9, column=6).font = Font(name="Aptos", bold=True, size=12, color="27AE60")

    auto_fit_columns(ws_cover)
    auto_fit_columns(ws_raci)
    auto_fit_columns(ws_cat)
    auto_fit_columns(ws_dq)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wb.save(output_path)
    return output_path
