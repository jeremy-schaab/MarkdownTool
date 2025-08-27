# API Test File

This file tests code block rendering with different languages.

## HTTP Requests

```http
GET /api/v1/analytics/combined
GET /api/v1/analytics/journal-details  
GET /api/v1/analytics/balances
GET /api/v1/analytics/account-segments
GET /api/v1/analytics/rollups
```

## Python Code

```python
def test_function():
    return "Hello, World!"

# This should render properly
result = test_function()
print(result)
```

## JavaScript

```javascript
const apiEndpoints = [
    '/api/v1/analytics/combined',
    '/api/v1/analytics/journal-details',
    '/api/v1/analytics/balances',
    '/api/v1/analytics/account-segments',
    '/api/v1/analytics/rollups'
];

apiEndpoints.forEach(endpoint => {
    console.log(`Calling ${endpoint}`);
});
```

## Plain Code Block

```
This is a plain code block
No syntax highlighting
Should still format properly
```

## Inline Code

Here is some `inline code` in a sentence.

This tests whether code blocks are properly handled by the markdown renderer.