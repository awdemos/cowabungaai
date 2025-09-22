
# Maintenance Plan: CowabungaAI System Updates

**Branch**: `001-update-the-feature` | **Date**: 2025-09-21 | **Type**: Maintenance
**Context**: Mature production system requiring ongoing maintenance and improvements

## Executive Summary
CowabungaAI is a complete, production-ready AI platform with **181 Python source files**, 131 frontend files, and comprehensive testing infrastructure. This maintenance plan focuses on system health, bug fixes, completing the LeapfrogAI→CowabungaAI rebranding, and operational improvements.

## Current System State
- **Status**: Production-ready with recent v0.14.0 release
- **Architecture**: Complex monorepo with API, SDK, UI, Evals, and multiple AI backends
- **Deployment**: Kubernetes via UDS (Universal Deployment Service) and Helm charts
- **Testing**: Comprehensive test suite with unit, integration, conformance, and load tests
- **Rebranding Status**: Partially complete - extensive "leapfrogai" references remain

## Maintenance Scope
**IN SCOPE**: System health, bug fixes, dependency updates, documentation cleanup
**OUT OF SCOPE**: New feature development, architectural changes, major refactoring

## Technical Context (Existing System)
**Language/Version**: Python 3.11+ (primary), SvelteKit/TypeScript for UI, Shell scripting for automation
**Primary Dependencies**: FastAPI, OpenAI compatibility, Supabase, gRPC, PostgreSQL, Hugging Face integration
**Storage**: PostgreSQL via Supabase, Kubernetes volumes, local file storage
**Testing**: pytest for unit/integration tests, conformance testing, GitHub Actions CI/CD
**Target Platform**: Linux/macOS development, Kubernetes production deployment
**Project Type**: Complex monorepo with 8 packages + 4 core components
**Performance**: Multi-backend AI model serving (vLLM, llama-cpp, whisper, text-embeddings)
**Constraints**: Air-gapped deployment, government compliance, OpenAI API compatibility
**Scale**: Production deployments with comprehensive monitoring and observability

## Maintenance Priorities

### Priority 1: Complete Rebranding (Critical)
- **Remove 12,712+ "leapfrogai" references** across Python, TypeScript, YAML, and configuration files
- **Update 458+ "defenseunicorns" references** to CowabungaAI branding
- **Fix API endpoints** from `/leapfrogai/v1/*` to `/cowabungaai/v1/*`
- **Update import statements** and module names throughout codebase
- **Rebrand package names** and distribution configurations

