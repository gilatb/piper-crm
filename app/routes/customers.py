from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import crud
from app.db.database import get_db
from app.models.customers import Customer, CustomerCreate

router = APIRouter()


@router.post("/customers/", response_model=Customer)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
	return crud.create_customer(db=db, customer=customer)


@router.get("/customers/{customer_id}", response_model=Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
	db_customer = crud.get_customer(db, customer_id=customer_id)
	if db_customer is None:
		raise HTTPException(status_code=404, detail="Customer not found")
	return db_customer


@router.get("/customers/", response_model=list[Customer])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	customers = crud.get_all_customers(db, skip=skip, limit=limit)
	return customers


@router.put("/customers/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, values: dict[str, Any], db: Session = Depends(get_db)):
	return crud.update_customer(db=db, customer_id=customer_id, values=values)


@router.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
	crud.delete_customer(db=db, customer_id=customer_id)
	return {"detail": "Customer deleted"}
