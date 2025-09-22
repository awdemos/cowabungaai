# Quick Start Guide: Feature Specification System

**Branch**: `001-update-the-feature` | **Date**: 2025-09-21

## Overview

This guide provides a quick start for using the modernized CowabungaAI feature specification system. The system automates specification generation, provides standardized templates, and ensures comprehensive documentation for all feature types.

## Prerequisites

### System Requirements
- **Operating System**: Linux, macOS, or Windows with WSL2
- **Python**: 3.11 or higher
- **Git**: Latest version
- **Storage**: 100MB for templates and configuration

### Development Environment
```bash
# Python environment setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install click pyyaml jinja2 gitpython
```

## Quick Start

### 1. Initialize the System
```bash
# Clone the repository
git clone https://github.com/defenseunicorns/leapfrogai.git
cd leapfrogai

# Initialize specification system
python -m spec_system init
```

### 2. Create a New Feature Specification
```bash
# Basic spec creation
python -m spec_system create --name "user-authentication" --type api

# Interactive spec creation
python -m spec_system create --interactive

# From existing branch
python -m spec_system create --from-branch "feature/user-auth"
```

### 3. Validate Existing Specifications
```bash
# Validate all specs
python -m spec_system validate --all

# Validate specific spec
python -m spec_system validate --spec "specs/001-user-auth/spec.md"

# Generate validation report
python -m spec_system validate --all --report validation-report.json
```

### 4. Generate Templates
```bash
# List available templates
python -m spec_system templates --list

# Create custom template
python -m spec_system templates --create --name "custom-api" --type api

# Update existing template
python -m spec_system templates --update --name "api"
```

## Common Workflows

### Creating an API Feature
```bash
# Create API feature specification
python -m spec_system create \
  --name "user-profile-api" \
  --type api \
  --template "enhanced-api" \
  --openapi "contracts/user-profile-api.yaml"

# The system will generate:
# - specs/002-user-profile-api/spec.md
# - specs/002-user-profile-api/contracts/api.yaml
# - Validation and completeness checks
```

### Creating a UI Feature
```bash
# Create UI feature specification
python -m spec_system create \
  --name "dashboard-redesign" \
  --type ui \
  --template "component-based" \
  --wireframes "design/wireframes/"

# The system will generate:
# - specs/003-dashboard-redesign/spec.md
# - specs/003-dashboard-redesign/contracts/ui-components.yaml
# - Accessibility and testing requirements
```

### Creating Architecture Decision
```bash
# Create ADR specification
python -m spec_system create \
  --name "database-migration" \
  --type architecture \
  --template "adr" \
  --impact "high"

# The system will generate:
# - specs/004-database-migration/spec.md
# - specs/004-database-migration/contracts/decision-criteria.yaml
# - Risk assessment and alternatives analysis
```

## Template Examples

### API Feature Template Structure
```markdown
# API Feature: [Feature Name]

## Overview
[Brief description of the API feature]

## OpenAPI Contract
- **Endpoint**: `GET /api/v1/users`
- **Authentication**: JWT required
- **Rate Limiting**: 100 requests/minute

## User Stories
- **As a** developer, **I want to** user management endpoints **so that** I can integrate user functionality
- **As a** system admin, **I want to** user listing **so that** I can monitor user activity

## Acceptance Criteria
- **Given** a valid JWT token, **When** I request users, **Then** I receive a paginated list
- **Given** an invalid token, **When** I request users, **Then** I receive 401 Unauthorized

## Technical Requirements
- **FR-001**: System MUST support pagination with customizable page sizes
- **FR-002**: System MUST validate JWT tokens using the configured secret
- **NFR-001**: Response time MUST be <200ms for 100 concurrent requests
```

### UI Feature Template Structure
```markdown
# UI Feature: [Feature Name]

## Overview
[Brief description of the UI feature]

## Component Structure
- **Parent Component**: DashboardPage
- **Child Components**: UserProfile, UserTable, SearchBar
- **State Management**: Redux store integration

## User Stories
- **As a** user, **I want to** search users **so that** I can find specific users quickly
- **As a** user, **I want to** export user data **so that** I can analyze it offline

## Acceptance Criteria
- **Given** I am on the dashboard, **When** I type in the search box, **Then** results filter in real-time
- **Given** I select users, **When** I click export, **Then** I receive a CSV file

## Accessibility Requirements
- **WCAG 2.1 AA**: All interactive elements must be keyboard accessible
- **Screen Reader**: Proper ARIA labels and descriptions
- **Color Contrast**: Minimum 4.5:1 contrast ratio
```

## Configuration

### System Configuration
Create `config/spec-system.yaml`:
```yaml
system:
  project_name: "CowabungaAI"
  version: "1.0.0"
  default_language: "en"

automation:
  auto_validate: true
  generate_tests: true
  integration_mode: "pre_commit"

templates:
  directory: "templates/"
  custom_path: "custom-templates/"

validation:
  strict_mode: false
  warning_threshold: 0.8
  error_threshold: 0.6
```

### Template Customization
Create custom templates in `custom-templates/`:
```yaml
# custom-templates/api-enhanced.yaml
name: "Enhanced API"
type: "api"
sections:
  - name: "OpenAPI Contract"
    required: true
    content_type: "yaml"
  - name: "Security Considerations"
    required: true
    content_type: "markdown"
  - name: "Performance Requirements"
    required: true
    content_type: "markdown"
```

## Integration with Development Workflow

### Pre-commit Integration
Add to `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: local
    hooks:
      - id: spec-validation
        name: Validate Feature Specifications
        entry: python -m spec_system validate --all
        language: system
        files: ^specs/.*\.md$
        pass_filenames: false
```

### CI/CD Integration
Add to your CI pipeline:
```yaml
# .github/workflows/spec-validation.yml
name: Specification Validation
on: [pull_request]

jobs:
  validate-specs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Validate specifications
        run: python -m spec_system validate --all --report validation-report.json
      - name: Upload validation report
        uses: actions/upload-artifact@v3
        with:
          name: validation-report
          path: validation-report.json
```

## Troubleshooting

### Common Issues

#### Specification Validation Fails
```bash
# Check validation details
python -m spec_system validate --spec "specs/001-feature/spec.md" --verbose

# Get recommendations
python -m spec_system validate --spec "specs/001-feature/spec.md" --recommendations
```

#### Template Not Found
```bash
# List available templates
python -m spec_system templates --list

# Check template directory
python -m spec_system config --show template_directories
```

#### Git Integration Issues
```bash
# Check git repository status
git status

# Verify git integration
python -m spec_system git --status
```

### Getting Help

```bash
# Get help
python -m spec_system --help

# Get specific command help
python -m spec_system create --help

# Check system status
python -m spec_system status
```

## Next Steps

1. **Explore Templates**: Review existing templates and create custom ones
2. **Integrate Workflow**: Set up pre-commit hooks and CI/CD integration
3. **Team Training**: Conduct training sessions for development team
4. **Backfill Existing**: Generate specifications for existing features
5. **Continuous Improvement**: Monitor usage and refine templates

For detailed documentation, see the full specification documentation or run `python -m spec_system docs`.