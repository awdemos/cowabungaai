# CowabungaAI Development Agents

This document describes the AI coding agents that operate in this repository and provides guidelines for their use.

## Available Agents

### Sisyphus (Main Orchestrator)
**Role**: Orchestrates development tasks, manages other agents, ensures code quality
**Capabilities**:
- Orchestrates multi-file operations
- Delegates to specialized agents (frontend-ui-ux-engineer, document-writer)
- Validates work across multiple files and modules
- Manages todo tracking for complex tasks
- Reviews code changes before finalizing

### Agent Specialization

#### Frontend UI/UX
**Agent**: `frontend-ui-ux-engineer`
**Use for**: Visual changes, styling, layout, animation, responsive design
**Capabilities**:
- Creates and modifies React/Svelte/Vue components
- Applies Tailwind CSS classes and modern design patterns
- Ensures responsive layouts and mobile compatibility
- Implements accessibility standards (WCAG, ARIA)

#### Document Writer
**Agent**: `document-writer`
**Use for**: README files, API documentation, architecture diagrams
**Capabilities**:
- Generates comprehensive project documentation
- Creates architecture diagrams
- Writes clear, structured markdown files
- Ensures consistency with existing docs

#### Oracle (Architecture Advisor)
**Agent**: `oracle`
**Use for**: Complex architectural decisions, multi-system tradeoffs, code quality
**Capabilities**:
- Deep analysis of system design patterns
- Recommends best practices for distributed systems
- Reviews and validates implementation approaches
- Provides guidance on security, performance, and scalability

#### Librarian (Research Agent)
**Agent**: `librarian`
**Use for**: External dependencies, OSS packages, documentation research
**Capabilities**:
- Researches best practices from open-source projects
- Locates implementation examples
- Checks for dependency vulnerabilities
- Retrieves library version information

#### Explore Agent
**Agent**: `explore`
**Use for**: Codebase pattern discovery, file searching, AST analysis
**Capabilities**:
- Searches codebase for specific patterns and implementations
- Uses AST-grep for structural analysis
- Finds imports, exports, and code relationships
- Analyzes file dependencies and module structures

#### Subagent Execution
The system supports subagent execution through `task` and `subagents/utils` modules. These are used by the main orchestrator (Sisyphus) to delegate specialized work.

## Code Style Guidelines

### General Principles
- **Clarity**: Code should be self-documenting and easy to understand
- **Consistency**: Follow existing patterns in codebase
- **Simplicity**: Prefer straightforward solutions over complex ones
- **Type Safety**: Use TypeScript types correctly, avoid `any` type
- **Error Handling**: Always handle errors gracefully, provide meaningful error messages
- **Performance**: Consider performance implications of changes

### TypeScript/JavaScript Guidelines

#### Imports
```typescript
// Preferred - explicit named imports
import { expect, test } from '@playwright/test';
import type { Page } from '@playwright/test';

// Avoid wildcard imports
// import * from 'library-name';  // Not recommended

// Type imports
import type { FileObject } from 'openai/resources/files';
```

#### Naming Conventions

#### Files
- **Components**: PascalCase (e.g., `UserProfile.ts`, `ChatMessage.ts`)
- **Utilities**: camelCase (e.g., `fileHelpers.ts`, `navigationHelpers.ts`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `API_BASE_URL`, `LONG_RESPONSE_PROMPT`)
- **Test Files**: kebab-case (e.g., `api-keys.test.ts`, `header.test.ts`)
- **Test Functions**: camelCase (e.g., `createAPIKey`, `deleteBtn`

#### Functions
```typescript
// Async functions use camelCase
async function createAPIKey(): Promise<void> {
  const { page } = getTestPage();
  // ...
}

// Utility functions use camelCase
function formatDate(date: Date): string {
  // ...
}
```

#### Error Handling

#### Expected Patterns
```typescript
// Try-catch blocks for async operations
try {
  await someAsyncOperation();
} catch (error) {
  logError('Operation failed', error);
  throw new ApplicationError(error.message);
}

// Validate inputs before processing
function validateApiKey(key: string): boolean {
  if (!key || key.trim().length === 0) {
    throw new Error('API key is required');
  }
  return true;
}
```

#### Testing Guidelines

#### E2E Testing
- Test critical user flows (authentication, file operations, chat)
- Test error conditions and edge cases
- Verify UI responsiveness and accessibility
- Test API error handling
- Verify data serialization/deserialization

#### API Testing
- Mock API responses for local development
- Test API error handling
- Verify data serialization/deserialization

#### Documentation Requirements

#### README Files
- Project overview and architecture
- Installation and setup instructions
- Development guidelines and contribution process
- API reference documentation
- Troubleshooting guide

## Build/Lint/Test Commands

The repository uses several tools for building and testing codebase:

### Testing Framework
- **Playwright**: E2E testing framework for UI
- **Expectation/Assert**: Assertion library for test assertions
- **Test Organization**: Tests organized by feature/feature

### Linting
- **Ruff**: Python linter for fast, type-safe linting
- **ESLint**: JavaScript/TypeScript linter
- **Prettier**: Code formatter for consistent formatting

### Running Tests
```bash
# Run all tests
npm test
```

### Docker/Packaging

Images are built and can be run directly:
```bash
# Run UI
docker run -d -p 5173:5173 \
  --name leapfrogai-ui \
  ghcr.io/defenseunicorns/leapfrogai/leapfrogai-ui:4dd6953f
```

## Environment Variables

Required environment variables should be documented in deployment guides.

---

*Last Updated: 2025-01-11*
