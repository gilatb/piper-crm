
import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.crud import (create_customer, create_lead, delete_customer,
                         delete_lead, get_all_leads, get_customer, get_lead,
                         update_customer, update_lead)
from app.db.models import Customer, Lead
from app.models.customers import CustomerCreate
from app.models.leads import LeadCreate, LeadStatus
from tests.constants import EXPECTED_REVENUE, TODAY


def test_get_all_leads(db_session: Session):
    lead_data1 = LeadCreate(
        name="Test Lead 1",
        contact_email="test1@test.com",
        status=LeadStatus.New,
        expected_revenue=EXPECTED_REVENUE,
        assigned_to=1,
    )
    lead_data2 = LeadCreate(
        name="Test Lead 2",
        contact_email="test2@test.com",
        status=LeadStatus.New,
        expected_revenue=EXPECTED_REVENUE,
        assigned_to=1,
    )
    create_lead(db_session, lead_data1)
    create_lead(db_session, lead_data2)

    existing_leads = get_all_leads(db_session)
    assert len(existing_leads) == 2
    assert existing_leads[0].name == lead_data1.name
    assert existing_leads[1].name == lead_data2.name


def test_create_lead(db_session: Session):
    lead_data = LeadCreate(
        name="Test Lead",
        contact_email="test@test.com",
        status=LeadStatus.New,
        expected_revenue=EXPECTED_REVENUE,
        assigned_to=1,
    )
    db_lead = create_lead(db_session, lead_data)
    assert db_lead.name == lead_data.name
    assert db_lead.contact_email == lead_data.contact_email


def test_get_lead(db_session: Session, db_lead: Lead):
    retrieved_lead = get_lead(db_session, int(db_lead.id))

    assert retrieved_lead
    assert retrieved_lead.id == int(db_lead.id)
    assert retrieved_lead.name == db_lead.name


def test_update_lead(db_session: Session, db_lead: Lead):
    update_data = {'name': "Updated Lead"}
    updated_lead = update_lead(db_session, int(db_lead.id), update_data)

    assert updated_lead
    assert updated_lead.id == int(db_lead.id)
    assert updated_lead.name == update_data['name']


def test_delete_lead(db_session: Session, db_lead: Lead):
    delete_lead(db_session, int(db_lead.id))
    assert get_lead(db_session, int(db_lead.id)) is None


def test_create_customer(db_session: Session, db_lead: Lead):
    customer_data = CustomerCreate(
        name="Test Customer",
        contact_email="customer@test.com",
        phone_number="1234567890",
        address="123 Main St",
        signed_date=TODAY,
        account_manager_id=1,
        lead_id=int(db_lead.id),
    )
    db_customer = create_customer(db_session, customer_data)
    assert db_customer.name == customer_data.name
    assert db_customer.contact_email == customer_data.contact_email


def test_get_customer(db_session: Session, db_customer: Customer):
    retrieved_customer = get_customer(db_session, int(db_customer.id))

    assert retrieved_customer
    assert retrieved_customer.id == db_customer.id
    assert retrieved_customer.name == db_customer.name


def test_update_customer(db_session: Session, db_customer: Customer):
    update_data = {'name': "Updated Customer"}
    updated_customer = update_customer(db_session, int(db_customer.id), update_data)

    assert updated_customer
    assert updated_customer.id == db_customer.id
    assert updated_customer.name == update_data['name']


def test_delete_customer(db_session: Session, db_customer: Customer):
    delete_customer(db_session, int(db_customer.id))
    assert get_customer(db_session, int(db_customer.id)) is None


def test_one_to_one_relationship(db_session: Session, db_lead: Lead, db_customer: Customer):
    assert db_lead.id == db_customer.lead_id
    customer_data2 = CustomerCreate(
        name="Test Customer 2",
        contact_email="customer2@test.com",
        phone_number="1234567890",
        address="123 Main St",
        signed_date=TODAY,
        account_manager_id=1,
        lead_id=int(db_customer.lead_id),
    )
    with pytest.raises(IntegrityError):
        create_customer(db_session, customer_data2)
