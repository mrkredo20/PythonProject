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