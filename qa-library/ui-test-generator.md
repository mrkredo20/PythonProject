# UI Test Generator Prompt

## Purpose:
Use this prompt to generate Playwright UI tests using Page Object Model pattern.

## Prompt Template:
"Generate a Playwright + Python UI test using Page Object Model for:
- Website: {url}
- Feature: {feature_name}
- Test Steps: {steps}
- Expected Result: {expected_result}

Requirements:
- Create a page class in pages/ folder
- Create a test file in tests/ folder
- Use pytest fixtures for browser setup
- Include assertions for each step"

## Example Usage:
- Website: https://biletebi.ge
- Feature: User Login
- Steps: Navigate to login, enter email, enter password, click submit
- Expected Result: User is redirected to homepage

---

## Prompt 1 — Basic UI flow:
"Generate a Playwright + Python test using Page Object Model for:
- Website: {url}
- Feature: {feature}
- Steps: {steps}
- Expected Result: {expected}
Create a page class in pages/ and test in tests/."

## Prompt 2 — Form validation test:
"Generate Playwright tests for form validation on {url}:
- Test empty fields → expect error messages
- Test invalid email format → expect validation error
- Test mismatched passwords → expect error
- Test successful submit → expect redirect to {success_url}
Use POM pattern."

## Prompt 3 — Navigation & redirect test:
"Generate a Playwright test that:
1. Goes to {url}
2. Logs in with {credentials}
3. Verifies redirect to {expected_url}
4. Checks that {element} is visible on the page
5. Clicks logout and verifies redirect back to login"