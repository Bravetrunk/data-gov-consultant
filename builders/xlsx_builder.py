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


def apply_header_style(cell, text, fill_color="1F497D", font_color="FFFFFF", font_size=11):
    cell.value = text
    cell.font = Font(name="Aptos", size=font_size, bold=True, color=font_color)
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


# ==============================================================================
# WORKBOOK 1: FINANCIAL ROI & CLOUD TCO MODEL
# ==============================================================================

def build_financial_and_tco_workbook(
    output_path: str,
    client_name: str,
    use_cases: List[UseCaseItem],
    tco_list: List[CloudTCOComparison]
) -> str:
    wb = Workbook()

    # --------------------------------------------------------------------------
    # Sheet 1: Cover & Summary
    # --------------------------------------------------------------------------
    ws_cover = wb.active
    ws_cover.title = "Executive Summary"
    ws_cover.views.sheetView[0].showGridLines = True

    ws_cover.merge_cells("B2:H2")
    ws_cover["B2"] = f"EXECUTIVE FINANCIAL & CLOUD TCO REPORT - {client_name.upper()}"
    ws_cover["B2"].font = Font(name="Aptos", size=16, bold=True, color="1F497D")

    ws_cover["B4"] = "Prepared by:"
    ws_cover["C4"] = "data-gov-consultant AI-Native Transformation Practice"
    ws_cover["B5"] = "Engagement:"
    ws_cover["C5"] = "Enterprise Big Data, Data Governance & AI Transformation"
    ws_cover["B6"] = "Methodology:"
    ws_cover["C6"] = "Business-First Value Modeling (2x2 Impact Matrix & 3-Year TCO)"
    ws_cover["B7"] = "Currency:"
    ws_cover["C7"] = "Thai Baht (THB)"

    for r in range(4, 8):
        ws_cover[f"B{r}"].font = Font(name="Aptos", size=11, bold=True)
        ws_cover[f"C{r}"].font = Font(name="Aptos", size=11)

    # Key Metrics Cards
    ws_cover["B10"] = "Total Prioritized Use Cases"
    ws_cover["B11"] = f"{len(use_cases)} Use Cases"
    ws_cover["B11"].font = Font(name="Aptos", size=18, bold=True, color="1F497D")

    ws_cover["D10"] = "Total Expected 3-Yr Benefits"
    ws_cover["D11"] = f"=SUM('Use-Case Prioritization & ROI'!F4:F{len(use_cases)+3})*3"
    ws_cover["D11"].number_format = "#,##0"
    ws_cover["D11"].font = Font(name="Aptos", size=18, bold=True, color="27AE60")

    ws_cover["F10"] = "Average Payback Period"
    ws_cover["F11"] = f"=AVERAGE('Use-Case Prioritization & ROI'!H4:H{len(use_cases)+3})"
    ws_cover["F11"].number_format = "0.0 'Months'"
    ws_cover["F11"].font = Font(name="Aptos", size=18, bold=True, color="D35400")

    ws_cover["H10"] = "3-Year Cloud TCO (Recommended)"
    ws_cover["H11"] = "='Cloud TCO 3-Year Model'!G4"
    ws_cover["H11"].number_format = "#,##0"
    ws_cover["H11"].font = Font(name="Aptos", size=18, bold=True, color="2980B9")

    # Table of Contents in Cover
    ws_cover["B14"] = "WORKBOOK STRUCTURE & DESCRIPTIONS:"
    ws_cover["B14"].font = Font(name="Aptos", size=12, bold=True, color="1F497D")
    
    sheets_info = [
        ("1. Executive Summary", "ภาพรวมผลประโยชน์ทางการเงิน ดัชนีชี้วัดความคุ้มค่า และสรุปสำหรับคณะกรรมการ"),
        ("2. Use-Case Prioritization & ROI", "พอร์ตโฟลิโอ 10 ยูสเคสธุรกิจ พร้อมสูตรคำนวณผลประโยชน์ ต้นทุน และระยะเวลาคืนทุน"),
        ("3. 36-Month Cashflow Projection", "แบบจำลองกระแสเงินสดสุทธิรายไตรมาส 3 ปี (Capex, Opex, Ramp-up Benefits, Cumulative Cash)"),
        ("4. Cloud TCO 3-Year Model", "การเปรียบเทียบต้นทุนรวมในการเป็นเจ้าของ (TCO) ระหว่าง GCP, AWS, Azure และ On-Premise"),
        ("5. TCO Sensitivity Analysis", "แบบจำลองความอ่อนไหวต่อปริมาณข้อมูลและการขยายตัวของการใช้งาน (Workload Scenarios)")
    ]
    for idx, (title, desc) in enumerate(sheets_info, start=15):
        ws_cover[f"B{idx}"] = title
        ws_cover[f"B{idx}"].font = Font(name="Aptos", bold=True)
        ws_cover[f"D{idx}"] = desc
        ws_cover[f"D{idx}"].font = Font(name="Aptos", italic=True)

    # --------------------------------------------------------------------------
    # Sheet 2: Use Cases & ROI
    # --------------------------------------------------------------------------
    ws_roi = wb.create_sheet(title="Use-Case Prioritization & ROI")
    ws_roi.views.sheetView[0].showGridLines = True
    headers_roi = [
        "Use Case ID", "Use Case Title", "Business Unit", "Impact (1-5)",
        "Feasibility (1-5)", "Annual Benefit (THB)", "Implementation Cost (THB)",
        "Payback (Months)", "3-Year Net Profit (THB)", "Priority Tier", "Required Datasets"
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

        # Formula for 3-Year Net Profit: =(Benefit * 3) - Cost
        c_net3 = ws_roi.cell(row=i, column=9, value=f"=(F{i}*3)-G{i}")
        c_net3.number_format = "#,##0"
        c_net3.font = Font(name="Aptos", color="145A32")

        c_tier = ws_roi.cell(row=i, column=10, value=uc.priority_tier)
        c_tier.alignment = Alignment(horizontal="center")
        if uc.priority_tier == "Quick Win":
            c_tier.fill = PatternFill(start_color="D4EFDF", end_color="D4EFDF", fill_type="solid")
            c_tier.font = Font(name="Aptos", bold=True, color="145A32")
        else:
            c_tier.fill = PatternFill(start_color="FCF3CF", end_color="FCF3CF", fill_type="solid")
            c_tier.font = Font(name="Aptos", bold=True, color="7D6608")

        ws_roi.cell(row=i, column=11, value=", ".join(uc.required_datasets))

        for c in range(1, 12):
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
    ws_roi.cell(row=tot_row, column=9, value=f"=SUM(I4:I{last_row})").number_format = "#,##0"
    ws_roi.cell(row=tot_row, column=9).font = Font(name="Aptos", bold=True, color="145A32")
    for c in range(1, 12):
        apply_thin_border(ws_roi.cell(row=tot_row, column=c))

    # --------------------------------------------------------------------------
    # Sheet 3: 36-Month Cashflow Projection
    # --------------------------------------------------------------------------
    ws_cf = wb.create_sheet(title="36-Month Cashflow Projection")
    ws_cf.views.sheetView[0].showGridLines = True

    cf_headers = [
        "Financial Cashflow Item",
        "Y1-Q1", "Y1-Q2", "Y1-Q3", "Y1-Q4",
        "Y2-Q1", "Y2-Q2", "Y2-Q3", "Y2-Q4",
        "Y3-Q1", "Y3-Q2", "Y3-Q3", "Y3-Q4",
        "3-Year Total (THB)"
    ]
    for col_idx, h in enumerate(cf_headers, 1):
        cell = ws_cf.cell(row=3, column=col_idx)
        apply_header_style(cell, h, fill_color="2C3E50")

    ws_cf.cell(row=4, column=1, value="CapEx: Initial Architecture & Pilot Implementation").font = Font(name="Aptos", bold=True)
    capex_vals = [2_500_000, 3_000_000, 1_800_000, 800_000, 400_000, 300_000, 200_000, 150_000, 100_000, 100_000, 100_000, 100_000]
    for idx, v in enumerate(capex_vals, start=2):
        c = ws_cf.cell(row=4, column=idx, value=v)
        c.number_format = "#,##0"
    ws_cf.cell(row=4, column=14, value="=SUM(B4:M4)").number_format = "#,##0"

    ws_cf.cell(row=5, column=1, value="OpEx: Cloud Data Lakehouse & Software Licenses").font = Font(name="Aptos", bold=True)
    opex_cloud = [150_000, 250_000, 450_000, 540_000, 540_000, 540_000, 540_000, 540_000, 560_000, 560_000, 560_000, 560_000]
    for idx, v in enumerate(opex_cloud, start=2):
        c = ws_cf.cell(row=5, column=idx, value=v)
        c.number_format = "#,##0"
    ws_cf.cell(row=5, column=14, value="=SUM(B5:M5)").number_format = "#,##0"

    ws_cf.cell(row=6, column=1, value="OpEx: Data Governance Team & Engineering Support").font = Font(name="Aptos", bold=True)
    opex_team = [300_000, 450_000, 600_000, 600_000, 650_000, 650_000, 650_000, 650_000, 700_000, 700_000, 700_000, 700_000]
    for idx, v in enumerate(opex_team, start=2):
        c = ws_cf.cell(row=6, column=idx, value=v)
        c.number_format = "#,##0"
    ws_cf.cell(row=6, column=14, value="=SUM(B6:M6)").number_format = "#,##0"

    ws_cf.cell(row=7, column=1, value="TOTAL OUTFLOWS (Cash Cost)").font = Font(name="Aptos", bold=True, color="C0392B")
    for col in range(2, 14):
        col_let = get_column_letter(col)
        c = ws_cf.cell(row=7, column=col, value=f"=SUM({col_let}4:{col_let}6)")
        c.number_format = "#,##0"
        c.font = Font(name="Aptos", bold=True, color="C0392B")
    ws_cf.cell(row=7, column=14, value="=SUM(N4:N6)").number_format = "#,##0"
    ws_cf.cell(row=7, column=14).font = Font(name="Aptos", bold=True, color="C0392B")

    # Inflows (Realized Benefits from 10 Use Cases)
    ws_cf.cell(row=8, column=1, value="INFLOWS: Realized Business Benefits & Cost Savings").font = Font(name="Aptos", bold=True, color="27AE60")
    benefit_ramp = [0, 1_500_000, 6_000_000, 12_000_000, 18_000_000, 21_000_000, 22_000_000, 22_500_000, 23_000_000, 23_000_000, 23_000_000, 23_000_000]
    for idx, v in enumerate(benefit_ramp, start=2):
        c = ws_cf.cell(row=8, column=idx, value=v)
        c.number_format = "#,##0"
        c.font = Font(name="Aptos", bold=True, color="27AE60")
    ws_cf.cell(row=8, column=14, value="=SUM(B8:M8)").number_format = "#,##0"
    ws_cf.cell(row=8, column=14).font = Font(name="Aptos", bold=True, color="27AE60")

    # Net Quarterly Cashflow: Row 8 - Row 7
    ws_cf.cell(row=9, column=1, value="NET QUARTERLY CASHFLOW").font = Font(name="Aptos", bold=True)
    for col in range(2, 14):
        col_let = get_column_letter(col)
        c = ws_cf.cell(row=9, column=col, value=f"={col_let}8-{col_let}7")
        c.number_format = "#,##0"
        c.font = Font(name="Aptos", bold=True)
    ws_cf.cell(row=9, column=14, value="=N8-N7").number_format = "#,##0"
    ws_cf.cell(row=9, column=14).font = Font(name="Aptos", bold=True)

    # Cumulative Cashflow
    ws_cf.cell(row=10, column=1, value="CUMULATIVE NET CASHFLOW (Breakeven Tracking)").font = Font(name="Aptos", bold=True, color="1F497D")
    ws_cf.cell(row=10, column=2, value="=B9").number_format = "#,##0"
    for col in range(3, 14):
        col_prev = get_column_letter(col - 1)
        col_curr = get_column_letter(col)
        c = ws_cf.cell(row=10, column=col, value=f"={col_prev}10+{col_curr}9")
        c.number_format = "#,##0"
        c.font = Font(name="Aptos", bold=True, color="1F497D")
    ws_cf.cell(row=10, column=14, value="=M10").number_format = "#,##0"
    ws_cf.cell(row=10, column=14).font = Font(name="Aptos", bold=True, size=12, color="27AE60")

    for r in range(4, 11):
        for c in range(1, 15):
            apply_thin_border(ws_cf.cell(row=r, column=c))

    # --------------------------------------------------------------------------
    # Sheet 4: Cloud TCO
    # --------------------------------------------------------------------------
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

    # --------------------------------------------------------------------------
    # Sheet 5: TCO Sensitivity Analysis
    # --------------------------------------------------------------------------
    ws_sens = wb.create_sheet(title="TCO Sensitivity Analysis")
    ws_sens.views.sheetView[0].showGridLines = True

    sens_headers = [
        "Workload Scaling Scenario", "Data Volume (TB)", "Monthly Queries (M)",
        "GCP Monthly (THB)", "AWS Monthly (THB)", "Azure Monthly (THB)", "On-Prem Monthly (THB)",
        "Recommended Strategy"
    ]
    for col_idx, h in enumerate(sens_headers, 1):
        cell = ws_sens.cell(row=3, column=col_idx)
        apply_header_style(cell, h, fill_color="34495E")

    sens_rows = [
        ("Base Case (Year 1 Pilot)", 10, 1.5, 180_000, 195_000, 199_000, 160_000, "Serverless GCP/AWS เริ่มต้นได้ทันทีไม่มี CapEx ล่วงหน้า"),
        ("Moderate Growth (Year 2 Scaling)", 35, 5.0, 310_000, 335_000, 340_000, 240_000, "ตั้ง Alert Quota และทำ Data Partitioning เพื่อคุมต้นทุน Query"),
        ("High Expansion (Year 3 Multi-Hospital)", 100, 18.0, 680_000, 720_000, 740_000, 480_000, "พิจารณา Reserved Capacity / Savings Plans เพื่อรับส่วนลด 30-40%")
    ]
    for idx, r_data in enumerate(sens_rows, start=4):
        for c_idx, val in enumerate(r_data, start=1):
            c = ws_sens.cell(row=idx, column=c_idx, value=val)
            if c_idx in [2, 3]:
                c.number_format = "#,##0.0"
                c.alignment = Alignment(horizontal="center")
            elif c_idx in [4, 5, 6, 7]:
                c.number_format = "#,##0"
                c.alignment = Alignment(horizontal="right")
            apply_thin_border(c)

    auto_fit_columns(ws_cover)
    auto_fit_columns(ws_roi)
    auto_fit_columns(ws_cf)
    auto_fit_columns(ws_tco)
    auto_fit_columns(ws_sens)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wb.save(output_path)
    return output_path


# ==============================================================================
# WORKBOOK 2: GOVERNANCE RACI & DATA CATALOG
# ==============================================================================

def build_governance_and_catalog_workbook(
    output_path: str,
    client_name: str,
    raci_items: List[RACIItem],
    catalog_items: List[MetadataRecord]
) -> str:
    wb = Workbook()

    # --------------------------------------------------------------------------
    # Sheet 1: Cover & Operating Model
    # --------------------------------------------------------------------------
    ws_cover = wb.active
    ws_cover.title = "Overview & Operating Model"
    ws_cover.views.sheetView[0].showGridLines = True

    ws_cover.merge_cells("B2:I2")
    ws_cover["B2"] = f"DATA GOVERNANCE OPERATING MODEL & DATA CATALOG - {client_name.upper()}"
    ws_cover["B2"].font = Font(name="Aptos", size=15, bold=True, color="1F497D")

    ws_cover["B4"] = "Standards Grounding:"
    ws_cover["C4"] = "DGA Thailand Framework, DAMA-DMBOK2, PDPA B.E. 2562, ISO/IEC 42001:2023"
    ws_cover["B5"] = "Catalog Schema:"
    ws_cover["C5"] = "14 Mandatory Metadata Fields (สพร./DGA National Standard)"
    ws_cover["B6"] = "Governance Tiers:"
    ws_cover["C6"] = "1. Council (Strategic) -> 2. Data Stewards (Tactical) -> 3. Custodians/Users (Operational)"
    ws_cover["B7"] = "Scope of Governance:"
    ws_cover["C7"] = f"{len(raci_items)} RACI Activities across 9 Lifecycle Domains | {len(catalog_items)} Key Registered Datasets"

    for r in range(4, 8):
        ws_cover[f"B{r}"].font = Font(name="Aptos", size=11, bold=True)
        ws_cover[f"C{r}"].font = Font(name="Aptos", size=11)

    # Summary Cards
    ws_cover["B10"] = "Governed RACI Activities"
    ws_cover["B11"] = f"{len(raci_items)} Activities"
    ws_cover["B11"].font = Font(name="Aptos", size=18, bold=True, color="1F497D")

    ws_cover["E10"] = "Cataloged Datasets"
    ws_cover["E11"] = f"{len(catalog_items)} Datasets"
    ws_cover["E11"].font = Font(name="Aptos", size=18, bold=True, color="27AE60")

    ws_cover["H10"] = "DQ Operational Checks"
    ws_cover["H11"] = "24 Audit Points"
    ws_cover["H11"].font = Font(name="Aptos", size=18, bold=True, color="8E44AD")

    # Sheet Guide
    ws_cover["B14"] = "WORKBOOK SHEETS DIRECTORY:"
    ws_cover["B14"].font = Font(name="Aptos", size=12, bold=True, color="1F497D")
    
    sheets_dir = [
        ("1. Overview & Operating Model", "โครงสร้างการกำกับดูแล 3 ระดับ และคำอธิบายบทบาทอำนาจหน้าที่"),
        ("2. 42 Activity RACI Matrix", "เมทริกซ์ RACI ฉบับสมบูรณ์ 42 กิจกรรม ครอบคลุม 9 หมวดวงจรชีวิตข้อมูล"),
        ("3. Data Catalog (14 DGA Fields)", "บัญชีข้อมูลองค์กรตามมาตรฐาน สพร. 14 รายการ ครบทุกชุดข้อมูลสำคัญ"),
        ("4. Data Quality 5D Evaluation", "เมทริกซ์ประเมินคุณภาพข้อมูล 5 มิติ พร้อมเกณฑ์ถ่วงน้ำหนักและสูตรคำนวณ"),
        ("5. DQA Operational Audit Checklist", "เช็กลิสต์การตรวจประเมินคุณภาพข้อมูลภาคปฏิบัติ 24 ข้อ (Operational Audit)"),
        ("6. Data Governance Controls (DGC)", "การควบคุมความมั่นคงปลอดภัยและความเสี่ยงของข้อมูล 15 จุดสำคัญ")
    ]
    for idx, (s_title, s_desc) in enumerate(sheets_dir, start=15):
        ws_cover[f"B{idx}"] = s_title
        ws_cover[f"B{idx}"].font = Font(name="Aptos", bold=True)
        ws_cover[f"D{idx}"] = s_desc
        ws_cover[f"D{idx}"].font = Font(name="Aptos", italic=True)

    # --------------------------------------------------------------------------
    # Sheet 2: RACI Matrix (42 Activities)
    # --------------------------------------------------------------------------
    ws_raci = wb.create_sheet(title="42 Activity RACI Matrix")
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
            elif val == "C":
                c_cell.fill = PatternFill(start_color="FCF3CF", end_color="FCF3CF", fill_type="solid")  # Light yellow
                c_cell.font = Font(name="Aptos", bold=True, color="7D6608")
            elif val == "S":
                c_cell.fill = PatternFill(start_color="E8F8F5", end_color="E8F8F5", fill_type="solid")  # Soft teal
                c_cell.font = Font(name="Aptos", bold=True, color="0E6251")
            elif val == "I":
                c_cell.fill = PatternFill(start_color="F2F4F4", end_color="F2F4F4", fill_type="solid")  # Soft gray
                c_cell.font = Font(name="Aptos", color="5D6D7E")

        for c in range(1, 12):
            apply_thin_border(ws_raci.cell(row=i, column=c))

    # --------------------------------------------------------------------------
    # Sheet 3: Data Catalog (14 DGA Fields - 12 Datasets)
    # --------------------------------------------------------------------------
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

    # --------------------------------------------------------------------------
    # Sheet 4: Data Quality 5-Dimension Evaluation
    # --------------------------------------------------------------------------
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
        ("Consistency", "ความสอดคล้องกัน", 0.20, 85.0, 90.0, "=D5*C5", "ปรับมาตรฐานรหัสอ้างอิงให้ตรงกับ Master Data และรหัสสากล (ICD-10, TMT)"),
        ("Timeliness", "ความเป็นปัจจุบัน", 0.20, 95.0, 80.0, "=D6*C6", "ย้ายจาก Batch สิ้นเดือนเป็น Daily CDC Pipeline ผ่าน Kafka/Debezium"),
        ("Relevancy", "ตรงตามความต้องการ", 0.15, 90.0, 95.0, "=D7*C7", "ตัดฟิลด์ Unused ออกจากรายงานเพื่อลด Overhead ของฐานข้อมูล"),
        ("Availability", "ความพร้อมใช้งาน", 0.20, 94.0, 85.0, "=D8*C8", "เปิดบริการผ่าน REST API / Data Lakehouse สำหรับทีม BI และ AI")
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
    for c in range(1, 8):
        apply_thin_border(ws_dq.cell(row=9, column=c))

    # --------------------------------------------------------------------------
    # Sheet 5: DQA Operational Audit Checklist (24 items)
    # --------------------------------------------------------------------------
    ws_chk = wb.create_sheet(title="DQA Operational Audit Checklist")
    ws_chk.views.sheetView[0].showGridLines = True

    chk_headers = [
        "Check ID", "Target Dimension", "Operational Audit Item (หัวข้อการตรวจประเมิน)",
        "Verification Methodology", "Standard Pass Criteria", "Current Status", "Corrective Action Required"
    ]
    for col_idx, h in enumerate(chk_headers, 1):
        cell = ws_chk.cell(row=3, column=col_idx)
        apply_header_style(cell, h, fill_color="D35400")

    audit_checklist = [
        # Accuracy & Completeness (1-5)
        ("AC-01", "Completeness", "ตรวจสอบค่าว่าง (Null / Blank Value) ใน Primary Key เช่น HN, Bill ID", "SQL IS NULL Query", "Null Rate = 0.00%", "PASS", "ระบบ HIS บังคับ Mandatory Input หน้าจอ"),
        ("AC-02", "Completeness", "ตรวจสอบความครบถ้วนของข้อมูลประวัติแพ้ยา (Drug Allergy)", "Cross-table Inner Join", "Missing < 0.1%", "PASS", "แพทย์หรือพยาบาลต้องกดยืนยันประวัติก่อนสั่งยา"),
        ("AC-03", "Accuracy", "ตรวจสอบความถูกต้องของเลขประจำตัวประชาชน 13 หลัก (Mod 11 Check)", "Checksum Algorithm Script", "Error Rate = 0.00%", "PASS", "ระบบเชื่อมต่อเครื่องอ่านสมาร์ตการ์ด"),
        ("AC-04", "Accuracy", "ตรวจสอบช่วงค่าทางคลินิกที่เป็นไปได้ (Vital Signs Range Check: BP, Pulse)", "Boundary Condition Check", "Out of Bound < 0.05%", "WARNING", "พยาบาลบางท่านคีย์ค่าผิดหลักสิบ ให้ทำ UI Validation"),
        ("AC-05", "Completeness", "ตรวจสอบว่าบันทึกการวินิจฉัยโรคผู้ป่วยในมีรหัส ICD-10 ครบทุกราย", "Discharge Audit Report", "Coverage = 100%", "FAIL", "รหัส ICD-10 ยังตกหล่น 12% ต้องตั้ง Audit Alert"),

        # Consistency (6-10)
        ("CS-01", "Consistency", "ตรวจสอบความสอดคล้องของ Master Data ยาและเวชภัณฑ์กับ TMT สากล", "Master Mapping Reconciliation", "Mapping Rate >= 95%", "PASS", "ทีมเภสัชกรแมปโค้ดเสร็จสิ้นแล้ว"),
        ("CS-02", "Consistency", "ตรวจสอบคำนำหน้าชื่อ เพศ และอายุ ไม่ขัดแย้งกันในระบบเวชระเบียน", "Logical Consistency Script", "Mismatch = 0.00%", "PASS", "ทำ Business Rule ตรวจสอบก่อนบันทึก"),
        ("CS-03", "Consistency", "ตรวจสอบรูปแบบวันที่ (Date Format) ให้ตรงกันทั่วทั้งองค์กร (ISO 8601)", "Schema Standardization Check", "Format = YYYY-MM-DD", "PASS", "Data Pipeline ทำ Formatting ตอน Ingestion"),
        ("CS-04", "Consistency", "ตรวจสอบการสะกดชื่อ-นามสกุลผู้ป่วยภาษาอังกฤษให้ตรงกับหนังสือเดินทาง", "Passport OCR Comparison", "Accuracy >= 98%", "WARNING", "แผนกทะเบียนยังใช้พิมพ์มือบางส่วน ให้ใช้เครื่องสแกน"),
        ("CS-05", "Consistency", "ตรวจสอบความสอดคล้องของยอดรายได้ระหว่างระบบ HIS และระบบบัญชี ERP", "Daily Financial Reconciliation", "Variance = 0.00 THB", "PASS", "ทำ Automated Reconciliation สิ้นวัน"),

        # Timeliness (11-14)
        ("TM-01", "Timeliness", "ตรวจสอบระยะเวลาการส่งข้อมูลผลตรวจทางห้องปฏิบัติการ (Lab Turnaround Time)", "Timestamp Delta Analysis", "< 60 นาทีสำหรับ Routine", "PASS", "ระบบ LIS ส่งข้อมูลผ่าน HL7 ทันที"),
        ("TM-02", "Timeliness", "ตรวจสอบความถี่ในการปรับปรุงบัญชีข้อมูล (Data Catalog Metadata)", "Last Updated Timestamp", "ปรับปรุงทุกไตรมาส", "PASS", "Data Steward รับผิดชอบอัปเดตตามรอบ"),
        ("TM-03", "Timeliness", "ตรวจสอบ Latency ของระบบ Data Pipeline จาก HIS เข้าสู่ Lakehouse", "Pipeline Latency Monitor", "Latency < 24 Hours", "PASS", "รัน Daily Batch ทุก 01:00 น."),
        ("TM-04", "Timeliness", "ตรวจสอบการปิดยอดสรุปเคลมประกันสุขภาพและการส่งเบิกจ่าย (Billing Lag)", "Discharge to Bill Delta", "< 7 วันทำการ", "WARNING", "ปัจจุบันเฉลี่ย 14 วัน ต้องลดขั้นตอนแพทย์เซ็น"),

        # Relevancy (15-18)
        ("RL-01", "Relevancy", "ตรวจสอบตารางและคอลัมน์ใน Data Lakehouse ที่ไม่มีผู้ใช้งานเกิน 90 วัน", "Audit Log Query Scan", "Unused Tables < 10%", "PASS", "ทำ Cleanup Script ย้ายเข้า Cold Archive"),
        ("RL-02", "Relevancy", "ตรวจสอบรายงานและแดชบอร์ด BI ที่ไม่มีผู้เปิดดูเกิน 6 เดือน", "Power BI / Tableau Usage Stats", "Active Reports >= 85%", "WARNING", "มีรายงานขยะค้างอยู่ 24 รายการ ต้องดำเนินการลบ"),
        ("RL-03", "Relevancy", "ตรวจสอบชุดข้อมูลเทรนโมเดล AI ว่าตอบโจทย์ทางคลินิกและธุรกิจจริง", "Clinical Advisory Review", "Sign-off 100%", "PASS", "ผ่านการอนุมัติจากคณะกรรมการวิชาการ"),
        ("RL-04", "Relevancy", "ตรวจสอบการจัดทำ Data Dictionary ภาษาไทยกำกับเพื่อลดความสับสน", "Glossary Linkage Audit", "Coverage >= 90%", "PASS", "บรรจุใน Data Catalog เรียบร้อยแล้ว"),

        # Availability & Security (19-24)
        ("AV-01", "Availability", "ตรวจสอบความพร้อมใช้งานของระบบฐานข้อมูลหลัก (Database Uptime SLA)", "Prometheus / Zabbix Monitoring", "Uptime >= 99.90%", "PASS", "จัดทำ High Availability Cluster"),
        ("AV-02", "Security", "ตรวจสอบการเข้ารหัสข้อมูลที่มีชั้นความลับ (Sensitive Data Encryption at Rest)", "Storage Encryption Audit", "AES-256 Enabled 100%", "PASS", "เปิดใช้งาน TDE ในทุก Database"),
        ("AV-03", "Security", "ตรวจสอบการทำ Data Masking บนชุดข้อมูลที่ทีม Data Science นำไปใช้งาน", "PII Scanning Script", "PII Leakage = 0", "PASS", "ผ่าน Anonymization Pipeline 100%"),
        ("AV-04", "Availability", "ตรวจสอบความเร็วในการกู้คืนข้อมูล (Disaster Recovery RTO < 4 ชม.)", "Annual DR Drill Result", "Actual Recovery 2.5 ชม.", "PASS", "ผ่านการซ้อมแผนกู้คืนประจำปี"),
        ("AV-05", "Security", "ตรวจสอบบันทึก Log การเข้าถึงข้อมูลเวชระเบียนของผู้ป่วย (Access Log Audit)", "Log Retention >= 90 Days", "Audit Log Complete", "PASS", "จัดเก็บใน Centralized Log Server"),
        ("AV-06", "Security", "ตรวจสอบความถูกต้องของสิทธิ์ Role-Based Access Control (RBAC) ประจำปี", "Access Rights Certification", "Revocation completed", "PASS", "ตัดสิทธิ์พนักงานที่ลาออกภายใน 24 ชม.")
    ]

    for idx, item in enumerate(audit_checklist, start=4):
        for c_idx, val in enumerate(item, start=1):
            cell = ws_chk.cell(row=idx, column=c_idx, value=val)
            if c_idx == 1:
                cell.alignment = Alignment(horizontal="center")
            elif c_idx == 6:
                cell.alignment = Alignment(horizontal="center")
                if val == "PASS":
                    cell.fill = PatternFill(start_color="D4EFDF", end_color="D4EFDF", fill_type="solid")
                    cell.font = Font(name="Aptos", bold=True, color="145A32")
                elif val == "WARNING":
                    cell.fill = PatternFill(start_color="FCF3CF", end_color="FCF3CF", fill_type="solid")
                    cell.font = Font(name="Aptos", bold=True, color="7D6608")
                elif val == "FAIL":
                    cell.fill = PatternFill(start_color="FADBD8", end_color="FADBD8", fill_type="solid")
                    cell.font = Font(name="Aptos", bold=True, color="78281F")
            apply_thin_border(cell)

    # --------------------------------------------------------------------------
    # Sheet 6: Data Governance Controls (DGC - 15 items)
    # --------------------------------------------------------------------------
    ws_ctrl = wb.create_sheet(title="Data Governance Controls")
    ws_ctrl.views.sheetView[0].showGridLines = True

    ctrl_headers = [
        "Control ID", "Governance Domain", "Control Objective (วัตถุประสงค์การควบคุม)",
        "Mandatory Standard / Regulation", "Responsible Role", "Audit Frequency", "Enforcement Tool"
    ]
    for col_idx, h in enumerate(ctrl_headers, 1):
        cell = ws_ctrl.cell(row=3, column=col_idx)
        apply_header_style(cell, h, fill_color="16A085")

    controls_data = [
        ("DGC-01", "Classification", "ชุดข้อมูลทุกชุดในองค์กรต้องได้รับการจัดระดับชั้นความลับ 5 ระดับ", "DGA / PDPA", "Data Owner", "Annually", "Data Catalog Tagging"),
        ("DGC-02", "Access Control", "การเข้าถึงข้อมูลลับและข้อมูลอ่อนไหวต้องใช้การยืนยันตัวตนแบบ MFA", "NIST CSF / ISO 27001", "Data Custodian (IT)", "Continuous", "Azure AD / Keycloak"),
        ("DGC-03", "Consent Management", "การประมวลผลข้อมูลส่วนบุคคลต้องมีบันทึกความยินยอมและสิทธิ์การถอน", "PDPA มาตรา 19, 26", "DPO / Legal", "Monthly", "OneTrust / In-house CMP"),
        ("DGC-04", "Data Retention", "ข้อมูลเวชระเบียนต้องเก็บรักษาไม่น้อยกว่า 5 ปี และทำลายเมื่อครบกำหนด", "พ.ร.บ. สถานพยาบาล 2541", "Medical Record Head", "Bi-annually", "Automated Purge Script"),
        ("DGC-05", "Third-Party DPA", "การส่งข้อมูลให้ Vendor ภายนอกต้องลงนามสัญญา DPA ทุกครั้ง", "PDPA มาตรา 40", "Legal / Procurement", "Every Contract", "Standard Legal DPA"),
        ("DGC-06", "Encryption", "ข้อมูลส่วนบุคคลที่ส่งผ่านอินเทอร์เน็ตต้องเข้ารหัส TLS 1.3 หรือเทียบเท่า", "DGA Standards", "Network Admin", "Continuous", "WAF / SSL Certificates"),
        ("DGC-07", "De-identification", "ข้อมูลที่นำมาใช้วิจัยหรือเทรน AI ต้องผ่านการตัด 18 PII Identifiers", "HIPAA Safe Harbor / PDPA", "Lead Data Steward", "Every Project", "Python De-id Engine"),
        ("DGC-08", "Breach Response", "เหตุการณ์ข้อมูลรั่วไหลต้องแจ้ง DPO ทันที และแจ้ง สคส. ภายใน 72 ชม.", "PDPA มาตรา 37(4)", "Incident Response Team", "As Occurred", "Incident Playbook"),
        ("DGC-09", "Change Management", "การแก้ไข Data Schema ของตารางหลักต้องผ่านการอนุมัติจาก Data Steward", "DAMA-DMBOK", "Data Steward", "Every Release", "Git Pull Request / Jira"),
        ("DGC-10", "AI Model Lineage", "โมเดล AI ทุกตัวต้องบันทึกแหล่งที่มาของชุดข้อมูลเทรนและเวอร์ชันโมเดล", "ISO/IEC 42001", "MLOps Engineer", "Every Deployment", "MLflow / Vertex AI Registry"),
        ("DGC-11", "Backup Verification", "ต้องทดสอบ Restore ฐานข้อมูลหลักอย่างน้อยทุก 6 เดือน", "ISO 27001 Annex A.12", "DBA", "Bi-annually", "Automated Restore Job"),
        ("DGC-12", "Data Literacy", "พนักงานทุกคนต้องผ่านการฝึกอบรม Data & AI Governance พื้นฐาน", "Corporate Governance", "HR / Academy", "Annually", "E-Learning Platform"),
        ("DGC-13", "Open Data Audit", "ข้อมูลที่จะเผยแพร่เป็น Open Data ต้องไม่มีข้อมูลอ่อนไหวโดยเด็ดขาด", "DGA Open Data Guideline", "Data Governance Council", "Every Release", "DPO Clearance Review"),
        ("DGC-14", "DPIA Execution", "โครงการที่มีการประมวลผลข้อมูลความเสี่ยงสูงต้องทำ DPIA ก่อนเริ่ม", "PDPA มาตรา 37", "Project Manager / DPO", "Pre-project", "DPIA Template"),
        ("DGC-15", "Council Review", "คณะกรรมการธรรมาภิบาลข้อมูลต้องจัดประชุมติดตามผลการดำเนินงาน", "DGA Governance Model", "Council Secretary", "Quarterly", "Formal Board Minutes")
    ]

    for idx, c_data in enumerate(controls_data, start=4):
        for c_idx, val in enumerate(c_data, start=1):
            cell = ws_ctrl.cell(row=idx, column=c_idx, value=val)
            if c_idx in [1, 6]:
                cell.alignment = Alignment(horizontal="center")
            apply_thin_border(cell)

    auto_fit_columns(ws_cover)
    auto_fit_columns(ws_raci)
    auto_fit_columns(ws_cat)
    auto_fit_columns(ws_dq)
    auto_fit_columns(ws_chk)
    auto_fit_columns(ws_ctrl)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wb.save(output_path)
    return output_path
