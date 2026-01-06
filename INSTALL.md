# Quick Installation Guide

## 1. Run Setup

```bash
./setup.sh
```

This automatically:
- ✅ Creates a virtual environment at `.claude/skills/todoist/venv/`
- ✅ Installs dependencies (requests library)
- ✅ Checks for your API token
- ✅ Validates everything works

## 2. Your API token is already set!

Your `.env` file contains:
```
TODOIST_API_TOKEN=4f32432f58a650d8ab12a0e61ce191024bfb3c83
```

The Python script automatically loads this file.

## 3. Test it works

```bash
.claude/skills/todoist/scripts/run_todoist.sh tasks list --filter today
```

## 4. Restart Claude Code

Exit and restart Claude Code to load the skill.

## 5. Use it!

```bash
claude "What's on my Todoist for today?"
claude "Add 'Buy milk' to my Todoist for tomorrow"
claude "Complete the 'Fix Inbox' task in Todoist"
```

## Important Notes

✅ **Uses proper virtual environment** - All dependencies isolated
✅ **Loads .env automatically** - No need to export tokens
✅ **NEVER breaks system packages** - Safe and clean
✅ **10x token efficiency** - Short commands vs long curl

## Wrapper Script

Always use the wrapper script:
```bash
scripts/run_todoist.sh
```

**NOT** `python scripts/todoist.py` directly!

The wrapper:
- Activates the venv automatically
- Loads .env file
- Handles all paths correctly

## If Something Goes Wrong

Re-run setup:
```bash
./setup.sh
```

It will fix any issues automatically.
