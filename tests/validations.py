import pytest
from starlette.testclient import TestClient

from app.db.models import Lead
from app.models.customers import CustomerCreate
from tests.constants import TODAY


def test_customer_create_w_invalid_email(client: TestClient, db_lead: Lead):
    with pytest.raises(ValueError, match="Invalid email address"):
        CustomerCreate(
            name="Test Customer 2",
            contact_email="invalid",
            phone_number="1234567890",
            address="123 Main St",
            signed_date=TODAY,
            account_manager_id=1,
            lead_id=int(db_lead.id),
        )
