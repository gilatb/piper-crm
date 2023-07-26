from sqlalchemy.orm import Session

from . import models
from ..models.customers import CustomerCreate
from ..models.leads import LeadCreate


# Customer CRUD operations

def get_customer(db: Session, customer_id: int):
	return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


def get_all_customers(db: Session):
	return db.query(models.Customer).all()


def create_customer(db: Session, customer: CustomerCreate):
	db_customer = models.Customer(**customer.dict())
	db.add(db_customer)
	db.commit()
	db.refresh(db_customer)
	return db_customer


def update_customer(db: Session, customer_id: int, customer: CustomerCreate):
	db.query(models.Customer).filter(models.Customer.id == customer_id).update(customer.dict())
	db.commit()
	return get_customer(db, customer_id)


def delete_customer(db: Session, customer_id: int):
	db.query(models.Customer).filter(models.Customer.id == customer_id).delete()
	db.commit()


# Lead CRUD operations

def get_lead(db: Session, lead_id: int):
	return db.query(models.Lead).filter(models.Lead.id == lead_id).first()


def get_all_leads(db: Session):
	return db.query(models.Lead).all()


def create_lead(db: Session, lead: LeadCreate):
	db_lead = models.Lead(**lead.dict())
	db.add(db_lead)
	db.commit()
	db.refresh(db_lead)
	return db_lead


def update_lead(db: Session, lead_id: int, lead: LeadCreate):
	db.query(models.Lead).filter(models.Lead.id == lead_id).update(lead.dict())
	db.commit()
	return get_lead(db, lead_id)


def delete_lead(db: Session, lead_id: int):
	db.query(models.Lead).filter(models.Lead.id == lead_id).delete()
	db.commit()
