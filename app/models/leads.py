from enum import Enum

from pydantic import BaseModel


class LeadStatus(str, Enum):
    New = "New"
    Contacted = "Contacted"
    Qualified = "Qualified"
    Proposal = "Proposal"
    Negotiation = "Negotiation"
    Won = "Won"
    Lost = "Lost"


class LeadBase(BaseModel):
    name: str
    contact_email: str
    status: LeadStatus
    expected_revenue: float
    source: str
    created_at: str
    assigned_to: int


class LeadCreate(LeadBase):
    pass


class Lead(LeadBase):
    id: int

    class Config:
        from_attributes = True
