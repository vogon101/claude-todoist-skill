#!/bin/bash

# Todoist Skill Setup and Validation Script

echo "🎯 Todoist Skill Setup"
echo "======================"
echo ""

# Check Python
echo "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo "✅ Python installed: $PYTHON_VERSION"
else
    echo "❌ Python 3 not found"
    echo "Install Python: https://www.python.org/downloads/"
    exit 1
fi

echo ""

# Check/create virtual environment
echo "Checking virtual environment..."
VENV_DIR=".claude/skills/todoist/venv"

if [ -d "$VENV_DIR" ]; then
    echo "✅ Virtual environment found"
else
    echo "⚠️  Virtual environment not found"
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    if [ -d "$VENV_DIR" ]; then
        echo "✅ Virtual environment created"
    else
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi

# Check if requests library is installed in venv
echo "Checking Python dependencies in venv..."
if "$VENV_DIR/bin/python3" -c "import requests" 2>/dev/null; then
    echo "✅ Dependencies installed in venv"
else
    echo "⚠️  Dependencies not installed in venv"
    echo "Installing dependencies..."
    if [ -f ".claude/skills/todoist/requirements.txt" ]; then
        "$VENV_DIR/bin/pip" install -q -r .claude/skills/todoist/requirements.txt
        if "$VENV_DIR/bin/python3" -c "import requests" 2>/dev/null; then
            echo "✅ Dependencies installed successfully"
        else
            echo "❌ Failed to install dependencies"
            exit 1
        fi
    fi
fi

echo ""

# Check if TODOIST_API_TOKEN is set
echo "Checking API token..."

# Check for .env file
if [ -f ".env" ]; then
    echo "✅ .env file found"
    # Try to read token from .env
    if grep -q "TODOIST_API_TOKEN" .env; then
        echo "✅ TODOIST_API_TOKEN found in .env file"
        # Export it for testing
        export $(grep "^TODOIST_API_TOKEN=" .env | xargs)
    fi
fi

if [ -z "$TODOIST_API_TOKEN" ]; then
    echo "⚠️  TODOIST_API_TOKEN not found"
    echo ""
    echo "Option 1 - Create a .env file (recommended):"
    echo "   Create a .env file in the project root with:"
    echo "   TODOIST_API_TOKEN=your_token_here"
    echo ""
    echo "Option 2 - Set environment variable:"
    echo "   export TODOIST_API_TOKEN='your_token_here'"
    echo "   Add to ~/.zshrc or ~/.bashrc to make permanent"
    echo ""
    echo "Get your token from: https://app.todoist.com/app/settings/integrations/developer"
    echo ""
else
    echo "✅ TODOIST_API_TOKEN is set"

    # Test the token using wrapper script
    echo "Testing API token..."
    if [ -f ".claude/skills/todoist/scripts/run_todoist.sh" ]; then
        TEST_OUTPUT=$(.claude/skills/todoist/scripts/run_todoist.sh projects list 2>&1)
        TEST_EXIT=$?

        if [ $TEST_EXIT -eq 0 ]; then
            echo "✅ API token is valid!"
        else
            echo "❌ API token test failed"
            echo "Error: $TEST_OUTPUT"
            echo "Please check your token at https://app.todoist.com/app/settings/integrations/developer"
        fi
    else
        # Fallback to curl test
        RESPONSE=$(curl -s -w "%{http_code}" -o /dev/null "https://api.todoist.com/rest/v2/projects" \
            -H "Authorization: Bearer $TODOIST_API_TOKEN")

        if [ "$RESPONSE" = "200" ]; then
            echo "✅ API token is valid!"
        else
            echo "❌ API token test failed (HTTP $RESPONSE)"
            echo "Please check your token at https://app.todoist.com/app/settings/integrations/developer"
        fi
    fi
fi

echo ""

# Check skill files
echo "Checking skill files..."
SKILL_FILES_OK=true

if [ -f ".claude/skills/todoist/SKILL.md" ]; then
    echo "✅ SKILL.md found"
else
    echo "❌ SKILL.md not found"
    SKILL_FILES_OK=false
fi

if [ -f ".claude/skills/todoist/scripts/todoist.py" ]; then
    echo "✅ todoist.py script found"
    # Make sure it's executable
    chmod +x .claude/skills/todoist/scripts/todoist.py
else
    echo "❌ todoist.py script not found"
    SKILL_FILES_OK=false
fi

if [ -f ".claude/skills/todoist/requirements.txt" ]; then
    echo "✅ requirements.txt found"
else
    echo "⚠️  requirements.txt not found"
fi

if [ -f ".claude/skills/todoist/EXAMPLES.md" ]; then
    echo "✅ EXAMPLES.md found"
else
    echo "⚠️  EXAMPLES.md not found (optional)"
fi

if [ -f ".claude/skills/todoist/API_REFERENCE.md" ]; then
    echo "✅ API_REFERENCE.md found"
else
    echo "⚠️  API_REFERENCE.md not found (optional)"
fi

echo ""

# Test the wrapper script
if [ -f ".claude/skills/todoist/scripts/run_todoist.sh" ] && [ ! -z "$TODOIST_API_TOKEN" ]; then
    echo "Testing todoist CLI..."
    .claude/skills/todoist/scripts/run_todoist.sh --help > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "✅ Todoist CLI is working"
    else
        echo "❌ CLI test failed"
    fi
fi

echo ""
echo "📚 Next Steps:"
if [ $SKILL_FILES_OK = true ] && [ ! -z "$TODOIST_API_TOKEN" ]; then
    echo "✅ All checks passed!"
    echo ""
    echo "1. Restart Claude Code to load the skill"
    echo "2. Try: claude 'What skills are available?'"
    echo "3. Test: claude 'Show me my Todoist tasks for today'"
    echo ""
    echo "Or test the CLI directly:"
    echo "  .claude/skills/todoist/scripts/run_todoist.sh tasks list"
else
    echo "⚠️  Please fix the issues above before using the skill"
fi

echo ""
