# Integration Examples

This page provides practical, real-world examples of rules and how they are translated for different AI agents.

## 1. Project-Wide TypeScript Standards
Ensures all agents follow the same coding style across the entire repository.

**File: `typescript-standards.md`**
```markdown
---
name: ts-standards
description: Global TypeScript coding standards
type: global
always_apply: true
---
- Use functional components for React.
- Prefer `interface` over `type` for public APIs.
- Always define explicit return types for functions.
- Avoid using `any`; use `unknown` if the type is truly dynamic.
```

**Compiled Results:**
- **Cursor**: Added to `.cursor/rules/ts-standards.mdc` with `alwaysApply: true`.
- **Claude**: Appended to `CLAUDE.md`.
- **Windsurf**: Added to `.windsurf/rules/ts-standards.md`.
- **Trae**: Added to `.trae/rules/project_rules.md`.
- **Copilot**: Appended to `.github/copilot-instructions.md`.
- **Gemini & Codex**: Appended to `GEMINI.md` and `AGENTS.md`.

---

## 2. Specialized API Development Skill
Provides Claude with advanced "agentic" capabilities for building and testing APIs.

**File: `api-skill.md`**
```markdown
---
name: api-expert
description: Specialized skill for FastAPI development
type: skill
globs: ["app/api/**/*.py"]
---
### API Development Workflow
1. Define the Pydantic model first.
2. Implement the route handler with dependency injection.
3. Write a test case in `tests/test_api.py` before finalizing the code.
4. Use `HTTPException` with appropriate status codes for error handling.
```

**Compiled Results:**
- **Claude Code**: Written to `.claude/skills/api-expert/SKILL.md`.
- **Trae**: Written to `.trae/skills/api-expert/SKILL.md`.
- **Windsurf**: Written to `.windsurf/rules/api-expert.md`.
- **Cursor**: Written to `.cursor/rules/api-expert.mdc`.
- **Copilot**: Written to `.github/instructions/api-expert.instructions.md`.

---

## 3. Legacy Code Guardrails
Prevents AI agents from making risky changes to sensitive or legacy parts of the codebase.

**File: `legacy-guardrails.md`**
```markdown
---
name: legacy-safety
description: Safety rules for the legacy payment engine
globs: ["src/payments/legacy/**/*.js"]
---
- DO NOT refactor this code without explicit permission.
- Only make bug fixes; do not add new features here.
- Ensure all changes are verified by the original payment tests.
- Maintain existing JSDoc comments.
```

**Compiled Results:**
- **GitHub Copilot**: Written to `.github/instructions/legacy-safety.instructions.md` with `applyTo` set to the legacy path.
- **Cursor**: Written to `.cursor/rules/legacy-safety.mdc` with appropriate globs.
- **Claude**: Appended to `CLAUDE.md` with glob context.
- **Gemini**: Appended to `GEMINI.md` with a scope warning.
- **Codex**: Appended to `AGENTS.md`.

---

## 4. Test-Driven Development (TDD) Workflow
Forces agents to adopt a TDD mindset for new features.

**File: `tdd-workflow.md`**
```markdown
---
name: tdd-enforcement
description: Enforce TDD for new features
globs: ["src/features/**/*.ts"]
---
- Before writing any implementation code, write a failing test in the corresponding `__tests__` directory.
- Implementation code must only be written to pass the failing test.
- Refactor only after the test passes.
```

**Compiled Results:**
- **Windsurf**: Written to `.windsurf/rules/tdd-enforcement.md`.
- **Copilot**: Written to a specialized instruction file.
- **Claude**: Appended to `CLAUDE.md`.
