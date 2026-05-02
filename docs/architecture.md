# Architecture Overview

`agentsync-vcs` is designed to be a lightweight yet powerful bridge between human-authored behavior guidelines and AI agent consumption.

## Data Flow

1.  **Discovery**: The CLI scans the local project and remote caches for Markdown rules (`.md`).
2.  **Parsing**: Each rule is parsed into an `AgentRule` model (using Pydantic), extracting metadata from YAML frontmatter and behavioral text from the Markdown body.
3.  **Translation**: The selected `BaseAdapter` subclass takes the `AgentRule` and determines:
    - Which file(s) should be created or updated.
    - How the content should be formatted (e.g., adding XML headers for Cursor or sections for Claude).
4.  **Generation**: The CLI writes the translated content to the target paths, creating directories as needed. For shared targets like `CLAUDE.md`, it intelligently merges content from multiple rules.

## Modular Components

- **`cli.py`**: Handles user input, project initialization, and orchestration of the sync/pull flow.
- **`parser.py`**: A robust regex-based parser that handles universal rule formats.
- **`models.py`**: Defines the `AgentRule` schema and shared constants like `SHARED_FILES`.
- **`adapters/`**: A pluggable directory where new IDE targets can be added by implementing the `BaseAdapter` interface.

## Performance
- **Minimal Dependencies**: Built on top of `PyYAML` and `Pydantic` for speed and reliability.
- **Fast Execution**: Designed to run in milliseconds, making it suitable for pre-commit hooks or CI/CD pipelines.
- **Efficient Syncing**: Uses standard Git commands to fetch remote rules, ensuring compatibility with existing enterprise security and authentication.
