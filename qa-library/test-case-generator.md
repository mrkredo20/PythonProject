# Test Case Generator Prompt

## Purpose:
Use these prompts to generate full test case lists before writing code.

---

## Prompt 1 — Full feature test cases:
"Generate a complete test case table for:
- Feature: {feature_name}
- App: {app_name}
- User Role: {user_role}
Include positive, negative, and edge cases.
Format as table: ID | Title | Steps | Expected Result"

## Prompt 2 — Edge cases only:
"Generate edge case tests for {feature} on {app}:
- Empty inputs
- Maximum character limits
- Special characters (!@#$%)
- Copy-pasted whitespace
- Very long strings
Format as table: ID | Input | Expected Result"

## Prompt 3 — Regression test cases:
"Generate a regression test checklist for {feature} on {app}.
Include the most critical user flows that must always work.
Format as a simple checklist with pass/fail column."

