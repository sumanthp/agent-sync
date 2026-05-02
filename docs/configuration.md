# Configuration Guide

## Rule Definition
Rules are defined in Markdown files with a YAML frontmatter block.

### Frontmatter Fields
- `name` (required): Unique identifier for the rule.
- `description`: A brief summary of what the rule does.
- `globs`: A list of file patterns the rule applies to (e.g., `["src/**/*.ts"]`).
- `type`: Category of the rule.
    - `rule` (default): Standard behavioral instruction.
    - `skill`: Advanced agentic behavior (compiled to `SKILL.md` for Claude).
    - `global`: Project-wide instruction (compiled to `.cursorrules` for Cursor).
- `always_apply`: Boolean. If true, the rule is always active (handled natively by Cursor).

### Example Rule
```markdown
---
name: strict-typing
description: Enforce strict typing in TypeScript
globs: ["**/*.ts"]
type: rule
---
- Always use explicit return types.
- Avoid the `any` type at all costs.
```

## Local Configuration
The `.agent-sync/config.json` file manages remote repositories:
```json
{
  "remotes": [
    "https://github.com/org/shared-rules.git"
  ]
}
```

## Rule Discovery
`agentsync-vcs` looks for all `.md` files in the current directory (excluding generated files like `CLAUDE.md`) and any rules synced to the local cache.
