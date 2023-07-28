from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator

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
    name: str = Field(json_schema_extra={"description": "Name of the lead"})
    contact_email: EmailAddress = Field(
        json_schema_extra={"description": "Email address for the primary contact"},
    )
    status: LeadStatus = Field(
        json_schema_extra={"description": "Current status of the lead"},
        default=LeadStatus.New,
    )
    expected_revenue: int = Field(
        json_schema_extra={
            "description": "Expected revenue from this lead. "
            "Will be converted into cents when stored in the database.",
        },
        example=100000.00,
        default=None,
    )
    source: str = Field(
        json_schema_extra={"description": "Where did this lead come from?"},
        example="Google Ads",
        default=None,
    )
    created_at: datetime = Field(
        json_schema_extra={"description": "Date and time when the lead was created"},
        example="2021-07-26T15:40:13.881567",
        default=datetime.utcnow().isoformat(),
    )
    assigned_to: int = Field(
        json_schema_extra={
            "description": "ID of the sales person assigned to this lead",
        },
    )


class LeadCreate(LeadBase):
    @field_validator("expected_revenue")
    @classmethod
    def convert_to_cents(cls, value: float | int) -> int:
        return int(value * 100)


class Lead(LeadBase):
    id: int

    class Config:
        from_attributes = True
