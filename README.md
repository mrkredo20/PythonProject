# QA Automation Project - Playwright + Python

## 📁 Structure
- `pages/` — Page Object Model classes
- `tests/` — Test files
- `qa-library/` — AI Prompt templates

## ▶️ How to Run

1. Install dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

2. Run all tests:
```bash
pytest tests/ --headed
```

3. Run specific test:
```bash
pytest tests/test_login.py -v
```

## 🤖 AI Part
Prompts in `qa-library/` are used to generate test cases via AI.

## 🔄 Self-Healing
`pages/self_healing.py` tries multiple selectors automatically when UI changes.