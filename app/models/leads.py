from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from app.types import EmailAddress


class LeadStatus(str, Enum):
    New = "New"
    Contacted = "Contacted"
    Qualified = "Qualified"
    Proposal = "Proposal"
    Negotiation = "Negotiation"
    Won = "Won"
    Lost = "Lost"


class LeadBase(BaseModel):
    name: str = Field(description="Name of the lead")
    contact_email: EmailAddress = Field(description="Email address for the primary contact")
    status: LeadStatus = Field(
        description="Current status of the lead",
        default=LeadStatus.New,
    )
    expected_revenue: float = Field(
        description="Expected revenue from this lead. "
                    "Will be converted into cents when stored in the database.",
        example=100000.00,
        default=None,
    )
    source: str = Field(
        description="Where did this lead come from?",
        example="Google Ads",
        default=None,
    )
    created_at: datetime = Field(
        description="Date and time when the lead was created",
        example="2021-07-26T15:40:13.881567",
        default=datetime.utcnow().isoformat(),
    )
    assigned_to: int = Field(description="ID of the sales person assigned to this lead")


class LeadCreate(LeadBase):
    pass


class Lead(LeadBase):
    id: int

    class Config:
        from_attributes = True
