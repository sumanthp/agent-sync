# agentsync-vcs

Universal Agent VCS and package manager for AI Agent behaviors.

## Overview

`agentsync-vcs` allows you to define AI agent rules and contexts in a single, universal Markdown format and compile them into native configurations for various AI tools.

### Supported Targets
- **Cursor**: `.cursor/rules/*.mdc`
- **Claude Code**: `CLAUDE.md`
- **GitHub Copilot**: `.github/copilot-instructions.md` and `.github/instructions/*.md`
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
---
- Use functional programming patterns.
- Ensure all exports are documented.
```

### Remote Syncing
Sync rules from a shared team repository:
```bash
agentsync-vcs remote add https://github.com/my-org/agent-rules.git
agentsync-vcs sync
agentsync-vcs pull cursor
```
This will compile both your local rules and all rules from the remote Git repositories.

## License

This project is licensed under the **Apache License 2.0 with Commons Clause v1.0**. 

This means:
- **Free for personal and internal use.**
- **No Commercial Sale/Hosting:** You cannot sell the software or provide it as a paid service (e.g., hosting, support, or consulting where the value is derived substantially from the software) without explicit permission.
- **Licensor retains all rights:** The original author (Sumanth Polisetty) retains the right to distribute and sell the software commercially.

See the [LICENSE](LICENSE) file for the full text.
