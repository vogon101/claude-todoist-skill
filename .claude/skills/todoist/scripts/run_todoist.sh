#!/bin/bash
# Wrapper script to run todoist.py with the skill's venv

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
VENV_PYTHON="$SKILL_DIR/venv/bin/python3"
TODOIST_SCRIPT="$SCRIPT_DIR/todoist.py"

# Check if venv exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "Error: Virtual environment not found at $SKILL_DIR/venv" >&2
    echo "Run setup.sh to create it" >&2
    exit 1
fi

# Run todoist.py with venv python
exec "$VENV_PYTHON" "$TODOIST_SCRIPT" "$@"
