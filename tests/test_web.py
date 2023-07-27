from datetime import date
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.customers import CustomerCreate
from app.models.leads import LeadCreate, LeadStatus


@pytest.fixture
def created_lead(app: FastAPI):
    client = TestClient(app)
    lead_data = LeadCreate(
        name="Test Lead",
        contact_email="test@test.com",
        status=LeadStatus.New,
        expected_revenue=5000,
        source="Google",
        assigned_to=1,
    ).model_dump()

    response = client.post("/leads/", json=lead_data)
    return response.json()


def test_create_lead(app: FastAPI):
    client = TestClient(app)
    lead_data = LeadCreate(
        name="Test Lead",
        contact_email="test@test.com",
        status=LeadStatus.New,
        expected_revenue=5000,
        source="Google",
        assigned_to=1,
    ).model_dump()

    response = client.post("/leads/", json=lead_data)

    assert response.status_code == 200
    assert response.json()["name"] == lead_data["name"]
    assert response.json()["contact_email"] == lead_data["contact_email"]
    assert response.json()["status"] == lead_data["status"]
    assert response.json()["expected_revenue"] == int(lead_data["expected_revenue"] * 100)


def test_create_customer(app: FastAPI):
    client = TestClient(app)
    customer_data = CustomerCreate(
        name="Test Customer",
        contact_email="some@email.com",
        phone_number="1234567890",
        address="123 Main St",
        signed_date=date(2021, 1, 1),
        account_manager_id=1,
        lead_id=1,
    ).model_dump()
    customer_data["signed_date"] = customer_data["signed_date"].isoformat()
    response = client.post("/customers/", json=customer_data)

    assert response.status_code == 200
    assert response.json()["name"] == customer_data["name"]
    assert response.json()["contact_email"] == customer_data["contact_email"]


def test_convert_lead_to_customer(
    app: FastAPI,
    db_session: Session,
    created_lead: dict[str, Any],
):
    client = TestClient(app)

    values = {'status': LeadStatus.Won}
    updated_lead_response = client.put(f"/leads/{created_lead['id']}", json=values).json()

    assert updated_lead_response['status'] == LeadStatus.Won

    all_customers = client.get("/customers/").json()
    assert any(customer['lead_id'] == created_lead['id'] for customer in all_customers)