### Priority 2: System Health (High)
- **Fix 12 TODO/FIXME/BUG issues** identified in Python files
- **Update 8 pyproject.toml files** with current dependency versions
- **Address OpenAPI compliance issues** (GitHub issues #1107, #1109, #1110)
- **Ensure all CI/CD workflows** are passing and up-to-date
- **Security patches** for any vulnerable dependencies

### Priority 3: Documentation & Configuration (Medium)
- **Update all README files** with CowabungaAI branding
- **Fix broken links** and outdated deployment instructions
- **Update API documentation** to reflect new endpoint paths
- **Standardize configuration** across 8 packages
- **Update Helm charts** and UDS bundles with new branding

### Priority 4: Code Quality & Testing (Low)
- **Address linting issues** in Python and TypeScript files
- **Improve test coverage** in weak areas identified
- **Refactor code duplication** identified in grpc_client.py
- **Performance optimization** for file processing in niah_runner.py
- **Update evaluation metrics** framework with enhanced capabilities

## Identified Issues (Actual Assessment)
- **12,712 "leapfrogai" references** requiring rebranding across all file types
- **458 "defenseunicorns" references** needing updates to CowabungaAI
- **16 TODO/FIXME/BUG comments** in 12 Python files requiring attention
- **8 pyproject.toml files** with potential dependency version conflicts
- **OpenAPI compliance issues** blocking GitHub issues #1107, #1109, #1110
- **API endpoint paths** still using `/leapfrogai/v1/` instead of `/cowabungaai/v1/`

## Current System Architecture (Existing)

### Source Code Structure (Actual Monorepo)
```
cowabungaai/
├── src/                          # Core source code (1.9M total)
│   ├── leapfrogai_api/          # FastAPI backend (448K) - REBRAND NEEDED
│   ├── leapfrogai_evals/        # Evaluation framework (116K) - REBRAND NEEDED
│   ├── leapfrogai_sdk/          # gRPC SDK and protobufs (176K) - REBRAND NEEDED
│   └── leapfrogai_ui/           # SvelteKit frontend (1.9M) - REBRAND NEEDED
├── packages/                    # Deployable packages (8 total)
│   ├── api/                     # API package with UDS bundle
│   ├── llama-cpp-python/        # CPU LLM backend with pyproject.toml
│   ├── vllm/                    # GPU LLM backend with pyproject.toml
│   ├── text-embeddings/         # Embedding service with pyproject.toml
│   ├── whisper/                 # Speech-to-text service with pyproject.toml
│   ├── repeater/                # Testing backend with pyproject.toml
│   └── supabase/                # Database service
├── bundles/                     # UDS deployment bundles
│   ├── dev/                     # Development configurations
│   └── latest/                  # Production configurations
├── tests/                       # Comprehensive test suite
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   ├── conformance/             # OpenAI conformance tests
│   ├── load/                    # Performance tests
│   └── pytest/                  # API pytest tests
├── adr/                         # Architecture Decision Records
├── docs/                        # Documentation
├── website/                     # Docusaurus documentation site
├── .github/                     # GitHub Actions workflows (240 YAML files)
└── pyproject.toml               # Root configuration file
```

### Package Dependencies (8 Total + Root)
- **Core Services**: API, SDK, UI, Evals (all need rebranding)
- **AI Backends**: vLLM (GPU), llama-cpp-python (CPU), text-embeddings, whisper, repeater
- **Infrastructure**: Supabase (database), UDS bundles (deployment)
- **Configuration**: 8 pyproject.toml files + root pyproject.toml

### Key Technologies (Actual)
- **Backend**: Python 3.11+, FastAPI, OpenAI API compatibility
- **Frontend**: SvelteKit, TypeScript, comprehensive component library
- **AI Models**: Multiple backends with OpenAI-compatible API endpoints
- **Database**: Supabase (PostgreSQL) with proper schemas
- **Deployment**: Kubernetes, Helm charts, UDS, Docker containers
- **Testing**: pytest with 4 test types, comprehensive coverage
- **Monitoring**: GitHub Actions, logging, observability tools

## Maintenance Research Approach

### Phase 0: System Analysis
1. **Audit current system state**:
   - Catalog all 12,712 "leapfrogai" references across Python, TypeScript, YAML files
   - Analyze dependency versions in 8 pyproject.toml files + root configuration
   - Assess 16 TODO/FIXME/BUG comments in 12 Python files
   - Review GitHub Actions workflow statuses and OpenAPI compliance issues

2. **Prioritize maintenance tasks**:
   - Critical: Complete LeapfrogAI→CowabungaAI rebranding (12,712 references)
   - High: Fix OpenAPI compliance issues, address 16 TODO/FIXME/BUG items
   - Medium: Update 8 dependency files, ensure CI/CD workflows pass
   - Low: Performance optimizations, enhanced monitoring capabilities

3. **Research best practices**:
   - Safe mass refactoring strategies for large Python/TypeScript codebases
   - OpenAI API compatibility requirements and endpoint migration
   - Multi-package dependency management in monorepos
   - Government compliance requirements for AI systems with rebranding

**Output**: research.md with rebranding strategy, issue prioritization, and safe maintenance protocols

## Phase 1: Maintenance Strategy
*Prerequisites: research.md complete*

1. **Assess rebranding impact** → `data-model.md`:
   - Map 12,712 "leapfrogai" references by file type and component
   - Identify import statements, API endpoints, and package names requiring changes
   - Document dependency relationships affected by rebranding
   - Assess risk and create safe rebranding procedures

2. **Create rebranding procedures**:
   - Define safe refactoring procedures for each component type
   - Establish automated find/replace strategies with validation
   - Document testing requirements for rebranding changes
   - Create rollback procedures for each component category

3. **Generate rebranding checklists**:
   - File-type specific rebranding procedures (Python, TypeScript, YAML, JSON)
   - API endpoint migration validation
   - Import statement and module name updates
   - Package name and distribution rebranding steps

4. **Update agent file incrementally** (O(1) operation):
   - Run `.specify/scripts/bash/update-agent-context.sh claude`
     **IMPORTANT**: Execute it exactly as specified above. Do not add or remove any arguments.
   - Update to reflect actual Python-based system with rebranding focus
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

**Output**: data-model.md (rebranding impact analysis), rebranding procedures, validation checklists, agent-specific file

## Phase 2: Maintenance Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `.specify/templates/tasks-template.md` as base
- Generate tasks from rebranding priorities and system analysis
- Each file type → rebranding task category [P]
- Each component → specific rebranding tasks [P]
- Each TODO/FIXME/BUG → remediation task
- Each dependency file → update task [P]

**Ordering Strategy**:
- Safety order: Configuration files → Python → TypeScript → Documentation
- Component order: Infrastructure → Core → Backends → UI → Tests
- Mark [P] for parallel execution (independent components/file types)
- Prioritize OpenAPI compliance fixes and critical rebranding

**Estimated Output**: 60-80 numbered, ordered rebranding and maintenance tasks in tasks.md

**Task Categories**:
1. **Core Rebranding**: Module names, import statements, package names [P]
2. **API Migration**: Endpoint paths, OpenAPI specs, client compatibility
3. **Configuration Updates**: YAML, TOML, JSON files across all components [P]
4. **Documentation Rebranding**: READMEs, comments, deployment guides [P]
5. **Bug Fixes**: Address 16 TODO/FIXME/BUG items in Python files
6. **Dependency Updates**: 8 pyproject.toml files with version updates

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Maintenance Execution Phases

**Phase 3**: Task execution (/tasks command creates maintenance tasks.md)
**Phase 4**: Implementation (execute maintenance tasks following safety principles)
**Phase 5**: Validation (comprehensive testing of maintenance changes)

## Maintenance Progress Tracking

### Phase 0: System Analysis ⏳
- [ ] Complete "leapfrogai" reference audit (12,712 items)
- [ ] Catalog all TODO/FIXME/BUG comments (16 items in 12 files)
- [ ] Analyze 8 pyproject.toml dependency files
- [ ] Review OpenAPI compliance issues (#1107, #1109, #1110)
- [ ] Assess GitHub Actions workflow health

### Phase 1: Rebranding Strategy ⏳
- [ ] Rebranding impact analysis by file type and component
- [ ] Safe refactoring procedures for Python/TypeScript/YAML
- [ ] API endpoint migration planning
- [ ] Rollback procedures development
- [ ] Testing strategy for rebranding validation

### Phase 2: Task Planning ⏳
- [ ] Organize rebranding tasks by file type and component
- [ ] Create safe parallel execution groups
- [ ] Define component-specific rollback procedures
- [ ] Establish validation testing requirements

## Rebranding Success Criteria

### Core Rebranding Complete
- [ ] Zero "leapfrogai" references remaining in any files
- [ ] All module names updated to cowabungaai_*
- [ ] API endpoints migrated to `/cowabungaai/v1/`
- [ ] Import statements and package names updated
- [ ] Configuration files reflect new branding

### System Health Restored
- [ ] All 16 TODO/FIXME/BUG comments addressed
- [ ] OpenAPI compliance issues resolved (#1107, #1109, #1110)
- [ ] All 8 dependency files updated with current versions
- [ ] No CVEs in updated dependencies
- [ ] All CI/CD workflows passing

### Documentation Quality
- [ ] All README files updated with CowabungaAI branding
- [ ] API documentation reflects new endpoint structure
- [ ] Deployment guides updated and functional
- [ ] Code comments rebranded consistently

### Code Quality Maintained
- [ ] No linting or formatting issues introduced
- [ ] Test coverage maintained during rebranding
- [ ] All automated tests passing after changes
- [ ] Performance benchmarks maintained
- [ ] Rollback procedures tested and documented

**Next Phase**: Execute /tasks command to generate comprehensive rebranding and maintenance task list

## Rebranding Risk Assessment

| Change Category | Risk Level | Rollback Strategy | Testing Requirements |
|-----------------|------------|-------------------|---------------------|
| Core Module Names | High | Git revert | Full test suite + API validation |
| API Endpoints | High | Route config revert | Conformance + integration tests |
| Import Statements | Medium | Find/replace revert | Unit tests + import validation |
| Configuration Files | Low | Version control revert | Configuration validation |
| Documentation | Low | Version control revert | Link and content validation |
| Package Names | High | Distribution rollback | Package installation tests |

**Safety First**: All rebranding changes must include automated validation, comprehensive testing, and documented rollback procedures. Prioritize changes that can be safely rolled back without breaking production deployments.

---
*Maintenance-focused approach for existing production system*
