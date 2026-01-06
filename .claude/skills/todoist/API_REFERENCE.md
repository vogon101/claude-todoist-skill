# Todoist REST API Reference

Base URL: `https://api.todoist.com/rest/v2`

All requests require authentication header:
```
Authorization: Bearer $TODOIST_API_TOKEN
```

## Tasks

### Get All Active Tasks

**Endpoint**: `GET /tasks`

**Query Parameters**:
- `project_id` (optional): Filter by project ID
- `label` (optional): Filter by label name
- `filter` (optional): Filter by any supported filter (e.g., "today", "overdue")
- `lang` (optional): Language for due dates (default: en)

**Example**:
```bash
curl -s "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN"
```

**Response** (200 OK):
```json
[
  {
    "id": "2995104339",
    "project_id": "2203306141",
    "content": "Buy groceries",
    "description": "",
    "due": {
      "date": "2026-01-07",
      "string": "tomorrow",
      "lang": "en",
      "is_recurring": false
    },
    "priority": 4,
    "labels": ["shopping"],
    "order": 1,
    "url": "https://todoist.com/showTask?id=2995104339",
    "created_at": "2026-01-06T10:00:00Z"
  }
]
```

### Get a Single Task

**Endpoint**: `GET /tasks/{id}`

**Example**:
```bash
curl -s "https://api.todoist.com/rest/v2/tasks/2995104339" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN"
```

### Create a Task

**Endpoint**: `POST /tasks`

**Headers**:
- `Authorization: Bearer $TODOIST_API_TOKEN`
- `Content-Type: application/json`

**Body Parameters**:
- `content` (required): Task name/content
- `description` (optional): Task description
- `project_id` (optional): Project ID (default: Inbox)
- `due_string` (optional): Natural language due date (e.g., "tomorrow at 12:00")
- `due_date` (optional): ISO 8601 date (e.g., "2026-01-07")
- `due_datetime` (optional): ISO 8601 datetime with timezone
- `priority` (optional): 1-4 (1=normal, 4=urgent)
- `labels` (optional): Array of label names
- `assignee_id` (optional): User ID to assign task to

**Example**:
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Review code",
    "description": "Check PR #123 for security issues",
    "due_string": "tomorrow at 14:00",
    "priority": 3,
    "labels": ["work", "code-review"]
  }'
```

**Response** (200 OK):
```json
{
  "id": "2995104340",
  "content": "Review code",
  "description": "Check PR #123 for security issues",
  "due": {
    "date": "2026-01-07",
    "string": "tomorrow at 14:00",
    "datetime": "2026-01-07T14:00:00Z"
  },
  "priority": 3,
  "labels": ["work", "code-review"]
}
```

### Update a Task

**Endpoint**: `POST /tasks/{id}`

**Headers**:
- `Authorization: Bearer $TODOIST_API_TOKEN`
- `Content-Type: application/json`

**Body Parameters** (all optional, include only what you want to change):
- `content`: Update task content
- `description`: Update description
- `due_string`: Update due date with natural language
- `due_date`: Update with ISO date
- `priority`: Update priority (1-4)
- `labels`: Replace labels array

**Example**:
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/tasks/2995104339" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "due_string": "next Friday",
    "priority": 4
  }'
```

### Complete a Task

**Endpoint**: `POST /tasks/{id}/close`

**Example**:
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/tasks/2995104339/close" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN"
```

**Response**: 204 No Content

### Reopen a Task

**Endpoint**: `POST /tasks/{id}/reopen`

**Example**:
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/tasks/2995104339/reopen" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN"
```

**Response**: 204 No Content

### Delete a Task

**Endpoint**: `DELETE /tasks/{id}`

**Example**:
```bash
curl -s -X DELETE "https://api.todoist.com/rest/v2/tasks/2995104339" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN"
```

**Response**: 204 No Content

## Projects

### Get All Projects

**Endpoint**: `GET /projects`

**Example**:
```bash
curl -s "https://api.todoist.com/rest/v2/projects" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN"
```

**Response** (200 OK):
```json
[
  {
    "id": "2203306141",
    "name": "Work",
    "color": "blue",
    "parent_id": null,
    "order": 1,
    "is_favorite": true,
    "is_inbox_project": false,
    "is_shared": false,
    "url": "https://todoist.com/showProject?id=2203306141"
  }
]
```

### Get a Single Project

**Endpoint**: `GET /projects/{id}`

**Example**:
```bash
curl -s "https://api.todoist.com/rest/v2/projects/2203306141" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN"
```

### Create a Project

**Endpoint**: `POST /projects`

