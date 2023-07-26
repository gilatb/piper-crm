from enum import Enum

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

from app.db.database import Base


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
	name = Column(String)
	contact_email = Column(String)
	sales_stage = Column(String)
	expected_revenue = Column(Float)
	source = Column(String)
	created_at = Column(DateTime)
	assigned_to = Column(Integer)

	# Relationships
	customer = relationship("Customer", back_populates="lead")
