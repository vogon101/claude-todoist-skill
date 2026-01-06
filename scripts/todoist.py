#!/usr/bin/env python3
"""
Todoist CLI utility for Claude Code skill
Provides simple commands to interact with Todoist API
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests library not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)


def load_env_file():
    """Load environment variables from .env file if it exists"""
    # Start from current directory and walk up to find .env file
    current = Path.cwd().resolve()

    while True:
        env_path = current / ".env"
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if not line or line.startswith("#"):
                        continue
                    # Parse KEY=VALUE
                    if "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip()
                        # Only set if not already in environment
                        if key not in os.environ:
                            os.environ[key] = value
            return True

        # Move up one directory
        parent = current.parent
        if parent == current:  # Reached root
            break
        current = parent

    return False


class TodoistClient:
    """Simple Todoist API client"""

    BASE_URL = "https://api.todoist.com/rest/v2"

    def __init__(self, token: Optional[str] = None):
        # Try to load from .env file if not in environment
        load_env_file()

        self.token = token or os.getenv("TODOIST_API_TOKEN")
        if not self.token:
            print("Error: TODOIST_API_TOKEN not found", file=sys.stderr)
            print("Set it in environment or create a .env file with:", file=sys.stderr)
            print("TODOIST_API_TOKEN=your_token_here", file=sys.stderr)
            sys.exit(1)

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Any:
        """Make API request"""
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported method: {method}")

            if response.status_code == 204:
                return None

            response.raise_for_status()
            return response.json() if response.content else None

        except requests.exceptions.HTTPError as e:
            print(f"API Error ({response.status_code}): {response.text}", file=sys.stderr)
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}", file=sys.stderr)
            sys.exit(1)

    # Tasks
    def get_tasks(self, project_id: Optional[str] = None, filter_str: Optional[str] = None) -> List[Dict]:
        """Get all active tasks"""
        params = []
        if project_id:
            params.append(f"project_id={project_id}")
        if filter_str:
            params.append(f"filter={filter_str}")

        endpoint = "tasks"
        if params:
            endpoint += "?" + "&".join(params)

        return self._request("GET", endpoint) or []

    def get_task(self, task_id: str) -> Dict:
        """Get a single task"""
        return self._request("GET", f"tasks/{task_id}")

    def create_task(self, content: str, **kwargs) -> Dict:
        """Create a new task"""
        data = {"content": content}
        data.update(kwargs)
        return self._request("POST", "tasks", data)

    def update_task(self, task_id: str, **kwargs) -> Dict:
        """Update a task"""
        return self._request("POST", f"tasks/{task_id}", kwargs)

    def complete_task(self, task_id: str) -> None:
        """Complete a task"""
        self._request("POST", f"tasks/{task_id}/close")

    def reopen_task(self, task_id: str) -> None:
        """Reopen a task"""
        self._request("POST", f"tasks/{task_id}/reopen")

    def delete_task(self, task_id: str) -> None:
        """Delete a task"""
        self._request("DELETE", f"tasks/{task_id}")

    # Projects
    def get_projects(self) -> List[Dict]:
        """Get all projects"""
        return self._request("GET", "projects") or []

    def create_project(self, name: str, **kwargs) -> Dict:
        """Create a new project"""
        data = {"name": name}
        data.update(kwargs)
        return self._request("POST", "projects", data)

    def delete_project(self, project_id: str) -> None:
        """Delete a project"""
        self._request("DELETE", f"projects/{project_id}")


def format_task(task: Dict, verbose: bool = False) -> str:
    """Format a task for display"""
    priority_map = {1: "", 2: "🟡", 3: "🟠", 4: "🔴"}
    priority_icon = priority_map.get(task.get("priority", 1), "")

    content = task["content"]
    task_id = task["id"]

    parts = []
    if priority_icon:
        parts.append(priority_icon)
    parts.append(content)

    if task.get("due"):
        due_date = task["due"].get("date", "")
        parts.append(f"(Due: {due_date})")

    if verbose:
        parts.append(f"[ID: {task_id}]")
        if task.get("labels"):
            parts.append(f"Labels: {', '.join(task['labels'])}")

    return " ".join(parts)


def format_project(project: Dict) -> str:
    """Format a project for display"""
    name = project["name"]
    project_id = project["id"]
    favorite = "⭐" if project.get("is_favorite") else ""
    return f"{favorite} {name} [ID: {project_id}]".strip()


def main():
    parser = argparse.ArgumentParser(description="Todoist CLI utility")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Tasks commands
    tasks_parser = subparsers.add_parser("tasks", help="Task operations")
    tasks_subparsers = tasks_parser.add_subparsers(dest="action")

    # tasks list
    list_parser = tasks_subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--filter", help="Filter tasks (e.g., 'today', 'overdue')")
    list_parser.add_argument("--project", help="Project ID")
    list_parser.add_argument("--verbose", "-v", action="store_true", help="Show task IDs and details")

    # tasks get
    get_parser = tasks_subparsers.add_parser("get", help="Get a single task")
    get_parser.add_argument("task_id", help="Task ID")

    # tasks create
    create_parser = tasks_subparsers.add_parser("create", help="Create a task")
    create_parser.add_argument("content", help="Task content/name")
    create_parser.add_argument("--due", help="Due date (e.g., 'tomorrow', 'next Monday')")
    create_parser.add_argument("--priority", type=int, choices=[1, 2, 3, 4], help="Priority (1-4)")
    create_parser.add_argument("--description", help="Task description")
    create_parser.add_argument("--labels", nargs="+", help="Labels")
    create_parser.add_argument("--project", help="Project ID")

    # tasks update
    update_parser = tasks_subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("task_id", help="Task ID")
    update_parser.add_argument("--content", help="New content")
    update_parser.add_argument("--due", help="New due date")
    update_parser.add_argument("--priority", type=int, choices=[1, 2, 3, 4], help="New priority")

    # tasks complete
    complete_parser = tasks_subparsers.add_parser("complete", help="Complete a task")
    complete_parser.add_argument("task_id", help="Task ID")

    # tasks delete
    delete_parser = tasks_subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", help="Task ID")

    # tasks search
    search_parser = tasks_subparsers.add_parser("search", help="Search tasks by content")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--verbose", "-v", action="store_true", help="Show task IDs")

    # Projects commands
    projects_parser = subparsers.add_parser("projects", help="Project operations")
    projects_subparsers = projects_parser.add_subparsers(dest="action")

    # projects list
    projects_subparsers.add_parser("list", help="List all projects")

    # projects create
    proj_create_parser = projects_subparsers.add_parser("create", help="Create a project")
    proj_create_parser.add_argument("name", help="Project name")
    proj_create_parser.add_argument("--color", help="Project color")
    proj_create_parser.add_argument("--favorite", action="store_true", help="Mark as favorite")

    # projects search
    proj_search_parser = projects_subparsers.add_parser("search", help="Search projects by name")
    proj_search_parser.add_argument("query", help="Search query")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = TodoistClient()

    # Handle tasks commands
    if args.command == "tasks":
        if args.action == "list":
            tasks = client.get_tasks(project_id=args.project, filter_str=args.filter)
            if not tasks:
                print("No tasks found")
            else:
                for task in tasks:
                    print(format_task(task, verbose=args.verbose))

        elif args.action == "get":
            task = client.get_task(args.task_id)
            print(json.dumps(task, indent=2))

        elif args.action == "create":
            kwargs = {}
            if args.due:
                kwargs["due_string"] = args.due
            if args.priority:
                kwargs["priority"] = args.priority
            if args.description:
                kwargs["description"] = args.description
            if args.labels:
                kwargs["labels"] = args.labels
            if args.project:
                kwargs["project_id"] = args.project

            task = client.create_task(args.content, **kwargs)
            print(f"✓ Created: {format_task(task, verbose=True)}")

        elif args.action == "update":
            kwargs = {}
            if args.content:
                kwargs["content"] = args.content
            if args.due:
                kwargs["due_string"] = args.due
            if args.priority:
                kwargs["priority"] = args.priority

            task = client.update_task(args.task_id, **kwargs)
            print(f"✓ Updated: {format_task(task, verbose=True)}")

        elif args.action == "complete":
            client.complete_task(args.task_id)
            print(f"✓ Completed task {args.task_id}")

        elif args.action == "delete":
            client.delete_task(args.task_id)
            print(f"✓ Deleted task {args.task_id}")

        elif args.action == "search":
            tasks = client.get_tasks()
            matching = [t for t in tasks if args.query.lower() in t["content"].lower()]
            if not matching:
                print(f"No tasks matching '{args.query}'")
            else:
                for task in matching:
                    print(format_task(task, verbose=args.verbose))

        else:
            tasks_parser.print_help()

    # Handle projects commands
    elif args.command == "projects":
        if args.action == "list":
            projects = client.get_projects()
            if not projects:
                print("No projects found")
            else:
                for project in projects:
                    print(format_project(project))

        elif args.action == "create":
            kwargs = {}
            if args.color:
                kwargs["color"] = args.color
            if args.favorite:
                kwargs["is_favorite"] = True

            project = client.create_project(args.name, **kwargs)
            print(f"✓ Created: {format_project(project)}")

        elif args.action == "search":
            projects = client.get_projects()
            matching = [p for p in projects if args.query.lower() in p["name"].lower()]
            if not matching:
                print(f"No projects matching '{args.query}'")
            else:
                for project in matching:
                    print(format_project(project))

        else:
            projects_parser.print_help()


if __name__ == "__main__":
    main()
