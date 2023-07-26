from pydantic import BaseModel


class CustomerBase(BaseModel):
	name: str
	contact_email: str
	phone_number: str
	address: str
	signed_date: str
	account_manager_id: int


class CustomerCreate(CustomerBase):
	pass


class Customer(CustomerBase):
	id: int

	class Config:
		from_attributes = True
