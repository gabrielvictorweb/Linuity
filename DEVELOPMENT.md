# 🛠️ Development Guide

This document describes how to develop, test, version, and contribute to this CLI project.

We use two workflows:

- 🧑‍💻 **Development environment (recommended)** → fast iteration, testing, debugging
- 👤 **pipx environment** → simulate real user installation

---

# 📦 Project Overview

This is a Python CLI tool distributed as a package.

Goals:

- Smooth developer experience
- Reproducible environments
- Reliable CLI behavior for end users

---

# ⚙️ Prerequisites

Make sure you have:

- Python 3.10+
- pip
- pipx (for CLI testing)

---

# 🧑‍💻 Development Setup (Recommended)

## 1. Clone the repository

```bash
git clone <repo-url>
cd <project-folder>
```

---

## 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## 3. Install project with dev dependencies

```bash
pip install -e .[dev]
```

This installs:

- Project dependencies
- Development tools (pytest, coverage, mocks)
- Project in editable mode

---

## 4. Run tests

```bash
pytest
```

---

## 5. Run lint and format

```bash
ruff check . --fix
ruff format .
```

---

# 👤 Testing as End User (pipx)

To simulate real usage:

```bash
pipx install . --force
```

Run CLI:

```bash
linuity
```

After changes:

```bash
pipx reinstall linuity
```

⚠️ This is **only for validating final CLI behavior**, not for development.

---

# 🔁 Development Workflow

1. Create a branch:

```bash
git checkout -b feature/your-feature-name
```

1. Make changes

2. Run checks:

```bash
ruff check . --fix
pytest
```

1. Commit changes:

```bash
git add .
cz commit
```

1. Push branch:

```bash
git push origin feature/your-feature-name
```

1. Open a Pull Request

---

# 🧪 Testing Strategy

- Unit tests → core logic (domain/application)
- Integration tests → CLI behavior
- Avoid testing framework internals
- Mock external dependencies (e.g. HID devices)

---

# 🧰 Development Tools

Install globally using pipx:

```bash
pipx install pre-commit
pipx install commitizen
```

Enable hooks:

```bash
pre-commit install
```

---

# ✍️ Commit Guidelines

We follow **Conventional Commits**.

Examples:

```bash
feat: add LED control command
fix: handle device disconnect
chore: update dependencies
```

Interactive commit:

```bash
cz commit
```

---

# 🧾 Changelog & Versioning

We use:

- Semantic Versioning (`MAJOR.MINOR.PATCH`)
- Automatic changelog generation

---

## 🚀 Release flow

### 1. Make commits normally

```bash
cz commit
```

---

### 2. Bump version

```bash
cz bump
```

This automatically:

- Updates version
- Updates `CHANGELOG.md`
- Creates commit
- Creates git tag

---

### 3. Push changes and tag

```bash
git push --follow-tags
```

This triggers CI and release workflow.

---

## ⚠️ Important rules

- Do NOT edit `CHANGELOG.md` manually (except small fixes)
- Do NOT use generic commits like `update`
- Always use conventional commits

---

# 🧹 Code Quality

Run before pushing:

```bash
pre-commit run --all-files
```

---

# ⚠️ Important Notes

- Do not commit directly to `main`
- Always use Pull Requests
- Use virtualenv for development
- Use pipx only to validate CLI behavior
- Keep commits small and meaningful

---

# 💡 Summary

- Use virtualenv for development
- Use pipx to simulate real installation
- Use Ruff for linting and formatting
- Use pytest for testing
- Use commitizen for versioning and changelog
- Keep everything reproducible and automated

---
