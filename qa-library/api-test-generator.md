# API Test Generator Prompt

## Purpose:
Use this prompt to generate API tests using Python + requests library.

## Prompt Template:
"Generate a Python pytest test for the following API endpoint:
- Endpoint: {endpoint}
- Method: {method}
- Request Body: {request_body}
- Expected Status Code: {status_code}
- Expected Response: {expected_response}

Requirements:
- Use Python requests library
- Include status code assertion
- Include response body validation
- Include error handling
- Follow AAA pattern (Arrange, Act, Assert)"

## Example Usage:
- Endpoint: https://biletebi.ge/api/login
- Method: POST
- Request Body: { "username": "test@mail.com", "password": "pass123" }
- Expected Status Code: 200
- Expected Response: { "token": "abc123" }