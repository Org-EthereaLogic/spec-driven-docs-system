# API Documentation Template

## Purpose
This template defines the structure and requirements for API documentation. Use this template when documenting REST APIs, GraphQL endpoints, or other programmatic interfaces.

## Target Audience
- Backend developers integrating with the API
- Frontend developers consuming API data
- Third-party developers building integrations
- DevOps engineers configuring API access

---

## Required Sections

### 1. Overview
**Purpose:** Introduce the API, its purpose, and key capabilities.

**Must Include:**
- API name and version
- Brief description (1-2 sentences)
- Base URL(s) for each environment
- API style (REST, GraphQL, gRPC)
- Key capabilities and use cases

**Example Structure:**
```markdown
# [API Name] API Reference

Version: [X.Y.Z]

The [API Name] API provides [brief description of what it does].

## Base URLs

| Environment | URL |
|-------------|-----|
| Production  | `https://api.example.com/v1` |
| Staging     | `https://api.staging.example.com/v1` |

## Key Features
- [Feature 1]
- [Feature 2]
```

---

### 2. Authentication
**Purpose:** Explain how to authenticate with the API.

**Must Include:**
- Supported authentication methods
- How to obtain credentials
- Token format and placement
- Token expiration and refresh
- Code example for authentication

**Example Structure:**
```markdown
## Authentication

This API uses [Bearer tokens/API keys/OAuth 2.0] for authentication.

### Obtaining Credentials
[Steps to get API keys or tokens]

### Using Your Token
Include the token in the `Authorization` header:

\`\`\`bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.example.com/v1/resource
\`\`\`

### Token Expiration
Tokens expire after [duration]. To refresh, [instructions].
```

---

### 3. Endpoints
**Purpose:** Document each API endpoint comprehensively.

**Per-Endpoint Requirements:**
- HTTP method and path
- Brief description
- Parameters (path, query, body)
- Request headers
- Request body schema (if applicable)
- Response schema
- Example request/response pair
- Error responses

**Example Structure:**
```markdown
## Endpoints

### [Resource Name]

#### Get [Resource]

Retrieves a single [resource] by ID.

\`\`\`
GET /resources/{id}
\`\`\`

**Path Parameters:**

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| id        | string | Yes      | Unique identifier for the resource |

**Query Parameters:**

| Parameter | Type    | Required | Description | Default |
|-----------|---------|----------|-------------|---------|
| include   | string  | No       | Related resources to include | none |

**Response:**

\`\`\`json
{
  "id": "abc123",
  "name": "Example Resource",
  "created_at": "2025-01-01T00:00:00Z"
}
\`\`\`

**Error Responses:**

| Status | Code | Description |
|--------|------|-------------|
| 404    | RESOURCE_NOT_FOUND | The requested resource does not exist |
| 401    | UNAUTHORIZED | Invalid or missing authentication token |
```

---

### 4. Error Handling
**Purpose:** Document the error response format and common errors.

**Must Include:**
- Error response structure
- List of common error codes
- Error code meanings
- Recovery suggestions

**Example Structure:**
```markdown
## Error Handling

### Error Response Format

All errors return a consistent JSON structure:

\`\`\`json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}
  }
}
\`\`\`

### Common Error Codes

| HTTP Status | Code | Description | Recovery |
|-------------|------|-------------|----------|
| 400 | INVALID_REQUEST | Malformed request body | Check request format |
| 401 | UNAUTHORIZED | Missing or invalid token | Refresh your token |
| 403 | FORBIDDEN | Insufficient permissions | Request access |
| 404 | NOT_FOUND | Resource does not exist | Verify the ID |
| 429 | RATE_LIMITED | Too many requests | Wait and retry |
| 500 | INTERNAL_ERROR | Server error | Retry with backoff |
```

---

### 5. Rate Limits
**Purpose:** Document API rate limiting behavior.

**Must Include:**
- Rate limit values
- How limits are calculated
- Rate limit headers
- How to handle rate limiting

**Example Structure:**
```markdown
## Rate Limits

API requests are limited to ensure fair usage.

### Limits

| Plan       | Requests/minute | Requests/day |
|------------|-----------------|--------------|
| Free       | 60              | 1,000        |
| Pro        | 600             | 50,000       |
| Enterprise | Custom          | Custom       |

### Rate Limit Headers

Each response includes rate limit information:

| Header | Description |
|--------|-------------|
| X-RateLimit-Limit | Maximum requests allowed |
| X-RateLimit-Remaining | Requests remaining in window |
| X-RateLimit-Reset | Unix timestamp when limit resets |

### Handling Rate Limits

When rate limited, you'll receive a `429` response. Wait until `X-RateLimit-Reset` before retrying.
```

---

### 6. Changelog
**Purpose:** Document API version history and changes.

**Must Include:**
- Version number
- Release date
- Breaking changes (clearly marked)
- New features
- Deprecations
- Bug fixes

**Example Structure:**
```markdown
## Changelog

### v2.1.0 (2025-01-15)
- **New:** Added `GET /users/{id}/preferences` endpoint
- **Changed:** `created_at` now returns ISO 8601 format
- **Deprecated:** `GET /users/{id}/settings` - use preferences instead

### v2.0.0 (2025-01-01) - Breaking Changes
- **Breaking:** Removed `api_key` query parameter authentication
- **Breaking:** Changed error response format
- **New:** OAuth 2.0 authentication support
```

---

## Optional Sections

### Quick Start
Brief getting-started guide for common use cases.

### SDKs and Libraries
Links to official client libraries.

### Webhooks
Documentation for webhook integrations.

### Pagination
Detailed pagination patterns if applicable.

### Filtering and Sorting
Query parameter patterns for list endpoints.

---

## Style Guidelines

### Code Examples
- Always include `curl` examples
- Show complete, runnable commands
- Include all required headers
- Use realistic example data

### Tables
- Use tables for 3+ parameters
- Include Type, Required, Description columns minimum
- Add Default column when applicable

### Response Examples
- Show complete JSON responses
- Include realistic data values
- Document both success and error cases

### Terminology
- Use "endpoint" not "route"
- Use "request" not "call"
- Use "response" not "return value"
