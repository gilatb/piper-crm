from copy import deepcopy
from datetime import date
from typing import Any

from sqlalchemy.orm import Session

from ..models.customers import CustomerCreate
from ..models.leads import LeadCreate
from .models import Customer, Lead


def get_customer(db: Session, customer_id: int):
	return db.query(Customer).filter(Customer.id == customer_id).first()


def get_all_customers(db: Session, skip: int = 0, limit: int = 100):
	return db.query(Customer).offset(skip).limit(limit).all()


def create_customer(db: Session, customer: CustomerCreate):
	db_customer = Customer(**customer.model_dump())
	db.add(db_customer)
	db.commit()
	db.refresh(db_customer)
	return db_customer


def create_customer_from_lead(db: Session, lead_id: int, lead: Lead):
	customer_data = {
		'name': lead.name,
		'contact_email': lead.contact_email,
		'signed_date': date.today(),
		'account_manager_id': lead.assigned_to,
		'lead_id': lead_id,
	}
	db_customer = Customer(**customer_data)
	db.add(db_customer)
	db.commit()
	db.refresh(db_customer)
	return db_customer


def update_customer(db: Session, customer_id: int, customer: CustomerCreate):
	db.query(Customer).filter(Customer.id == customer_id).update(customer.model_dump())
	db.commit()
	return get_customer(db, customer_id)


def delete_customer(db: Session, customer_id: int):
	db.query(Customer).filter(Customer.id == customer_id).delete()
	db.commit()


# Lead CRUD operations

def get_lead(db: Session, lead_id: int):
	return db.query(Lead).filter(Lead.id == lead_id).first()


def get_all_leads(db: Session, skip: int = 0, limit: int = 100):
	return db.query(Lead).offset(skip).limit(limit).all()


def create_lead(db: Session, lead: LeadCreate):
	lead_in_cents = deepcopy(lead)
	lead_in_cents.expected_revenue = int(lead.expected_revenue * 100)

	db_lead = Lead(**lead_in_cents.model_dump())
	db.add(db_lead)
	db.commit()
	db.refresh(db_lead)
	return db_lead


def update_lead(db: Session, lead_id: int, values: dict[str, Any]):
	update_values = {
		getattr(Lead, key): value for key, value in values.items()
	}
	db.query(Lead).filter(Lead.id == lead_id).update(update_values)
	db.commit()
	return get_lead(db, lead_id)


def delete_lead(db: Session, lead_id: int):
	db.query(Lead).filter(Lead.id == lead_id).delete()
	db.commit()
