from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import crud
from app.db.database import get_db
from app.models.leads import Lead, LeadCreate, LeadStatus

router = APIRouter()


@router.post("/leads/", response_model=Lead)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
	return crud.create_lead(db=db, lead=lead)


@router.get("/leads/{lead_id}", response_model=Lead)
def read_lead(lead_id: int, db: Session = Depends(get_db)):
	db_lead = crud.get_lead(db, lead_id=lead_id)
	if db_lead is None:
		raise HTTPException(status_code=404, detail="Lead not found")
	return db_lead


@router.get("/leads/", response_model=list[Lead])
def read_leads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	leads = crud.get_all_leads(db, skip=skip, limit=limit)
	return leads


@router.put("/leads/{lead_id}", response_model=Lead)
def update_lead(lead_id: int, values: dict[str, Any], db: Session = Depends(get_db)):
	updated_lead = crud.update_lead(db=db, lead_id=lead_id, values=values)

	if not (status := values.get('status')):
		return updated_lead

	if updated_lead and status == LeadStatus.Won:
		crud.create_customer_from_lead(db=db, lead_id=lead_id, lead=updated_lead)
	return updated_lead


@router.delete("/leads/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
	crud.delete_lead(db=db, lead_id=lead_id)
	return {"detail": "Lead deleted"}
