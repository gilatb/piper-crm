import re

from app.constants import EMAIL_REGEX


def is_email_valid(email: str):
	if not re.fullmatch(EMAIL_REGEX, email):
		raise ValueError("Invalid email address")
	return email
