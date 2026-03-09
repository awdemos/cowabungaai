# CowabungaAI API Development Makefile
# Usage: make [target]

# Configuration
API_PORT ?= 8080
API_BASE_URL ?= https://cowabungaai-api.uds.dev
SUPABASE_BASE_URL ?= https://supabase-kong.uds.dev
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

# Get Supabase configuration from cluster
get-supabase-config: check-tools
	@echo "Fetching Supabase configuration from namespace: ${NAMESPACE}"
	$(eval SUPABASE_ANON_KEY := $(shell uds zarf tools kubectl get secret -n ${NAMESPACE} supabase-bootstrap-jwt -o json | uds zarf tools yq '.data.anon-key' | base64 -d))

# Create environment file
.env: get-supabase-config
	@echo "SUPABASE_URL=${SUPABASE_BASE_URL}" > .env
	@echo "SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}" >> .env
	@echo "Environment file created successfully"

# Install dependencies
install: .env
	@echo "Installing Python dependencies"
	python -m pip install ../../src/leapfrogai_sdk
	python -m pip install -e ".[dev]"

# Development server
dev: .env
	@echo "Starting development server on port ${API_PORT}"
	python -m uvicorn main:app --port ${API_PORT} --reload --log-level info --env-file .env

# Helper function for API key creation
define create_api_key
	curl -s -X POST '${SUPABASE_BASE_URL}/auth/v1/$(1)' \
		-H "apikey: ${SUPABASE_ANON_KEY}" \
		-H "Content-Type: application/json" \
		-H "Authorization: Bearer ${SUPABASE_ANON_KEY}" \
		-d '{ "email": "${TEST_EMAIL}", "password": "${TEST_PASSWORD}"$(2)}' | \
		uds zarf tools yq '.access_token' | \
		xargs -I {} curl -s --insecure -X POST '${API_BASE_URL}/cowabungaai/v1/auth/api-keys' \
		-H "apikey: {}" \
		-H "Content-Type: application/json" \
		-H "Authorization: Bearer {}" \
		-d '{ "name": "api-key", "expires_at": "${EXPIRATION_TIME}" }' | \
		uds zarf tools yq '.api_key'
endef

# Create new user and API key
api-key: get-supabase-config
	@echo "Creating new user and API key"
	@$(call create_api_key,signup?grant_type=password,' "confirmPassword": "${TEST_PASSWORD}"')

# Create API key for existing user
new-api-key: get-supabase-config
	@echo "Creating API key for existing user"
	@$(call create_api_key,token?grant_type=password,)

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
	@echo "  api-key      - Create new user and API key"
	@echo "  new-api-key  - Create API key for existing user"
	@echo "  clean        - Remove generated files"
	@echo "  help         - Show this help message"
	@echo ""
	@echo "Environment variables:"
	@echo "  API_PORT         - API server port (default: 8080)"
	@echo "  API_BASE_URL     - API base URL"
	@echo "  SUPABASE_BASE_URL - Supabase base URL"
	@echo "  NAMESPACE        - Kubernetes namespace (default: cowabungaai)"
	@echo "  TEST_EMAIL       - Test user email"
	@echo "  TEST_PASSWORD    - Test user password"
	@echo "  EXPIRATION_DAYS  - API key expiration in days (default: 30)"

.PHONY: check-tools get-supabase-config install dev api-key new-api-key clean help
