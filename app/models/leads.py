from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator

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
        default=None,
    )
    source: str = Field(
        json_schema_extra={"description": "Where did this lead come from?"},
        default=None,
    )
    created_at: datetime = Field(
        json_schema_extra={"description": "Date and time when the lead was created"},
        default_factory=datetime.utcnow,
    )
    assigned_to: int = Field(
        json_schema_extra={
            "description": "ID of the sales person assigned to this lead",
        },
    )

    @field_validator("created_at")
    @classmethod
    def set_created_at(cls, value: datetime | str) -> datetime:
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value or datetime.utcnow()


class LeadCreate(LeadBase):
    @field_validator("expected_revenue")
    @classmethod
    def convert_to_cents(cls, value: float | int) -> int:
        return int(value * 100)


class Lead(LeadBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Some Corp",
                "contact_email": "email.somecorp.com",
                "status": "New",
                "expected_revenue": 100000.00,
                "source": "Google Ads",
                "created_at": "2021-07-26T15:40:13.881567",
                "assigned_to": 1,
            },
        },
    )
