.PHONY: help lint format test coverage clean install

help:
	@echo "Available commands:"
	@echo "  make install      - Install development dependencies"
	@echo "  make lint         - Run all linters (black, isort, flake8, pylint, mypy)"
	@echo "  make format       - Format code with black and isort"
	@echo "  make test         - Run pytest"
	@echo "  make coverage     - Run pytest with coverage report"
	@echo "  make clean        - Remove generated files and caches"

install:
	pip install -r requirements-dev.txt

lint:
	@echo "Running Black check..."
	black --check .
	@echo "Running isort check..."
	isort --check-only .
	@echo "Running flake8..."
	flake8 .
	@echo "Running pylint..."
	find . -type f -name "*.py" -not -path "./.*" -not -path "./.venv/*" | xargs pylint --exit-zero --disable=fixme
	@echo "Running mypy..."
	mypy .

format:
	@echo "Formatting with black..."
	black .
	@echo "Sorting imports with isort..."
	isort .

test:
	pytest -v

coverage:
	pytest --cov=. --cov-report=html --cov-report=term-missing

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name htmlcov -exec rm -rf {} +
	find . -type d -name .tox -exec rm -rf {} +
	find . -name .coverage -delete
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "*.egg-info" -exec rm -rf {} +
	find . -name dist -exec rm -rf {} +
	find . -name build -exec rm -rf {} +

