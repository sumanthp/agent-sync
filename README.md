# agentsync-vcs

Universal Agent VCS and package manager for AI Agent behaviors.

[![CI](https://github.com/sumanthp/agent-sync/actions/workflows/ci.yml/badge.svg)](https://github.com/sumanthp/agent-sync/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/sumanthp/agent-sync/branch/main/graph/badge.svg)](https://codecov.io/gh/sumanthp/agent-sync)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

## Overview

`agentsync-vcs` is not just a file mirror; it is a **behavior compiler and distribution system** for AI agents. 

Unlike tools that merely copy text between IDEs, `agentsync-vcs` allows you to maintain a single, versioned source of truth in Git and compiles it into the optimized, native configuration for every AI tool in your stack (Cursor, Claude Code, Copilot, etc.). It enables engineering teams to enforce architectural standards and "harness engineering" guidelines across any environment.

### Supported Targets
- **Cursor**: `.cursor/rules/*.mdc` and `.cursorrules`
- **Claude Code**: `CLAUDE.md` and `.claude/skills/`
- **GitHub Copilot**: `.github/copilot-instructions.md` and `.github/instructions/*.md`
- **Windsurf**: `.windsurf/rules/*.md` and `.windsurfrules`
- **Trae**: `.trae/project_rules.md` and `.trae/skills/*.md`
- **Codex**: `AGENTS.md`
- **Gemini**: `GEMINI.md`

## Installation

### Prerequisites
- Python 3.8+

### Install via pip
```bash
pip install agentsync-vcs
```

## Usage

### Initialize a project
```bash
agentsync-vcs init
```
This creates a `sample-rule.md` file and a `.agent-sync/` configuration folder.

### Define a Rule
Create a `.md` file with YAML frontmatter:
```markdown
---
name: my-rule
description: Guidelines for this project
globs: ["src/**/*.ts"]
type: rule # Optional: 'rule', 'skill', or 'global'
---
- Use functional programming patterns.
- Ensure all exports are documented.
```

### Advanced Targets
- **Claude Code**: Rules with `type: skill` are compiled into `.claude/skills/<name>/SKILL.md`. Others go to `CLAUDE.md`.
- **Cursor**: Rules with `type: global` or `always_apply: true` (with no globs) are compiled into `.cursorrules`. Others go to `.cursor/rules/*.mdc`.

### Remote Syncing
Sync rules from a shared team repository:
```bash
agentsync-vcs remote add https://github.com/my-org/agent-rules.git
agentsync-vcs sync
agentsync-vcs pull cursor
```
This will compile both your local rules and all rules from the remote Git repositories.

## Documentation
For detailed guides on configuration, architecture, and IDE-specific adapters, see the [Documentation](docs/index.md).

- [Configuration Guide](docs/configuration.md)
- [Integration Examples](docs/examples.md)
- [Adapters Reference](docs/adapters.md)
- [Architecture Overview](docs/architecture.md)

## License

This project is licensed under the **Apache License 2.0 with Commons Clause v1.0**. 

This means:
- **Free for personal and internal use.**
- **No Commercial Sale/Hosting:** You cannot sell the software or provide it as a paid service (e.g., hosting, support, or consulting where the value is derived substantially from the software) without explicit permission.
- **Licensor retains all rights:** The original author (Sumanth Polisetty) retains the right to distribute and sell the software commercially.

See the [LICENSE](LICENSE) file for the full text.
