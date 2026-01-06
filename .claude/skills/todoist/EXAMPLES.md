# Todoist Usage Examples

This document provides concrete examples of common Todoist workflows.

## Example 1: Show Today's Tasks

**User Request**: "What's on my Todoist for today?"

**Implementation**:
```bash
# Get all active tasks
TASKS=$(curl -s "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN")

# Parse and display (using jq if available)
echo "$TASKS" | jq -r '.[] | select(.due != null and .due.date == (now | strftime("%Y-%m-%d"))) | "- [\(.content)] (Priority \(.priority))"'
```

**Response Format**:
```
Here are your tasks for today:
- [Buy groceries] (Priority 4)
- [Finish project proposal] (Priority 3)
- [Call dentist] (Priority 1)
```

## Example 2: Add a Task with Due Date

**User Request**: "Add 'Review PR #123' to my Todoist for tomorrow, high priority"

**Implementation**:
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Review PR #123",
    "due_string": "tomorrow",
    "priority": 3,
    "labels": ["work"]
  }'
```

**Response**:
```
✓ Added "Review PR #123" to Todoist
  Due: Tomorrow
  Priority: High
```

## Example 3: Complete a Task

**User Request**: "Mark 'Buy groceries' as complete in Todoist"

**Implementation**:
```bash
# First, find the task ID
TASKS=$(curl -s "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN")

TASK_ID=$(echo "$TASKS" | jq -r '.[] | select(.content == "Buy groceries") | .id')

# Complete the task
curl -s -X POST "https://api.todoist.com/rest/v2/tasks/${TASK_ID}/close" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN"
```

**Response**:
```
✓ Completed "Buy groceries"
```

## Example 4: Create a Project and Add Tasks

**User Request**: "Create a 'Home Renovation' project in Todoist with tasks for painting, flooring, and electrical work"

**Implementation**:
```bash
# Create the project
PROJECT=$(curl -s -X POST "https://api.todoist.com/rest/v2/projects" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Home Renovation",
    "color": "blue"
  }')

PROJECT_ID=$(echo "$PROJECT" | jq -r '.id')

# Add tasks to the project
curl -s -X POST "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"content\": \"Paint living room\",
    \"project_id\": \"$PROJECT_ID\",
    \"priority\": 3
  }"

curl -s -X POST "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"content\": \"Install new flooring\",
    \"project_id\": \"$PROJECT_ID\",
    \"priority\": 3
  }"

curl -s -X POST "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"content\": \"Electrical work inspection\",
    \"project_id\": \"$PROJECT_ID\",
    \"priority\": 4
  }"
```

**Response**:
```
✓ Created project "Home Renovation"
✓ Added 3 tasks:
  - Paint living room (Priority: High)
  - Install new flooring (Priority: High)
  - Electrical work inspection (Priority: Urgent)
```

## Example 5: Update Task Due Date

**User Request**: "Move my 'Call dentist' task to Friday"

**Implementation**:
```bash
# Find the task
TASKS=$(curl -s "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN")

TASK_ID=$(echo "$TASKS" | jq -r '.[] | select(.content == "Call dentist") | .id')

# Update the due date
curl -s -X POST "https://api.todoist.com/rest/v2/tasks/${TASK_ID}" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "due_string": "Friday"
  }'
```

**Response**:
```
✓ Updated "Call dentist" - new due date: Friday
```

## Example 6: Search Tasks by Label

**User Request**: "Show me all my work tasks in Todoist"

**Implementation**:
```bash
# Get all tasks and filter by label
TASKS=$(curl -s "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN")

# Filter for tasks with "work" label
echo "$TASKS" | jq -r '.[] | select(.labels | contains(["work"])) | "- [\(.content)] \(if .due then "Due: \(.due.date)" else "No due date" end)"'
```

**Response**:
```
Your work tasks:
- [Review PR #123] Due: 2026-01-07
- [Finish project proposal] Due: 2026-01-06
- [Team meeting prep] No due date
```

## Example 7: Get Overdue Tasks

**User Request**: "What tasks are overdue in my Todoist?"

**Implementation**:
```bash
# Get all tasks
TASKS=$(curl -s "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN")

# Filter for overdue (due date is before today)
TODAY=$(date +%Y-%m-%d)
echo "$TASKS" | jq --arg today "$TODAY" -r '.[] | select(.due != null and .due.date < $today) | "⚠️  [\(.content)] was due \(.due.date)"'
```

**Response**:
```
You have 2 overdue tasks:
⚠️  [Submit tax documents] was due 2026-01-04
⚠️  [Renew gym membership] was due 2026-01-02
```

## Example 8: Bulk Add Tasks from a List

**User Request**: "Add these to my Todoist: 'Buy milk', 'Walk dog', 'Read for 30 minutes'"

**Implementation**:
```bash
# Add multiple tasks
TASKS=("Buy milk" "Walk dog" "Read for 30 minutes")

for TASK in "${TASKS[@]}"; do
  curl -s -X POST "https://api.todoist.com/rest/v2/tasks" \
    -H "Authorization: Bearer $TODOIST_API_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
      \"content\": \"$TASK\",
      \"priority\": 1
    }" > /dev/null
  echo "✓ Added: $TASK"
done
```

**Response**:
```
✓ Added: Buy milk
✓ Added: Walk dog
✓ Added: Read for 30 minutes

Added 3 tasks to Todoist
```

## Example 9: Show Tasks by Project

**User Request**: "What tasks do I have in my 'Home Renovation' project?"

**Implementation**:
```bash
# Get all projects
PROJECTS=$(curl -s "https://api.todoist.com/rest/v2/projects" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN")

PROJECT_ID=$(echo "$PROJECTS" | jq -r '.[] | select(.name == "Home Renovation") | .id')

# Get tasks for this project
TASKS=$(curl -s "https://api.todoist.com/rest/v2/tasks?project_id=${PROJECT_ID}" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN")

echo "$TASKS" | jq -r '.[] | "- [\(.content)] Priority: \(.priority)"'
```

**Response**:
```
Tasks in "Home Renovation":
- [Paint living room] Priority: 3
- [Install new flooring] Priority: 3
- [Electrical work inspection] Priority: 4
```

## Example 10: Add Task with Description

**User Request**: "Add a task to review the Q4 report with notes about checking the revenue section"

**Implementation**:
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Review Q4 report",
    "description": "Make sure to check the revenue section carefully. Compare with Q3 numbers.",
    "due_string": "next Monday",
    "priority": 3
  }'
```

**Response**:
```
✓ Added "Review Q4 report"
  Due: Next Monday
  Priority: High
  Note: Make sure to check the revenue section carefully. Compare with Q3 numbers.
```

## Tips for JSON Parsing

If `jq` is not available, you can use basic grep/sed:

```bash
# Simple extraction without jq
TASKS=$(curl -s "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN")

# Extract task contents (basic, not robust)
echo "$TASKS" | grep -o '"content":"[^"]*"' | cut -d'"' -f4
```

However, `jq` is highly recommended for robust JSON parsing.
