import datetime

from pydantic import BaseModel, Field


class CustomerBase(BaseModel):
	name: str = Field(description="Name of the customer")
	contact_email: str = Field(description="Email address for the primary contact")
	phone_number: str | None = Field(description="Format: 123-456-789", default=None)
	address: str | None = Field(
		description="Street address, city, state, zip code",
		example="123 Main St, Anytown, USA 12345",
		default=None,
	)
	signed_date: datetime.date = Field(
		description="Format: YYYY-MM-DD",
		example="2021-01-01",
		default=datetime.date.today().isoformat(),
	)
	account_manager_id: int = Field(
		description="ID of the account manager assigned to this customer",
		example=1,
	)
	lead_id: int | None = Field(
		description="ID of the lead that converted to this customer",
		example=1,
		default=None,
	)


class CustomerCreate(CustomerBase):
	pass


class Customer(CustomerBase):
	id: int

	class Config:
		from_attributes = True
