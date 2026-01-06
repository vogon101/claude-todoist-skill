---
name: todoist
description: Manage tasks in Todoist - create, update, search, and organize tasks and projects. Use when the user wants to manage their Todoist tasks, add todos, check their task list, update task status, or work with Todoist projects. Requires TODOIST_API_TOKEN environment variable.
allowed-tools: Bash(python:*), Read, Grep
---

# Todoist Task Management

This skill enables Claude to interact with Todoist using a simple Python CLI utility. All operations are token-efficient one-line commands.

## Prerequisites

**Required**:
- Python 3.7+
- Todoist API token: https://app.todoist.com/app/settings/integrations/developer
- Environment variable: `export TODOIST_API_TOKEN="your_token_here"`

**Dependencies**:
The skill uses a virtual environment (venv) to isolate dependencies. The `requests` library is installed in the venv at `.claude/skills/todoist/venv/`. NEVER use `--break-system-packages` - always use the venv.

## Quick Start Guide

### List All Tasks

```bash
scripts/run_todoist.sh tasks list
```

With filter:
```bash
scripts/run_todoist.sh tasks list --filter today
scripts/run_todoist.sh tasks list --filter overdue
```

Show task IDs (verbose mode):
```bash
scripts/run_todoist.sh tasks list --verbose
```

### Create a Task

Basic task:
```bash
scripts/run_todoist.sh tasks create "Buy groceries"
```

With due date and priority:
```bash
scripts/run_todoist.sh tasks create "Review PR #123" --due tomorrow --priority 3
```

With full options:
```bash
scripts/run_todoist.sh tasks create "Finish report" \
  --due "next Monday at 14:00" \
  --priority 4 \
  --description "Include Q4 metrics" \
  --labels work urgent
```

### Search Tasks

```bash
scripts/run_todoist.sh tasks search "groceries"
scripts/run_todoist.sh tasks search "PR" --verbose
```

### Complete a Task

```bash
scripts/run_todoist.sh tasks complete TASK_ID
```

### Update a Task

```bash
scripts/run_todoist.sh tasks update TASK_ID --due "next Friday" --priority 4
scripts/run_todoist.sh tasks update TASK_ID --content "New task name"
```

### Delete a Task

```bash
scripts/run_todoist.sh tasks delete TASK_ID
```

### Get Single Task Details

```bash
scripts/run_todoist.sh tasks get TASK_ID
```

## Projects

### List All Projects

```bash
scripts/run_todoist.sh projects list
```

### Search Projects

```bash
scripts/run_todoist.sh projects search "Work"
```

### Create a Project

```bash
scripts/run_todoist.sh projects create "Home Renovation"
scripts/run_todoist.sh projects create "Q1 Goals" --color blue --favorite
```

## Common Workflows

### 1. Show Today's Tasks

```bash
scripts/run_todoist.sh tasks list --filter today
```

### 2. Add Task and Get Confirmation

When creating a task, the script outputs the task with its ID:
```bash
scripts/run_todoist.sh tasks create "Call dentist" --due tomorrow --priority 3
# Output: ✓ Created: 🟠 Call dentist (Due: 2026-01-07) [ID: 2995104339]
```

### 3. Search and Complete

```bash
# Find task
scripts/run_todoist.sh tasks search "groceries" --verbose
# Output shows: 🔴 Buy groceries (Due: 2026-01-06) [ID: 2995104339]

# Complete it
scripts/run_todoist.sh tasks complete 2995104339
```

### 4. Bulk Operations

To add multiple tasks from a list:
```bash
for task in "Buy milk" "Walk dog" "Read for 30min"; do
  scripts/run_todoist.sh tasks create "$task"
done
```

### 5. Get Tasks for a Specific Project

```bash
# Find project ID
scripts/run_todoist.sh projects search "Work"
# Output: ⭐ Work [ID: 2203306141]

# Get project tasks
scripts/run_todoist.sh tasks list --project 2203306141
```

## Priority Levels

The script uses visual indicators:
- Priority 1: No icon (normal)
- Priority 2: 🟡 (medium)
- Priority 3: 🟠 (high)
- Priority 4: 🔴 (urgent)

## Natural Language Due Dates

The `--due` parameter supports Todoist's natural language:
- `today`, `tomorrow`, `yesterday`
- `next Monday`, `next week`, `next month`
- `in 3 days`, `in 2 weeks`
- `tomorrow at 9am`, `next Friday at 14:00`
- `every day`, `every Monday`, `every 3 days`

## Workflow Best Practices

1. **Use verbose mode for IDs**: When you need to update/complete a task, use `--verbose` to see IDs
2. **Search before creating**: Use `tasks search` to avoid duplicates
3. **Use natural language dates**: More intuitive than ISO dates
4. **Set appropriate priorities**: Reserve p4 for truly urgent items
5. **Leverage projects and labels**: Better organization than one long list

## Response Formatting Guidelines

When presenting results to users:
1. **Summarize the action** (e.g., "Added 3 tasks to Todoist")
2. **Show key details** without overwhelming (task name, due date, priority)
3. **Use emoji indicators** that the script provides
4. **Group related items** (e.g., "Your tasks for today:")
5. **Provide task IDs** only when relevant for follow-up actions

Example response format:
```
Your tasks for today:
🔴 Submit tax documents (Due: 2026-01-06)
🟠 Team meeting prep (Due: 2026-01-06)
🟡 Review PR #123 (Due: 2026-01-06)
   Buy milk (Due: 2026-01-06)
```

## Error Handling

The Python script handles errors automatically:
- Missing API token → Clear error message
- Invalid task ID → API error displayed
- Network issues → Request error shown
- Rate limits → HTTP 429 error

No need to manually check response codes - the script exits with status 1 on errors.

## Additional Resources

- **Detailed examples**: See [EXAMPLES.md](EXAMPLES.md) for curl-based examples and advanced workflows
- **Complete API reference**: See [API_REFERENCE.md](API_REFERENCE.md) for all endpoints and parameters

## Script Location

All commands use the wrapper script that activates the venv:
```bash
scripts/run_todoist.sh
```

The wrapper automatically:
- Uses the skill's virtual environment at `.claude/skills/todoist/venv/`
- Loads environment variables from `.env` file if present
- Runs the todoist.py script with proper dependencies

IMPORTANT: Always use `scripts/run_todoist.sh`, never call `python scripts/todoist.py` directly.

## Getting Help

Show all available commands:
```bash
scripts/run_todoist.sh --help
scripts/run_todoist.sh tasks --help
scripts/run_todoist.sh projects --help
```
