"""
Automated Test Suite for data-gov-consultant Engine.
Tests LangGraph compilation, Pydantic state transitions, and all 5 industry accelerators.
"""

import sys
import os

# Add root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.state import ClientOrganization
from config.knowledge_base import (
    INDUSTRY_ACCELERATORS,
    DGA_MANDATORY_METADATA_FIELDS,
    DATA_QUALITY_5_DIMENSIONS
)
from pipeline.graph import build_consultant_pipeline


def test_knowledge_base_completeness():
    """Verify all 5 required industries are present with rich use cases and catalogs"""
    required_industries = ["healthcare", "retail", "manufacturing", "public_sector", "bfsi"]
    for ind in required_industries:
        assert ind in INDUSTRY_ACCELERATORS, f"Missing accelerator for {ind}"
        acc = INDUSTRY_ACCELERATORS[ind]
        assert len(acc["high_value_use_cases"]) >= 3, f"Insufficient use cases for {ind}"
        assert len(acc["default_catalog"]) >= 3, f"Insufficient catalog records for {ind}"
    
    assert len(DGA_MANDATORY_METADATA_FIELDS) == 15, "Expected 15 DGA metadata rows (including 9.1 and 9.2)"
    assert len(DATA_QUALITY_5_DIMENSIONS) == 5, "Expected 5 Data Quality dimensions"
    print("✅ test_knowledge_base_completeness passed.")


def test_pipeline_execution():
    """Verify end-to-end execution of a consulting sprint for retail"""
    client = ClientOrganization(
        name="Test Retail Enterprise",
        industry="retail",
        organization_size="Medium",
        annual_revenue_thb=500_000_000.0,
        current_systems=["POS", "ERP"],
        primary_pain_points=["Data silos"],
        target_objectives=["Data Governance"]
    )
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
    app = build_consultant_pipeline()
    final_state = app.invoke(initial_state)

    assert final_state["current_sprint"] == 4
    assert len(final_state["use_cases"]) >= 3
    assert len(final_state["raci_matrix"]) == 10
    assert len(final_state["data_catalog"]) >= 3
    assert len(final_state["cloud_tco"]) == 4
    assert len(final_state["deliverable_paths"]) == 4

    for key, path in final_state["deliverable_paths"].items():
        assert os.path.exists(path), f"Deliverable {key} not found at {path}"

    print("✅ test_pipeline_execution passed.")


if __name__ == "__main__":
    test_knowledge_base_completeness()
    test_pipeline_execution()
    print("\n🎉 ALL TESTS PASSED SUCCESSFULLY!")
