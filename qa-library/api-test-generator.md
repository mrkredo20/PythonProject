```ts
import { test, expect } from '@playwright/test';
import axios from 'axios';

test('POST /api/login returns token', async () => {
  const endpoint = '/api/login';
  const requestBody = { username: 'test', password: 'pass' };
  const expectedResponse = { token: 'abc123' };

  try {
    const response = await axios.post(endpoint, requestBody);

    expect(response.status).toBe(200);
    expect(response.data).toMatchObject(expectedResponse);
  } catch (error: any) {
    // Axios puts response details on error.response for non-2xx
    if (error.response) {
      throw new Error(
        `Request failed with status ${error.response.status}: ${JSON.stringify(error.response.data)}`
      );
    }
    throw error;
  }
});
```
