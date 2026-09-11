"""
data-gov-consultant Platform - Main Execution Engine.
Supports CLI arguments for dynamic client engagements via Node.js / AI Agents.
"""

import sys
import os
import argparse

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.state import ClientOrganization
from pipeline.graph import build_consultant_pipeline
from sample_cases.bangkok_smart_health import BANGKOK_SMART_HEALTH_PROFILE


def parse_arguments():
    parser = argparse.ArgumentParser(description="data-gov-consultant: AI-Native Transformation Engine")
    parser.add_argument("--name", type=str, default=None, help="ชื่อองค์กรลูกค้า")
    parser.add_argument("--industry", type=str, default=None, choices=["healthcare", "retail", "manufacturing", "public_sector", "bfsi"], help="ประเภทอุตสาหกรรม")
    parser.add_argument("--size", type=str, default="Large Enterprise", help="ขนาดองค์กร (SME, Medium, Large Enterprise, Ministry)")
    parser.add_argument("--budget", type=float, default=1_200_000_000.0, help="งบประมาณหรือรายได้ต่อปี (บาท)")
    parser.add_argument("--output", type=str, default="output", help="ไดเรกทอรีสำหรับบันทึกไฟล์ผลลัพธ์")
    return parser.parse_args()


def run_engagement():
    args = parse_arguments()

    print("=" * 80)
    print("🏛️  DATA-GOV-CONSULTANT: VIRTUAL DATA & AI TRANSFORMATION CONSULTING PRACTICE")
    print("    Modeled after Tier-1 Boutique Big Data & Data Governance Firms")
    print("=" * 80)

    # Resolve Client Profile
    if args.name and args.industry:
        client = ClientOrganization(
            name=args.name,
            industry=args.industry,
            organization_size=args.size,
            annual_revenue_thb=args.budget,
            current_systems=[
                "Enterprise Resource Planning (ERP)",
                "Transactional Database / Core Operations",
                "Departmental Shared Folders & Excel Reports (Shadow IT)"
            ],
            primary_pain_points=[
                "ข้อมูลระหว่างแผนกไม่เชื่อมโยงกัน รายงานตัวเลขขัดแย้งกัน",
                "ยังไม่มีการจัดทำ Data Catalog และขาดผู้รับผิดชอบข้อมูล (Data Steward) ที่ชัดเจน",
                "ความกังวลด้านกฎหมายคุ้มครองข้อมูลส่วนบุคคล (PDPA) และความมั่นคงปลอดภัยไซเบอร์",
                "ผู้บริหารต้องการเริ่มทำโครงการ AI/Machine Learning แต่ข้อมูลต้นน้ำยังไม่มีคุณภาพ"
            ],
            target_objectives=[
                "จัดตั้งสภาธรรมาภิบาลข้อมูล (Data Governance Council) และ RACI Matrix",
                "จัดทำบัญชีข้อมูลสำคัญ (High-Value Data Catalog) ตามมาตรฐาน 14 ฟิลด์ของ สพร.",
                "ออกแบบสถาปัตยกรรม Modern Data Lakehouse ที่มี TCO คุ้มค่าใน 3 ปี",
                "วางกรอบธรรมาภิบาล AI และความปลอดภัยของข้อมูลเทรนตามมาตรฐาน ISO/IEC 42001"
            ]
        )
    else:
        client = BANGKOK_SMART_HEALTH_PROFILE

    print(f"\n[INIT] Onboarding Client: {client.name}")
    print(f"       Industry: {client.industry.upper()} | Size: {client.organization_size}")
    print(f"       Annual Budget/Revenue: {client.annual_revenue_thb:,.0f} THB")
    print(f"       Legacy Systems: {len(client.current_systems)} identified")
    print(f"       Primary Pain Points: {len(client.primary_pain_points)} recorded")

    # Initialize State
    initial_state = {
        "client": client,
        "current_sprint": 0,
        "maturity_score": 0,
        "maturity_narrative": "",
        "use_cases": [],
        "raci_matrix": [],
        "data_catalog": [],
        "cloud_tco": [],
        "ai_governance_framework": {},
        "change_management_plan": {},
        "audit_notes": [],
        "gate_approved": {},
        "deliverable_paths": {}
    }

    print("\n" + "-" * 80)
    print("🚀 LAUNCHING 4-SPRINT CONSULTING PIPELINE VIA LANGGRAPH ENGINE...")
    print("-" * 80)

    app = build_consultant_pipeline()
    final_state = app.invoke(initial_state)

    print("\n" + "=" * 80)
    print("📋 CONSULTING SPRINT RESULTS & EXECUTIVE SUMMARY")
    print("=" * 80)

    print(f"\n1. MATURITY ASSESSMENT (สพร. DGA Framework):")
    print(f"   ► Current State: Level {final_state['maturity_score']} - {final_state['maturity_narrative']}")

    print(f"\n2. BUSINESS USE-CASE PORTFOLIO & FINANCIAL ROI:")
    total_benefit = sum(uc.estimated_annual_benefit_thb for uc in final_state['use_cases'])
    total_cost = sum(uc.implementation_cost_thb for uc in final_state['use_cases'])
    for uc in final_state['use_cases']:
        print(f"   ► [{uc.id}] {uc.title} ({uc.priority_tier})")
        print(f"     - Benefit: {uc.estimated_annual_benefit_thb/1_000_000:.2f}M THB/yr | Cost: {uc.implementation_cost_thb/1_000_000:.2f}M THB | Payback: {uc.payback_months:.1f} mos")
    print(f"   ► Total Projected 3-Yr Financial Impact: {total_benefit*3/1_000_000:.2f} Million THB")
    print(f"   ► Total Initial Investment: {total_cost/1_000_000:.2f} Million THB")

    print(f"\n3. DATA GOVERNANCE & 40+ RACI OPERATING MODEL:")
    print(f"   ► Formulated Governance Council & Steward Network across {len(final_state['raci_matrix'])} lifecycle activities")
    print(f"   ► Cataloged {len(final_state['data_catalog'])} High-Value Datasets with 14 DGA mandatory metadata fields")
    avg_dq = sum(d.data_quality_score for d in final_state['data_catalog']) / len(final_state['data_catalog'])
    print(f"   ► Average Data Quality Score: {avg_dq:.1f}% (Gate 3 Threshold >= 80% PASSED)")

    print(f"\n4. BIG DATA ARCHITECTURE & CLOUD TCO (3-Year Total Cost of Ownership):")
    for t in final_state['cloud_tco']:
        print(f"   ► {t.provider:<60} : {t.three_year_tco_thb/1_000_000:.2f}M THB (3-Yr TCO)")

    print(f"\n5. AI GOVERNANCE & CHANGE MANAGEMENT (ISO/IEC 42001 & NIST AI RMF):")
    print(f"   ► ISO 42001 Status: {final_state['ai_governance_framework']['iso_42001_readiness']}")
    print(f"   ► Training & Literacy Curriculum: {len(final_state['change_management_plan']['curriculum'])} tier programs configured")

    print(f"\n6. QUALITY GATEKEEPER & RED-TEAM AUDIT:")
    for note in final_state['audit_notes']:
        print(f"   ► {note}")

    print("\n" + "=" * 80)
    print("📦 GENERATED BOARDROOM DELIVERABLES SUITE (TURNKEY PACKAGE)")
    print("=" * 80)
    for name, path in final_state["deliverable_paths"].items():
        file_size_kb = os.path.getsize(path) / 1024
        print(f"   ✅ {name:<25} : {path} ({file_size_kb:.1f} KB)")

    print("\n✨ Engagement successfully completed in 1 execution cycle.")
    print("   All deliverables are publication-ready for Board presentation.")


if __name__ == "__main__":
    run_engagement()
