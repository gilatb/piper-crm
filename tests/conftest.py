from typing import Generator
from unittest.mock import patch

import pytest
from _pytest.monkeypatch import MonkeyPatch
from fastapi import FastAPI
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import (create_database, database_exists,  # type: ignore
                              drop_database)
from starlette.testclient import TestClient

from app.db.crud import create_customer, create_lead
from app.db.database import Base
from app.db.models import Customer, Lead
from app.models.customers import CustomerCreate
from app.models.leads import LeadCreate, LeadStatus
from app.routes import customers, leads
from config import settings
from tests.constants import TEST_DATABASE_URL, TODAY


@pytest.fixture(autouse=True, scope="session")
def _patch_settings():
    previous_database_url = settings.database_url
    settings.database_url = TEST_DATABASE_URL

    yield

    settings.database_url = previous_database_url


@pytest.fixture(scope="session")
def db_engine(_patch_settings) -> Generator[Engine, None, None]:
    if not database_exists(settings.database_url):
        create_database(settings.database_url)

    engine = create_engine(settings.database_url)
    Base.metadata.create_all(bind=engine)

    with patch('app.db.database.engine', engine):
        yield engine

    drop_database(settings.database_url)


@pytest.fixture(scope="function")
def db_session(monkeypatch: MonkeyPatch, db_engine: Engine) -> Generator[Session, None, None]:
    session_maker = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session: Session = session_maker()

    monkeypatch.setattr('app.db.database.SessionLocal', session_maker)

    yield session

    session.close()


@pytest.fixture
def app(_patch_settings) -> FastAPI:
    app = FastAPI(
        debug=settings.debug,
        redoc_url='/redoc',
        docs_url='/docs',
    )

    app.include_router(customers.router)
    app.include_router(leads.router)
    return app


@pytest.fixture(scope="function")
def client(app: FastAPI) -> Generator:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def db_lead(db_session: Session) -> Lead:
    lead_data = LeadCreate(
        name="Test Lead",
        contact_email="test@test.com",
        status=LeadStatus.New,
        expected_revenue=5000,
        assigned_to=1,
    )
    return create_lead(db_session, lead_data)


@pytest.fixture(scope="function")
def db_customer(db_session: Session, db_lead: Lead) -> Customer:
    customer_data = CustomerCreate(
        name="Test Customer",
        contact_email="customer@test.com",
        phone_number="1234567890",
        address="123 Main St",
        signed_date=TODAY,
        account_manager_id=1,
        lead_id=int(db_lead.id),
    )
    return create_customer(db_session, customer_data)
