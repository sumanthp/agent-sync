# agent-sync

Universal Agent VCS and package manager for AI Agent behaviors.

## Overview

`agent-sync` allows you to define AI agent rules and contexts in a single, universal Markdown format and compile them into native configurations for various AI tools.

### Supported Targets
- **Cursor**: `.cursor/rules/*.mdc`
- **Claude Code**: `CLAUDE.md`
- **GitHub Copilot**: `.github/copilot-instructions.md` and `.github/instructions/*.md`
- **Codex**: `AGENTS.md`
- **Gemini**: `GEMINI.md`

## Installation

### Prerequisites
- Python 3.8+
- Go 1.21+ (to build the CLI)

### Building the CLI
1. Clone the repository.
2. Run `go build -o agent-sync ./cmd/agent-sync`
3. Add the resulting binary to your PATH.

### Python Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Initialize a project
```bash
agent-sync init
```
This creates a `sample-rule.md` file.

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

### Pull and Compile
```bash
agent-sync pull cursor
agent-sync pull claude
agent-sync pull copilot
```

## License

This project is licensed under the **Apache License 2.0 with Commons Clause v1.0**. 

This means:
- **Free for personal and internal use.**
- **No Commercial Sale/Hosting:** You cannot sell the software or provide it as a paid service (e.g., hosting, support, or consulting where the value is derived substantially from the software) without explicit permission.
- **Licensor retains all rights:** The original author (Sumanth Polisetty) retains the right to distribute and sell the software commercially.

See the [LICENSE](LICENSE) file for the full text.
