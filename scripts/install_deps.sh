#!/bin/bash
# Auto-install dependencies for Todoist skill in venv
# This script is called by SessionStart hook (optional)

set -e

SKILL_DIR=".claude/skills/todoist"
VENV_DIR="$SKILL_DIR/venv"
REQUIREMENTS_FILE="$SKILL_DIR/requirements.txt"

# Only install if requirements.txt exists
if [ ! -f "$REQUIREMENTS_FILE" ]; then
    exit 0
fi

# Create venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment for Todoist skill..."
    python3 -m venv "$VENV_DIR"
fi

# Check if requests is already installed in venv
if "$VENV_DIR/bin/python3" -c "import requests" 2>/dev/null; then
    # Already installed, skip
    exit 0
fi

echo "Installing Todoist skill dependencies in venv..."

# Install requirements in venv (NEVER use --break-system-packages)
"$VENV_DIR/bin/pip" install -q -r "$REQUIREMENTS_FILE"

echo "✓ Todoist skill dependencies installed in venv"
exit 0
