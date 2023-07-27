from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.leads import LeadStatus


class Customer(Base):
	__tablename__ = "customers"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String)
	contact_email = Column(String)
	phone_number = Column(String)
	address = Column(String)
	signed_date = Column(DateTime)
	account_manager_id = Column(Integer)  # assuming we store the employee id elsewhere
	lead_id = Column(Integer, ForeignKey("leads.id"))

	# Relationships
	lead = relationship("Lead", back_populates="customer")


class Lead(Base):
	__tablename__ = "leads"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, nullable=False)
	contact_email = Column(String, nullable=False)
	status = Column(Enum(LeadStatus), nullable=False, default=LeadStatus.New)  # type: ignore
	expected_revenue = Column(Integer, nullable=True)
	source = Column(String, nullable=True)
	created_at = Column(DateTime, default=datetime.utcnow())
	assigned_to = Column(Integer, nullable=True)

	# Relationships
	customer = relationship("Customer", back_populates="lead")
