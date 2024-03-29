import json
from datetime import date
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.models import Lead
from app.models.customers import CustomerCreate
from app.models.leads import LeadCreate, LeadStatus
from tests.constants import EXPECTED_REVENUE


@pytest.fixture
def created_lead(client: TestClient):
    lead_data = LeadCreate(
        name="Test Lead",
        contact_email="test@test.com",
        status=LeadStatus.New,
        expected_revenue=EXPECTED_REVENUE,
        source="Google",
        assigned_to=1,
    )
    data = json.loads(lead_data.model_dump_json())
    response = client.post("/leads/", json=data)
    return response.json()


def test_create_lead(client: TestClient):
    lead_data = LeadCreate(
        name="Test Lead",
        contact_email="test@test.com",
        status=LeadStatus.New,
        expected_revenue=EXPECTED_REVENUE,
        source="Google",
        assigned_to=1,
    )
    data = json.loads(lead_data.model_dump_json())

    data["expected_revenue"] = data["expected_revenue"] // 100  # converted to cents
    response = client.post("/leads/", json=data)

    assert response.status_code == 200
    created_lead = response.json()
    assert created_lead["name"] == data["name"]
    assert created_lead["contact_email"] == data["contact_email"]
    assert created_lead["status"] == data["status"]
    assert created_lead["expected_revenue"] == EXPECTED_REVENUE * 100


def test_create_customer(client: TestClient, db_lead: Lead):
    customer_data = CustomerCreate(
        name="Test Customer",
        contact_email="some@email.com",
        phone_number="1234567890",
        address="123 Main St",
        signed_date=date(2021, 1, 1),
        account_manager_id=1,
        lead_id=int(db_lead.id),
    )
    data = json.loads(customer_data.model_dump_json())

    response = client.post("/customers/", json=data)

    assert response.status_code == 200
    assert response.json()["name"] == data["name"]
    assert response.json()["contact_email"] == data["contact_email"]


def test_convert_lead_to_customer(
    client: TestClient,
    db_session: Session,
    created_lead: dict[str, Any],
):
    values = {'status': LeadStatus.Won}
    updated_lead_response = client.put(f"/leads/{created_lead['id']}", json=values).json()

    assert updated_lead_response['status'] == LeadStatus.Won

    all_customers = client.get("/customers/").json()
    assert any(customer['lead_id'] == created_lead['id'] for customer in all_customers)
