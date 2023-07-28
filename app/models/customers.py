import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.types import EmailAddress


class CustomerBase(BaseModel):
	name: str = Field(json_schema_extra={'description': 'Name of the customer'})
	contact_email: EmailAddress = Field(
		json_schema_extra={"description": "Email address for the primary contact"},
	)
	account_manager_id: int = Field(
		json_schema_extra={
			"description": "ID of the account manager assigned to this customer",
		},
	)
	phone_number: str | None = Field(
		None,
		json_schema_extra={"description": "Format: 123-456-789"},
	)
	address: str | None = Field(
		None,
		json_schema_extra={"description": "Street address, city, state, zip code"},
	)
	signed_date: datetime.date = Field(
		datetime.date.today().isoformat(),
		json_schema_extra={"description": "Format: YYYY-MM-DD"},
	)
	lead_id: int | None = Field(
		None,
		json_schema_extra={
			"description": "ID of the lead that converted to this customer",
		},
	)


class CustomerCreate(CustomerBase):
	pass


class Customer(CustomerBase):
	id: int

	model_config = ConfigDict(
		from_attributes=True,
		json_schema_extra={
			"example": {
				"name": "Some Corp",
				"contact_email": "email.somecorp.com",
				"address": "123 Main St, Anytown, USA 12345",
				"account_manager_id": 1,
				"lead_id": 1,
				"singed_date": "2021-01-01",
			},
		},
	)
