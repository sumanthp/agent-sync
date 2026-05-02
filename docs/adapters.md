# Adapters Reference

`agentsync-vcs` supports a variety of AI agent targets. Each adapter translates the universal rule format into the native configuration required by the target IDE or tool.

## Supported Targets

### Cursor
- **Files**: `.cursor/rules/*.mdc`, `.cursorrules`
- **Logic**:
    - Rules with `type: global` or `always_apply: true` (and no globs) are compiled into `.cursorrules`.
    - All other rules are compiled into individual `.mdc` files in `.cursor/rules/`.

### Claude Code
- **Files**: `CLAUDE.md`, `.claude/skills/<skill-name>/SKILL.md`
- **Logic**:
    - Rules with `type: skill` are compiled into project-specific skills in `.claude/skills/`.
    - All other rules are merged into `CLAUDE.md`.

### GitHub Copilot
- **Files**: `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`
- **Logic**:
    - Rules with `globs` are compiled into path-specific `.instructions.md` files.
    - Rules without `globs` are merged into the repository-wide `copilot-instructions.md`.

### Windsurf
- **Files**: `.windsurf/rules/*.md`, `.windsurfrules`
- **Logic**:
    - Rules with `type: global` are compiled into `.windsurfrules`.
    - All other rules are compiled into the `.windsurf/rules/` directory.

### Trae
- **Files**: `.trae/project_rules.md`, `.trae/skills/*.md`
- **Logic**:
    - Rules with `type: skill` are compiled into the `.trae/skills/` directory.
    - All other rules are merged into `.trae/project_rules.md`.

### Gemini & Codex
- **Files**: `GEMINI.md`, `AGENTS.md`
- **Logic**: All rules are merged into these single-file targets.
