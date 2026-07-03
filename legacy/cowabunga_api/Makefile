# CowabungaAI API Development Makefile
# Usage: make [target]

# Configuration
API_PORT ?= 8080
API_BASE_URL ?= https://cowabungaai-api.uds.dev
NAMESPACE ?= cowabungaai

# Security credentials (set in environment or .env)
TEST_EMAIL ?= test@cowabungaai.com
TEST_PASSWORD ?= password
EXPIRATION_DAYS ?= 30

# Computed values
EXPIRATION_TIME := $(shell date -d "+${EXPIRATION_DAYS} days" +%s)

# Check required tools
check-tools:
	@command -v uds >/dev/null 2>&1 || { echo "UDS CLI required but not installed. Aborting." >&2; exit 1; }
	@command -v python >/dev/null 2>&1 || { echo "Python required but not installed. Aborting." >&2; exit 1; }

# Create environment file
.env:
	@echo "TURSO_URL=http://turso:8080" > .env
	@echo "Environment file created successfully"

# Install dependencies
install: .env
	@echo "Installing Python dependencies"
	python -m pip install ../../legacy/cowabunga_sdk
	python -m pip install -e ".[dev]"

# Development server
dev: .env
	@echo "Starting development server on port ${API_PORT}"
	python -m uvicorn main:app --port ${API_PORT} --reload --log-level info --env-file .env

# Clean up generated files
clean:
	@echo "Cleaning up generated files"
	rm -f .env
	@echo "Cleanup complete"

# Show help
help:
	@echo "Available targets:"
	@echo "  install      - Install Python dependencies and setup environment"
	@echo "  dev          - Start development server"
	@echo "  clean        - Remove generated files"
	@echo "  help         - Show this help message"
	@echo ""
	@echo "Environment variables:"
	@echo "  API_PORT         - API server port (default: 8080)"
	@echo "  API_BASE_URL     - API base URL"
	@echo "  NAMESPACE        - Kubernetes namespace (default: cowabungaai)"
	@echo "  TEST_EMAIL       - Test user email"
	@echo "  TEST_PASSWORD    - Test user password"
	@echo "  EXPIRATION_DAYS  - API key expiration in days (default: 30)"

.PHONY: check-tools install dev clean help
