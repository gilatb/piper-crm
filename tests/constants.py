from datetime import date

from config import settings

TEST_DATABASE_URL = settings.database_url + "_test"
TODAY = date.today()
EXPECTED_REVENUE = 5000
