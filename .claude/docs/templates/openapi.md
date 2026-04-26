# OpenAPI-Style API Documentation Template

## Purpose

A schema-first API reference structured in the OpenAPI conceptual style: operations grouped by resource, schemas defined separately, and every endpoint has explicit parameter, request, and response specifications. Use this template when building public developer portal documentation or when the team works with OpenAPI specs but does not auto-generate Markdown from them.

## Target Audience

- External developers integrating with the API
- Internal teams that need a reference (not a tutorial)
- Technical writers maintaining a developer portal

## Difference from `api-docs.md`

`api-docs.md` is general-purpose API documentation - flexible structure, prose-heavy where helpful. `openapi.md` enforces a strict, schema-first format suitable for reference documentation where consistency across endpoints matters more than narrative.

## Required Sections

1. Overview
2. Authentication
3. Operations (grouped into sub-sections by resource)
4. Schemas
5. Errors
6. Rate Limits

## Style Guidelines

- Every operation has the same structure: method badge, path, description, parameters table, request body schema, response schema, example pair.
- Schemas are defined once in the Schemas section and referenced from operations.
- Examples must be runnable: a curl command that succeeds against a real environment (or sandbox).
- Use HTTP method badges with consistent formatting: `**GET**`, `**POST**`, `**PUT**`, `**PATCH**`, `**DELETE**`.

---

## Template Body

```markdown
# [API Name] Reference

**Version:** v1
**Base URL:** `https://api.example.com/v1`
**Status:** Stable

## Overview

[One-paragraph description of what this API does, who it is for, and how it differs from other APIs in the system. Link to a separate Getting Started guide if one exists - this document is reference, not tutorial.]

## Authentication

[Brief description of the auth mechanism. Show one minimal example.]

```http
Authorization: Bearer YOUR_API_TOKEN
```

For details on obtaining tokens, see [Getting Started].

## Operations

### Resource: [Resource Name]

#### List [resources]

**GET** `/resources`

[One-sentence description of what this operation does.]

**Query parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `limit` | integer | No | Maximum results (default: 20, max: 100) |
| `cursor` | string | No | Pagination cursor from previous response |

**Response:** `200 OK` - Returns [`ResourceList`](#resourcelist)

**Example request:**

```bash
curl https://api.example.com/v1/resources?limit=10 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Example response:**

```json
{
  "items": [
    {"id": "res_001", "name": "Example", "created_at": "2026-01-01T00:00:00Z"}
  ],
  "next_cursor": "eyJpZCI6InJlc18wMDEifQ"
}
```

#### Get [resource]

**GET** `/resources/{id}`

[Description.]

**Path parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | string | Yes | Resource identifier |

**Response:** `200 OK` - Returns [`Resource`](#resource)

[... continue for each operation ...]

## Schemas

### Resource

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier, format `res_[a-z0-9]+` |
| `name` | string | Human-readable name |
| `created_at` | string (ISO 8601) | Creation timestamp |

### ResourceList

| Field | Type | Description |
|-------|------|-------------|
| `items` | array of [`Resource`](#resource) | Page of results |
| `next_cursor` | string \| null | Pass to next request, or null if no more pages |

## Errors

All error responses use this structure:

```json
{
  "error": {
    "code": "string",
    "message": "Human-readable description",
    "request_id": "req_abc123"
  }
}
```

| HTTP Status | Error Code | Meaning |
|-------------|------------|---------|
| 400 | `invalid_request` | Request was malformed |
| 401 | `unauthenticated` | Missing or invalid token |
| 403 | `forbidden` | Authenticated but not authorized |
| 404 | `not_found` | Resource does not exist |
| 429 | `rate_limited` | Too many requests, see Rate Limits |
| 500 | `internal_error` | Server error - retry with backoff |

## Rate Limits

[Concrete numbers: requests per minute, per token, per IP. Include the headers returned: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.]
```

---

## Anti-Bloat Warning

Do NOT add:

- Tutorials or "Getting Started" content (those belong elsewhere)
- Architectural background (link to a design doc)
- Endpoints that do not exist yet (this is reference for what is shipped)
- Schemas referenced only once (inline them in the operation instead)
