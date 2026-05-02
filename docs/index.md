# AgentSync VCS Documentation

Universal Agent VCS and package manager for AI Agent behaviors.

## Overview
`agentsync-vcs` is a behavior compiler and distribution system for AI agents. It allows you to maintain a single source of truth for agent rules in Git and compiles them into native configurations for tools like Cursor, Claude Code, and Copilot.

## Key Features
- **Universal Rule Format**: Write rules once in Markdown with YAML frontmatter.
- **Multi-IDE Support**: Automatically translates rules for Cursor, Claude, Copilot, Windsurf, and Trae.
- **Remote Syncing**: Sync shared team rules from Git repositories.
- **Enterprise Ready**: Modular architecture, extensible adapters, and robust CLI.

## Quick Start
1.  **Install**: `pip install agentsync-vcs`
2.  **Initialize**: `agentsync-vcs init`
3.  **Compile**: `agentsync-vcs pull cursor`

## Documentation Sections
- [Configuration](configuration.md): Setup and rule definition.
- [Adapters](adapters.md): Detailed target support.
- [Integration Examples](examples.md): Real-world scenarios.
- [Performance Benchmarks](benchmarks.md): Scalability and stress tests.
- [Architecture](architecture.md): How it works under the hood.
