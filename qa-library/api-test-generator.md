# API Test Generator Prompt Pack

## Purpose
Use these prompts to generate API tests with Python, `pytest`, and `requests`.

The prompts below are designed to produce tests that are:
- fast
- readable
- reusable
- less brittle than full-response equality checks

## Default Requirements
Unless stated otherwise, generated tests should:
- use `requests`
- use `pytest`
- use `timeout=10`
- follow AAA pattern: Arrange, Act, Assert
- assert both status code and important response fields
- prefer partial JSON assertions over full-body equality when possible
- avoid hardcoding secrets directly in test files

## Recommended Inputs
When using these prompts, include as many of these as possible:
- `Base URL: {base_url}`
- `Endpoint: {endpoint}`
- `Method: {method}`
- `Headers: {headers}`
- `Query Params: {query_params}`
- `Request Body: {request_body}`
- `Expected Status: {status_code}`
- `Expected Response Keys: {expected_keys}`
- `Expected Error Message: {expected_error}`
- `Auth Type: {auth_type}`

---

## Prompt 1 - Basic Endpoint Test
"Generate a Python pytest test for this API:
- Base URL: {base_url}
- Endpoint: {endpoint}
- Method: {method}
- Headers: {headers}
- Request Body: {request_body}
- Expected Status: {status_code}
- Expected Response: {expected_response}

Requirements:
- Use Python `requests`
- Use `timeout=10`
- Include status assertion
- Include JSON body assertions
- If full response equality is brittle, assert only key fields
- Follow AAA pattern."

## Prompt 2 - Auth Token Flow
"Generate a Python pytest test that:
1. Sends `POST` to `{login_endpoint}` with credentials
2. Asserts login returns `{login_status}`
3. Extracts auth token from response key `{token_key}`
4. Uses that token to call `{protected_endpoint}`
5. Sends the token as `{auth_header_format}`
6. Asserts the protected endpoint returns `200`

Requirements:
- Use Python `requests`
- Use `timeout=10`
- Assert the token exists and is non-empty
- Assert key fields in the protected response
- Keep the code reusable and readable."

## Prompt 3 - Negative API Tests
"Generate Python pytest tests for invalid API calls to `{endpoint}`:
- Wrong credentials -> expect `{wrong_credentials_status}`
- Missing fields -> expect `{missing_fields_status}`
- Invalid format -> expect `{invalid_format_status}`

Requirements:
- Use Python `requests`
- Use `timeout=10`
- Create separate pytest test functions
- Assert status code
- Assert important error message or error code fields from the JSON body
- Do not rely only on raw text matching if structured error data exists."

## Prompt 4 - Authenticated CRUD Test
"Generate Python pytest tests for this authenticated API flow:
- Login endpoint: {login_endpoint}
- Token key: {token_key}
- Create endpoint: {create_endpoint}
- Get endpoint: {get_endpoint}
- Update endpoint: {update_endpoint}
- Delete endpoint: {delete_endpoint}

Requirements:
- Use Python `requests`
- Reuse the auth token across calls
- Assert expected status codes for create/get/update/delete
- Assert the created resource fields
- Use clear Arrange/Act/Assert sections."

## Prompt 5 - Protected Endpoint Access Test
"Generate Python pytest tests for protected endpoint access on `{endpoint}`:
- No token -> expect `{unauthorized_status}`
- Invalid token -> expect `{invalid_token_status}`
- Valid token -> expect `200`

Requirements:
- Use Python `requests`
- Generate separate tests for each case
- Assert both status codes and important response fields/messages."

---

## Recommended Assertion Style

Prefer this:
```python
assert response.status_code == 200
data = response.json()
assert "token" in data
assert data["token"]
```

Over this:
```python
assert response.json() == {...full large response...}
```

Use full equality only when the response is small and stable.

---

## Example 1 - Basic Endpoint Prompt

Input:
- Base URL: `https://api.example.com`
- Endpoint: `/users/123`
- Method: `GET`
- Headers: `{"Accept": "application/json"}`
- Expected Status: `200`
- Expected Response: `{"id": 123, "name": "Test User"}`

Prompt:
"Generate a Python pytest test for this API:
- Base URL: https://api.example.com
- Endpoint: /users/123
- Method: GET
- Headers: {\"Accept\": \"application/json\"}
- Expected Status: 200
- Expected Response: {\"id\": 123, \"name\": \"Test User\"}
Use requests library, timeout=10, and include status and body assertions."

## Example 2 - Auth Token Prompt

Prompt:
"Generate a Python pytest test that:
1. Sends POST to `/auth/login` with credentials
2. Asserts login returns 200
3. Extracts auth token from response key `token`
4. Uses that token to call `/users/me`
5. Sends the token as `Authorization: Bearer <token>`
6. Asserts the protected endpoint returns 200
Use requests library and include status/body assertions."

## Example 3 - Negative Test Prompt

Prompt:
"Generate Python pytest tests for invalid API calls to `/auth/login`:
- Wrong credentials -> expect 401
- Missing fields -> expect 400
- Invalid format -> expect 422
Use requests library, timeout=10, and include assertions for status and error fields."

---

## Practical Notes
- If the API returns tokens in cookies instead of JSON, tell the generator that explicitly.
- If the API uses API keys, include the exact header format.
- If validation returns `400` instead of `422`, use the real backend behavior instead of a generic guess.
- If the endpoint is unstable or response payload is large, assert only critical keys.

## Suggested Repo Structure
For generated API tests, prefer:
- `tests/api/test_auth_api.py`
- `tests/api/test_registration_api.py`
- `tests/api/test_forgot_password_api.py`
- `tests/api/test_profile_api.py`

Keep shared helpers in:
- `tests/api/conftest.py`
- `tests/api/helpers.py`
