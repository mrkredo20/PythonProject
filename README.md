# QA Automation Project

This repository contains biletebi.ge UI and API automated tests built with Python.

Tech stack:
- Playwright + pytest for UI tests
- requests + pytest for API tests
- Page Object Model for UI flows

## Structure

- `pages/`: Playwright page objects and self-healing support
- `tests/`: UI test suite
- `tests/api/`: API test suite
- `qa-library/`: reusable AI prompt templates for generating tests

## Current Coverage

UI coverage includes:
- search flow
- login
- forgot password
- registration start and OTP-entry preparation
- session management
- self-healing login selectors

API coverage includes:
- authorization via `POST /AccessToken`
- current-user profile via `GET /Users`
- registration init via `POST /Users/with-otp/init`

Covered API cases:
- valid login
- wrong password
- missing email
- missing password
- invalid email format
- protected endpoint with valid token
- protected endpoint without token
- protected endpoint with invalid token
- registration with new email
- registration with existing email
- registration with missing email
- registration with invalid email format

## Setup

Install dependencies:

```powershell
pip install -r requirements.txt
playwright install chromium
```

## Environment Variables

UI and API auth tests use:

```powershell
$env:BILETEBI_EMAIL="your_email"
$env:BILETEBI_PASSWORD="your_password"
```

Optional variables:

```powershell
$env:BILETEBI_EXISTING_EMAIL="existing_user@example.com"
$env:BILETEBI_IDENTITY_API_BASE_URL="https://identity-api.biletebi.ge"
$env:ENABLE_ARTIFACTS="1"
```

For future OTP-enabled registration flow:

```powershell
$env:BILETEBI_NEW_REGISTRATION_EMAIL="new_user@example.com"
$env:BILETEBI_REGISTRATION_OTP="12345"
$env:BILETEBI_REGISTRATION_PASSWORD="StrongPassword123!"
```

## Running Tests

Run the full suite:

```powershell
python -m pytest -q -ra
```

Run all UI tests:

```powershell
python -m pytest tests -q -ra
```

Run all API tests:

```powershell
python -m pytest tests/api -q -ra
```

Run a specific file:

```powershell
python -m pytest tests/test_login.py -v
python -m pytest tests/api/test_auth_api.py -v
```

Run headed UI tests:

```powershell
python -m pytest tests --headed -v
```

Run by marker:

```powershell
python -m pytest -m api
python -m pytest -m auth
python -m pytest -m registration
python -m pytest -m "guest and not slow"
```

## Markers

Available pytest markers:
- `api`
- `auth`
- `guest`
- `registration`
- `forgot_password`
- `session`
- `self_healing`
- `smoke`
- `slow`

## Self-Healing Support

`pages/self_healing.py` retries fallback selectors automatically and prints which selector was used.

## Failure Artifacts

If you want screenshots and Playwright traces on failure, enable:

```powershell
$env:ENABLE_ARTIFACTS="1"
```

Artifacts are saved under:
- `test-artifacts/screenshots/`
- `test-artifacts/traces/`

## Current Status

Latest verified results:
- API suite: `12 passed in 5.84s`
- Full suite: `26 passed, 2 skipped, 2 xfailed in 88.41s`

Known non-passing cases:
- `tests/test_manual_test_case.py` is a placeholder scaffold and is intentionally skipped
- `tests/test_register.py` OTP/password-step case is skipped until OTP retrieval or bypass is available
- two session logout tests are marked `xfail` because the live logout flow does not clear auth cookies reliably

## Notes

- Registration is currently OTP-gated on the live site
- Full end-to-end registration completion needs OTP bypass or OTP retrieval support from the backend or test environment
- API tests are based on the live biletebi identity service behavior observed on April 6, 2026
