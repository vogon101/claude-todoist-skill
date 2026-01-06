# Todoist Skill for Claude Code

A Claude skill that enables Claude to manage your Todoist tasks using a simple Python CLI - no MCP server required!

## Why a Skill Instead of MCP?

**Skills are better than MCPs when**:
- You want Claude to automatically know *how* to do something, not just have access to tools
- You're teaching workflows and best practices, not just providing data access
- You want automatic activation based on context
- You want to reduce overhead - skills are loaded only when needed
- You don't need a persistent server running

**This skill uses Python scripts instead of curl commands**, providing:
- **10x token efficiency**: `scripts/run_todoist.sh tasks create "Buy milk"` vs 6 lines of curl
- **Automatic error handling**: No need to parse JSON or check HTTP codes
- **Clean output formatting**: Visual priority indicators (🔴🟠🟡) and human-readable messages
- **Workflow knowledge**: Teaches Claude best practices for task management

## Installation

### 1. Clone or copy this repository

```bash
git clone <your-repo-url>
cd claude-todoist-skill
```

Or copy the `.claude/skills/todoist/` directory to your project.

### 2. Run the setup script

```bash
./setup.sh
```

This will automatically:
- ✅ Check Python installation
- ✅ Create a virtual environment at `.claude/skills/todoist/venv/`
- ✅ Install dependencies in the venv (NEVER breaks system packages)
- ✅ Check for API token
- ✅ Validate everything is working

**IMPORTANT**: This skill uses a proper virtual environment. Never use `--break-system-packages`!

### 3. Set your Todoist API token

Get your token from: https://app.todoist.com/app/settings/integrations/developer

**Option 1: Use .env file (recommended)**
```bash
# Create .env file in project root
echo 'TODOIST_API_TOKEN=your_token_here' > .env
```

The Python script will automatically load from `.env` if it exists.

**Option 2: Environment variable**
```bash
export TODOIST_API_TOKEN="your_token_here"
```

Make it permanent by adding to your `~/.zshrc` or `~/.bashrc`:
```bash
echo 'export TODOIST_API_TOKEN="your_token_here"' >> ~/.zshrc
```

### 4. Restart Claude Code

The skill will be automatically loaded when you restart Claude Code.

### 5. Test the installation

```bash
# Test the CLI directly
.claude/skills/todoist/scripts/run_todoist.sh tasks list
```

## Usage

Once installed, simply ask Claude to manage your Todoist tasks:

### Examples

```bash
# View today's tasks
claude "What's on my Todoist for today?"

# Add a task
claude "Add 'Review PR #123' to my Todoist for tomorrow, high priority"

# Complete a task
claude "Mark 'Buy groceries' as complete in Todoist"

# Create a project
claude "Create a 'Home Renovation' project in Todoist"

# Search tasks
claude "Show me all my work tasks in Todoist"

# Update due dates
claude "Move my 'Call dentist' task to Friday"

# Bulk add tasks
claude "Add these to Todoist: Buy milk, Walk dog, Read for 30 minutes"
```

Claude will automatically use the Todoist skill when you mention Todoist or task management!

## Token Efficiency: Python vs Curl

**Before (curl approach)**:
```bash
# ~400 tokens for this command
curl -s -X POST "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Buy groceries",
    "due_string": "tomorrow",
    "priority": 4
  }'
```

**After (Python script with venv wrapper)**:
```bash
# ~40 tokens for this command
scripts/run_todoist.sh tasks create "Buy groceries" --due tomorrow --priority 4
```

**Result**: 10x token savings per operation!

## Skill Structure

```
.claude/skills/todoist/
├── SKILL.md                 # Main skill definition with quick start
├── requirements.txt         # Python dependencies (just 'requests')
├── venv/                    # Virtual environment (auto-created)
├── scripts/
│   ├── run_todoist.sh      # Wrapper script (use this!)
│   └── todoist.py          # CLI utility
├── EXAMPLES.md             # 10+ concrete usage examples
└── API_REFERENCE.md        # Complete REST API documentation
```

### Progressive Disclosure

The skill uses progressive disclosure to keep context efficient:
- **SKILL.md**: Core instructions and quick reference (loaded first)
- **scripts/todoist.py**: Executable logic (runs without consuming tokens for code)
- **EXAMPLES.md**: Detailed examples (loaded when needed)
- **API_REFERENCE.md**: Full API docs (loaded for complex operations)

## Features

### Task Management
- ✅ Create tasks with natural language dates
- ✅ List and filter tasks (today, overdue, by project)
- ✅ Search tasks by content
- ✅ Update task details (content, due date, priority)
- ✅ Complete and delete tasks
- ✅ Visual priority indicators (🔴🟠🟡)

### Project Management
- ✅ List all projects
- ✅ Search projects by name
- ✅ Create projects with colors and favorites
- ✅ Get tasks for specific projects

