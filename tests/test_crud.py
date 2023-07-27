from sqlalchemy.orm import Session

from app.db.crud import create_lead, get_all_leads
from app.models.leads import LeadCreate, LeadStatus


def test_get_all_leads(db_session: Session):
    lead_data1 = LeadCreate(
        name="Test Lead 1",
        contact_email="test1@test.com",
        status=LeadStatus.New,
        expected_revenue=5000,
        assigned_to=1,
    )
    lead_data2 = LeadCreate(
        name="Test Lead 2",
        contact_email="test2@test.com",
        status=LeadStatus.New,
        expected_revenue=5000,
        assigned_to=1,
    )
    create_lead(db_session, lead_data1)
    create_lead(db_session, lead_data2)

    existing_leads = get_all_leads(db_session)
    assert len(existing_leads) == 2
    assert existing_leads[0].name == lead_data1.name
    assert existing_leads[1].name == lead_data2.name


# test updating lead
# test deleting lead
# test getting lead by id
