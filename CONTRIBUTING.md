# Contributing to Agentic AI Demo — Financial Planner

Thank you for your interest in contributing. This document explains how to set up a development environment, run the app locally, and the preferred workflow for contributing changes.

Getting started
---------------
1. Fork the repository and clone your fork:

```bash
git clone <your-fork-url>
cd AgenticAIDemo
```

2. Work from a feature branch:

```bash
git checkout -b feat/your-feature-name
```

3. Set up a Python virtual environment and install dependencies (see `financial_planner/README.md` for details):

```powershell
cd financial_planner
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Running the app locally
-----------------------
Use the included helper script from the `financial_planner` directory:

```powershell
cd financial_planner
.\run_local.ps1
```

Or manually (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
$env:FLASK_APP = "app.py"
$env:FLASK_DEBUG = "1"
flask run
```

Code style and tests
--------------------
- Keep functions small and focused.
- Use clear variable names and avoid hard-coding secrets.
- Add unit tests for calculation logic when possible.
- If you add new endpoints, include small integration tests.

Submitting changes
------------------
1. Commit changes to your branch with clear messages.
2. Push your branch to your fork and open a PR against this repository's `main` branch.
3. In the PR description include:
   - Short summary of changes
   - How to run/test
   - Any known issues or limitations

Security
--------
- Do not include your OpenAI API key or other secrets in commits.
- If you accidentally commit a secret, rotate the secret and remove it from the Git history.

Support
-------
If you want the maintainer to run your changes locally or review specific behavior, include sample inputs and expected outputs in your PR.

Thank you for improving the project!