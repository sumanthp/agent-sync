# Contributing to AgentSync VCS

Thank you for your interest in contributing to `agentsync-vcs`! As an enterprise-grade tool, we maintain high standards for code quality and behavioral consistency.

## Code of Conduct
Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute
1.  **Fork the Repository**: Create your own fork of the repo.
2.  **Create a Branch**: Use a descriptive name like `feat/new-adapter` or `fix/parser-bug`.
3.  **Implement Changes**: Ensure your code follows the existing style and includes type hints.
4.  **Add Tests**: Every feature or fix MUST have corresponding tests in the `tests/` directory.
5.  **Run Benchmarks**: If modifying the core engine, run `python tests/benchmark_performance.py` to ensure no performance regressions.
6.  **Submit a PR**: Provide a detailed description of your changes and why they are needed.

## Development Setup
```bash
git clone https://github.com/sumanthp/agent-sync.git
cd agent-sync
pip install -e ".[dev]"
```

## Testing & Quality
We use the following tools to maintain standards:
- **Unittest**: For functional tests.
- **Ruff**: For linting.
- **MyPy**: For static type checking.
- **Coverage**: We aim for >90% code coverage.