**Body Parameters**:
- `name` (required): Project name
- `parent_id` (optional): Parent project ID for sub-projects
- `color` (optional): Color name (e.g., "blue", "red", "green")
- `is_favorite` (optional): Boolean, add to favorites

**Example**:
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/projects" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Home Renovation",
    "color": "green",
    "is_favorite": true
  }'
```

### Update a Project

**Endpoint**: `POST /projects/{id}`

**Body Parameters** (all optional):
- `name`: Update project name
- `color`: Update color
- `is_favorite`: Toggle favorite status

**Example**:
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/projects/2203306141" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Work Projects",
    "color": "purple"
  }'
```

### Delete a Project

**Endpoint**: `DELETE /projects/{id}`

**Example**:
```bash
curl -s -X DELETE "https://api.todoist.com/rest/v2/projects/2203306141" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN"
```

**Response**: 204 No Content

## Sections

### Get All Sections

**Endpoint**: `GET /sections`

**Query Parameters**:
- `project_id` (optional): Filter by project

**Example**:
```bash
curl -s "https://api.todoist.com/rest/v2/sections?project_id=2203306141" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN"
```

### Create a Section

**Endpoint**: `POST /sections`

**Body Parameters**:
- `name` (required): Section name
- `project_id` (required): Project ID
- `order` (optional): Position in project

**Example**:
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/sections" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "In Progress",
    "project_id": "2203306141"
  }'
```

## Labels

### Get All Labels

**Endpoint**: `GET /labels`

**Example**:
```bash
curl -s "https://api.todoist.com/rest/v2/labels" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN"
```

**Response** (200 OK):
```json
[
  {
    "id": "2156154810",
    "name": "work",
    "color": "blue",
    "order": 1,
    "is_favorite": false
  }
]
```

### Create a Label

**Endpoint**: `POST /labels`

**Body Parameters**:
- `name` (required): Label name
- `color` (optional): Color name
- `order` (optional): Position
- `is_favorite` (optional): Boolean

**Example**:
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/labels" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "urgent",
    "color": "red"
  }'
```

## Comments

### Get Task Comments

**Endpoint**: `GET /comments`

**Query Parameters**:
- `task_id` (optional): Filter by task
- `project_id` (optional): Filter by project

**Example**:
```bash
curl -s "https://api.todoist.com/rest/v2/comments?task_id=2995104339" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN"
```

### Create a Comment

**Endpoint**: `POST /comments`

**Body Parameters**:
- `task_id` (required): Task ID
- `content` (required): Comment text

**Example**:
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/comments" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "2995104339",
    "content": "Remember to check the expiration dates!"
  }'
```

## Available Colors

When setting colors for projects or labels:

- `berry_red`
- `red`
- `orange`
- `yellow`
- `olive_green`
- `lime_green`
- `green`
- `mint_green`
- `teal`
- `sky_blue`
- `light_blue`
- `blue`
- `grape`
- `violet`
- `lavender`
- `magenta`
- `salmon`
- `charcoal`
- `grey`
- `taupe`

## Natural Language Due Dates

When using `due_string`, Todoist supports:

**Relative dates**:
- `today`, `tomorrow`, `yesterday`
- `next Monday`, `next week`, `next month`
- `in 3 days`, `in 2 weeks`
- `every day`, `every Monday`, `every 3 days`

**Specific dates**:
- `Jan 23`, `January 23`, `23 Jan`
- `01/23/2026`, `2026-01-23`

**Times**:
- `tomorrow at 9am`
- `next Friday at 14:00`
- `every day at 9:00`

**Recurring**:
- `every day`
- `every Monday and Friday`
- `every 2 weeks`
- `every month on the 1st`
- `every year on Jan 1`

## Rate Limits

- **Free/Personal**: 450 requests per 15 minutes
- **Premium**: 450 requests per 15 minutes
- **Business**: 1500 requests per 15 minutes

When rate limited, you'll receive:
- HTTP Status: 429
- Header: `X-RateLimit-Remaining: 0`

Wait before retrying based on `Retry-After` header.

## Error Responses

Common error format:
```json
{
  "error": "Invalid argument value",
  "error_code": 400
}
```

**Error Codes**:
- `400` - Invalid request format
- `401` - Invalid or missing token
- `403` - Access denied
- `404` - Resource not found
- `429` - Rate limit exceeded
- `500` - Server error

## Best Practices

1. **Use natural language dates**: More readable than ISO dates
2. **Batch operations**: Minimize API calls when possible
3. **Handle rate limits**: Implement exponential backoff
4. **Check response codes**: Always validate before parsing
5. **Use project organization**: Group related tasks
6. **Leverage labels**: Better than creating many projects
7. **Set priorities wisely**: Reserve p4 for truly urgent tasks
8. **Add descriptions**: Provide context for complex tasks