### Smart Features
- 🧠 Natural language due dates ("tomorrow", "next Monday", "in 3 days")
- 🎨 Color-coded priorities with emoji indicators
- 🔍 Smart search across tasks and projects
- 📋 Bulk operations for adding multiple tasks
- ✨ Clean, formatted output

## Python CLI Reference

The `todoist.py` script provides a complete CLI interface:

### Tasks

```bash
# List tasks
scripts/run_todoist.sh tasks list
scripts/run_todoist.sh tasks list --filter today
scripts/run_todoist.sh tasks list --verbose  # Show IDs

# Create task
scripts/run_todoist.sh tasks create "Task name" \
  --due "tomorrow" \
  --priority 3 \
  --description "Details" \
  --labels work urgent

# Search tasks
scripts/run_todoist.sh tasks search "groceries" --verbose

# Update task
scripts/run_todoist.sh tasks update TASK_ID --due "next Friday"

# Complete task
scripts/run_todoist.sh tasks complete TASK_ID

# Delete task
scripts/run_todoist.sh tasks delete TASK_ID

# Get task details
scripts/run_todoist.sh tasks get TASK_ID
```

### Projects

```bash
# List projects
scripts/run_todoist.sh projects list

# Search projects
scripts/run_todoist.sh projects search "Work"

# Create project
scripts/run_todoist.sh projects create "Project Name" \
  --color blue \
  --favorite
```

### Get Help

```bash
scripts/run_todoist.sh --help
scripts/run_todoist.sh tasks --help
scripts/run_todoist.sh projects --help
```

## Advantages Over MCP

| Feature | Skill (this) | MCP |
|---------|-------------|-----|
| Server required | ❌ No | ✅ Yes |
| Token efficiency | ✅ High (scripts) | ❌ Lower (tool definitions) |
| Automatic activation | ✅ Yes | ❌ Manual |
| Workflow knowledge | ✅ Built-in | ❌ Just tools |
| Setup complexity | ✅ Simple | ❌ More complex |
| Portability | ✅ Copy directory | ❌ Install server |
| Context overhead | ✅ Low | ❌ Higher |

## Configuration

The skill restricts Claude to safe operations:
```yaml
allowed-tools: Bash(python:*), Read, Grep
```

This ensures Claude can only:
- Run Python scripts (the todoist.py utility)
- Read local files (for reference docs)
- Search for information

## Optional: Auto-Install Dependencies

To automatically install dependencies when starting Claude Code, add a SessionStart hook to `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "scripts/install_deps.sh"
          }
        ]
      }
    ]
  }
}
```

## Development

To modify this skill:

1. **Update Python script**: Edit `.claude/skills/todoist/scripts/todoist.py`
2. **Update instructions**: Edit `.claude/skills/todoist/SKILL.md`
3. **Add examples**: Update `EXAMPLES.md`
4. **Update API reference**: Edit `API_REFERENCE.md`
5. **Restart Claude Code** to reload

## Requirements

- Claude Code CLI
- Python 3.7+
- Todoist account with API token

**Note**: Dependencies are automatically installed in a virtual environment. NEVER use `--break-system-packages`!

## Troubleshooting

### Skill not loading

```bash
# Check skill directory exists
ls -la .claude/skills/todoist/

# Verify SKILL.md frontmatter
head -20 .claude/skills/todoist/SKILL.md

# Restart Claude Code
```

### API token not found

```bash
# Check environment variable
echo $TODOIST_API_TOKEN

# Test the script directly
python .claude/skills/todoist/scripts/todoist.py tasks list
```

### Dependencies not installed

```bash
# Run setup script - it will create venv and install deps
./setup.sh

# Or manually create venv and install
python3 -m venv .claude/skills/todoist/venv
.claude/skills/todoist/venv/bin/pip install -r .claude/skills/todoist/requirements.txt

# Test it works
.claude/skills/todoist/scripts/run_todoist.sh --help
```

### Script errors

```bash
# Make wrapper script executable
chmod +x .claude/skills/todoist/scripts/run_todoist.sh

# Check venv exists
ls -la .claude/skills/todoist/venv/

# Test it
.claude/skills/todoist/scripts/run_todoist.sh --help
```

## Testing

Use the `setup.sh` script to verify everything is configured correctly:

```bash
./setup.sh
```

This checks:
- ✅ TODOIST_API_TOKEN is set and valid
- ✅ Python dependencies installed
- ✅ Skill files present

## Contributing

Enhancements welcome:
- Add more Todoist features (sections, comments, etc.)
- Improve error handling
- Add more examples
- Optimize token usage further

## Resources

- [Todoist REST API Documentation](https://developer.todoist.com/rest/v2/)
- [Claude Code Skills Guide](https://code.claude.com/docs/en/skills.md)
- [Official Todoist MCP](https://github.com/Doist/todoist-ai) (for comparison)

## License

MIT License - feel free to use and modify!

---

**Built with ❤️ for Claude Code**
