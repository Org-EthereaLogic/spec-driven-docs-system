# API Documentation Template

## Purpose
This template defines the structure and requirements for API documentation. Use this template when documenting REST APIs, GraphQL endpoints, or other programmatic interfaces.

## Target Audience
- Backend developers integrating with the API
- Frontend developers consuming API data
- Third-party developers building integrations
- DevOps engineers configuring API access

---

## Minimal Variant

For simple APIs with few endpoints, use this reduced structure:

1. **Overview** - Purpose, base URL
2. **Authentication** - How to authenticate (if applicable)
3. **Core Endpoints** - 2-3 most commonly used endpoints

Skip Rate Limits, Changelog, and exhaustive error documentation for v1.0. Add them when needed.

### When to Use Minimal Variant
- API has fewer than 10 endpoints
- Internal or limited-audience API
- MVP or early-stage product
- Simple CRUD operations

---

## Scope Guidance

**Include only sections relevant to this specific API:**
- If the API has no rate limiting, skip Rate Limits section
- If there's only one authentication method, keep Authentication brief
- Document common error codes, not every possible error
- One representative example per endpoint is sufficient

**Anti-Bloat Warning:**
- Do not add sections for hypothetical future needs
- Do not document internal implementation details
- Do not exhaustively list all error codes if users rarely encounter them

---

## Full Variant Sections

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
**Purpose:** Document API endpoints so developers can use them effectively.

**Per-Endpoint Guidance (include what's relevant):**
- HTTP method and path (required)
- Brief description (required)
- Parameters that users need to know about
- One clear example request/response
- Common error responses (not exhaustive)

**Note:** Not every endpoint needs all elements. Simple GET endpoints need less than complex POST operations.

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
- Include `curl` examples for core endpoints
- Examples should be runnable (realistic headers and data)
- One good example is better than many incomplete examples

### Tables
- Use tables when there are 3+ parameters
- Columns: Type, Required, Description (add Default if relevant)

### Response Examples
- Show realistic JSON responses
- Success case is required; error cases are helpful but not mandatory for every endpoint

### Terminology
- Use "endpoint" not "route"
- Use "request" not "call"
- Use "response" not "return value"

### Scope Principle
Document what developers need to use the API successfully. Skip implementation details, rare edge cases, and sections that don't apply to this specific API.
