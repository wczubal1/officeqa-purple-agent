.PHONY: help install test run example clean docker-build docker-run lint format

help:
	@echo "OfficeQA Purple Agent - Available Commands"
	@echo "=========================================="
	@echo ""
	@echo "Setup:"
	@echo "  make install       - Install dependencies"
	@echo "  make venv          - Create virtual environment"
	@echo ""
	@echo "Development:"
	@echo "  make run           - Run the agent"
	@echo "  make example       - Run example assessment"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linting checks"
	@echo "  make format        - Format code with black"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run Docker container"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean         - Remove cache and build files"

venv:
	python -m venv venv
	. venv/bin/activate && pip install --upgrade pip

install: venv
	. venv/bin/activate && pip install -r requirements.txt
	. venv/bin/activate && pip install -e ".[dev]"

test:
	. venv/bin/activate && pytest tests/ -v

run:
	. venv/bin/activate && python -m src.agent.main

example:
	. venv/bin/activate && python -m src.agent.main --example

lint:
	. venv/bin/activate && ruff check src/ tests/
	. venv/bin/activate && mypy src/ --ignore-missing-imports

format:
	. venv/bin/activate && black src/ tests/
	. venv/bin/activate && ruff check --fix src/ tests/

docker-build:
	docker build -t officeqa-purple-agent:latest .

docker-run:
	docker run --env-file .env \
		-v $(PWD)/output:/app/output \
		officeqa-purple-agent:latest

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf output/
