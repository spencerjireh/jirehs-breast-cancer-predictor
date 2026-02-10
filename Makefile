.PHONY: install dev dev-backend dev-frontend docker-dev build docker-build docker-run lint format check train clean

BACKEND_VENV = backend/.venv
PYTHON = $(BACKEND_VENV)/bin/python
PIP = $(BACKEND_VENV)/bin/pip

## Setup -----------------------------------------------------------------------

install: ## Create venv, install Python + Node deps, install pre-commit hooks
	python3 -m venv $(BACKEND_VENV)
	$(PIP) install -r backend/requirements.txt
	cd frontend && npm install
	$(PIP) install pre-commit
	$(BACKEND_VENV)/bin/pre-commit install

## Dev servers -----------------------------------------------------------------

dev: ## Run backend + frontend concurrently
	@echo "Starting backend and frontend..."
	$(MAKE) dev-backend & $(MAKE) dev-frontend & wait

dev-backend: ## Start backend dev server
	cd backend && ../$(BACKEND_VENV)/bin/uvicorn app.main:app --reload --port 8000

dev-frontend: ## Start frontend dev server
	cd frontend && npm run dev

docker-dev: ## Run via docker compose (hot-reload)
	docker compose up

## Build -----------------------------------------------------------------------

build: ## Build frontend for production
	cd frontend && npm run build

docker-build: ## Build production Docker image
	docker build -t cytolens .

docker-run: ## Run production Docker container
	docker run -p 8000:8000 cytolens

## Code quality ----------------------------------------------------------------

lint: ## Run ruff check + prettier check
	cd backend && ../$(BACKEND_VENV)/bin/ruff check .
	cd frontend && npx prettier --check "src/**/*.{ts,svelte,css,html}" "*.{ts,js,json}"

format: ## Run ruff fix/format + prettier write
	cd backend && ../$(BACKEND_VENV)/bin/ruff check --fix .
	cd backend && ../$(BACKEND_VENV)/bin/ruff format .
	cd frontend && npx prettier --write "src/**/*.{ts,svelte,css,html}" "*.{ts,js,json}"

check: ## Run svelte-check + tsc
	cd frontend && npm run check

## ML --------------------------------------------------------------------------

train: ## Retrain ML model
	cd backend && ../$(BACKEND_VENV)/bin/python train.py

## Cleanup ---------------------------------------------------------------------

clean: ## Remove build artifacts
	rm -rf frontend/dist
	rm -rf backend/__pycache__ backend/app/__pycache__
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
