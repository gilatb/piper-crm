
web:
	python web.py

alembic-create-tables:
	PYTHONPATH=. alembic revision --autogenerate -m "create tables"

migrations:
	PYTHONPATH=. alembic upgrade head

requirements:
	pip install -r requirements.txt --no-cache-dir

alembic-restart:
	PYTHONPATH=. alembic downgrade base && make migrations

start: requirements migrations web

test:
	pytest

coverage-collect:
	coverage run -m pytest

coverage-report:
	coverage html

coverage: coverage-collect coverage-report

pycln:
	pycln .

mypy:
	mypy app tests *.py

flake8:
	flake8 app tests *.py

isort:
	isort app tests *.py

bandit:
	bandit -q -r -x /venv,/tests .

check: pycln isort flake8 mypy test coverage bandit
