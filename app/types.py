from typing import Annotated

from pydantic import AfterValidator

from app.utils import is_email_valid

EmailAddress = Annotated[str, AfterValidator(is_email_valid)]
