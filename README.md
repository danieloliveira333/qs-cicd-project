# QS Project — Todo Manager

Base project for **Project #5: AI-Enabled Quality Gates in CI/CD**  
Qualidade de Software 2025/26 — Universidade da Beira Interior

## Structure

```
qs-project/
├── src/
│   └── todo_manager.py      # Main module
├── tests/
│   └── test_todo_manager.py # Unit tests
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions pipeline (to be added)
├── requirements.txt
├── pytest.ini
└── README.md
```

## Run tests locally

```bash
pip install -r requirements.txt
pytest --cov=src tests/
```
