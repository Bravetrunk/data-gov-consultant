"""
Pydantic Models and TypedDict State for data-gov-consultant Multi-Agent Consulting Platform.
"""

from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict
from pydantic import BaseModel, Field


class ClientOrganization(BaseModel):
    name: str = Field(..., description="ชื่อองค์กรลูกค้า")
    industry: str = Field(..., description="อุตสาหกรรม (healthcare, retail, bfsi, manufacturing, public_sector)")
    organization_size: str = Field("Large Enterprise", description="ขนาดองค์กร (SME, Medium, Large, Ministry)")
    annual_revenue_thb: float = Field(500_000_000.0, description="รายได้หรือขนาดงบประมาณต่อปี (บาท)")
    current_systems: List[str] = Field(default_factory=list, description="ระบบสารสนเทศที่มีอยู่ในปัจจุบัน")
    primary_pain_points: List[str] = Field(default_factory=list, description="ปัญหาหลักด้านข้อมูลในปัจจุบัน")
    target_objectives: List[str] = Field(default_factory=list, description="เป้าหมายที่ต้องการบรรลุ")


class UseCaseItem(BaseModel):
    id: str
    title: str
    business_unit: str
    business_problem: str
    impact_score: int = Field(..., ge=1, le=5)  # 1-5
    feasibility_score: int = Field(..., ge=1, le=5)  # 1-5
    estimated_annual_benefit_thb: float
    implementation_cost_thb: float
    payback_months: float
    priority_tier: str  # "Quick Win", "Strategic Bet", "High-Value Long-Term", "Low Priority"
    required_datasets: List[str]


class RACIItem(BaseModel):
    task_id: str
    category: str  # "Create", "Store", "Use", "Publish", "Archive", "Destroy", "AI Model", "Compliance"
    activity_name: str
    data_council: str  # A, R, C, I, S
    lead_data_steward: str
    data_owner: str
    data_steward_team: str
    data_custodian_it: str
    data_creator: str
    data_user: str
    dpo_legal: str


class MetadataRecord(BaseModel):
    no: float
    title: str
    owner_org: str
    maintainer: str
    maintainer_email: str
    tag_string: str
    notes: str
    objective: str
    update_frequency: str
    geo_coverage: str
    data_source: str
    data_format: str
    data_category: str
    license_id: str
    data_quality_score: float
    classification_level: str


class CloudTCOComparison(BaseModel):
    provider: str
    storage_monthly_thb: float
    compute_monthly_thb: float
    network_monthly_thb: float
    license_monthly_thb: float
    annual_total_thb: float
    three_year_tco_thb: float
    pros: str
    cons: str


class DataGovConsultantState(TypedDict):
    client: ClientOrganization
    current_sprint: int
    maturity_score: int  # 0 to 5
    maturity_narrative: str
    use_cases: List[UseCaseItem]
    raci_matrix: List[RACIItem]
    data_catalog: List[MetadataRecord]
    cloud_tco: List[CloudTCOComparison]
    ai_governance_framework: Dict[str, Any]
    change_management_plan: Dict[str, Any]
    audit_notes: List[str]
    gate_approved: Dict[str, bool]
    deliverable_paths: Dict[str, str]
