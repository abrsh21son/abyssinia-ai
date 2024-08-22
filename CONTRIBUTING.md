# Contributing to Abyssinia AI

Thank you for your interest in contributing!

## How to Contribute
1. Fork the repository.
2. Create a branch: git checkout -b feature/my-feature
3. Commit with clear messages following Conventional Commits.
4. Run pytest tests/ to verify all tests pass.
5. Open a Pull Request with a clear description.

## Code Standards
- PEP 8 style
- Type hints on all public functions
- Docstrings for all public classes and functions

## Adding Corpus Documents
1. Add .txt files (UTF-8) to data/
2. Delete chroma_db/ to force re-embedding
3. Restart the app

## Reporting Bugs
Open a GitHub issue with steps to reproduce and expected vs actual behaviour.