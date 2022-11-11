install:
	poetry install
lint:
	poetry run flake8 flight_parser
test:
	poetry run pytest
test-coverage:
	poetry run pytest --cov=flight_parser --cov-report xml tests/