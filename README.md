# Task Tango (Task Manager)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         📋 TASK MANAGEMENT 📋                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

  Panel 1: The Overwhelmed Developer              Panel 2: The Discovery
  ┌─────────────────────┐                        ┌─────────────────────┐
  │                     │                        │                     │
  │    😰  "I have so   │                        │    💡  "Wait! There │
  │        many tasks!  │                        │        must be a    │
  │        Where do I   │                        │        better way!" │
  │        even start?" │                        │                     │
  │                     │                        │                     │
  │   📝 Buy groceries  │                        │   🔍 *searches*     │
  │   📝 Fix bug        │                        │                     │
  │   📝 Write docs     │                        │                     │
  │   📝 Call dentist   │                        │                     │
  │   📝 ... (20 more)  │                        │                     │
  │                     │                        │                     │
  └─────────────────────┘                        └─────────────────────┘
           │                                              │
           │                                              ▼
           │                        Panel 3: The Solution
           │                        ┌─────────────────────┐
           │                        │                     │
           │                        │   🎉  "Task Tracker │
           │                        │        CLI to the    │
           │                        │        rescue!"     │
           │                        │                     │
           │                        │   $ python          │
           │                        │     task_cli.py     │
           │                        │     add "Fix bug"   │
           │                        │                     │
           │                        │   ✅ Task added!    │
           │                        │                     │
           └────────────────────────┘─────────────────────┘
                    │
                    ▼
  Panel 4: The Organized Life
  ┌─────────────────────┐
  │                     │
  │    😊  "Now I can   │
  │        track        │
  │        everything!" │
  │                     │
  │   ✅ todo: 3        │
  │   🔄 in-progress: 1  │
  │   ✨ done: 5        │
  │                     │
  │   Life is good! 🎉  │
  │                     │
  └─────────────────────┘
```

A command-line task management application built with Python. Manage your tasks with a simple CLI interface, tracking status, descriptions, and timestamps.

## Features

- ✅ **Add tasks** - Create new tasks with descriptions
- 📋 **List tasks** - View all tasks or filter by status (todo, in-progress, done)
- ✏️ **Update tasks** - Modify task descriptions
- 🗑️ **Delete tasks** - Remove tasks from your list
- 🔄 **Status management** - Mark tasks as in-progress or done
- 💾 **Persistent storage** - Tasks are saved to JSON file
- 📅 **Timestamps** - Automatic tracking of creation and update times

## Requirements

- Python 3.10 or higher
- pytest (for running tests)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd practice-py-task-tracker
```

2. Install dependencies (using `uv` or `pip`):
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

## Usage

### Basic Commands

**Add a new task:**
```bash
python task_cli.py add "Buy groceries"
```

**List all tasks:**
```bash
python task_cli.py list
```

**List tasks by status:**
```bash
python task_cli.py list todo
python task_cli.py list in-progress
python task_cli.py list done
```

**Update a task:**
```bash
python task_cli.py update <task_id> "New description"
```

**Delete a task:**
```bash
python task_cli.py delete <task_id>
```

**Mark task as in progress:**
```bash
python task_cli.py mark-in-progress <task_id>
```

**Mark task as done:**
```bash
python task_cli.py mark-done <task_id>
```

### Example Workflow

```bash
# Add some tasks
python task_cli.py add "Buy milk"
python task_cli.py add "Write report"
python task_cli.py add "Call dentist"

# List all tasks
python task_cli.py list

# Mark a task as in progress
python task_cli.py mark-in-progress 1

# Update a task
python task_cli.py update 2 "Write quarterly report"

# Mark task as done
python task_cli.py mark-done 1

# List only done tasks
python task_cli.py list done

# Delete a task
python task_cli.py delete 3
```

## Project Structure

```
practice-py-task-tracker/
├── task_cli.py              # CLI interface and command parsing
├── task_manager.py          # Core business logic
├── tasks.json               # Task storage (created automatically)
├── tests/
│   ├── unit/
│   │   └── test_task_manager.py    # Unit tests for TaskManager
│   └── integration/
│       └── test_task_cli.py         # Integration tests for CLI
├── pyproject.toml           # Project configuration
└── README.md                # This file
```

## Testing

Run all tests:
```bash
pytest
```

Run only unit tests:
```bash
pytest tests/unit/
```

Run only integration tests:
```bash
pytest tests/integration/
```

Run with verbose output:
```bash
pytest -v
```

## Design

The project follows a clean architecture pattern with separated concerns:

```
           +----------------------------+
           |         task_cli.py        |
           |  (parses commands, prints) |
           +--------------+-------------+
                          |
                          | uses
                          v
           +----------------------------+
           |      task_manager.py       |
           |   (adds, updates, lists)   |
           |        JSON storage        |
           +----------------------------+
```

This design provides several benefits:

* **Testing** - Business logic can be tested without the command line interface
* **TDD** - Test-Driven Development can be executed more cleanly
* **Simplicity** - The CLI becomes a small wrapper that is simple and readable
* **Extensibility** - Easy to add GUI, API, cronjob, or other interfaces without changing core logic

## Task Data Structure

Each task is stored as a JSON object with the following structure:

```json
{
  "id": 1,
  "description": "Buy groceries",
  "status": "todo",
  "createdAt": "2024-01-15T10:30:00",
  "updatedAt": "2024-01-15T10:30:00"
}
```

### Task Statuses

- `todo` - Task is not yet started
- `in-progress` - Task is currently being worked on
- `done` - Task has been completed

## Development

### Code Style

The project uses:
- Type hints for better code documentation
- Comprehensive docstrings following Google/NumPy style
- Ruff for code formatting (line length: 88, Python 3.10+)

### Adding New Features

When adding new features:

1. Add the business logic to `task_manager.py`
2. Add corresponding CLI command in `task_cli.py`
3. Write unit tests in `tests/unit/test_task_manager.py`
4. Write integration tests in `tests/integration/test_task_cli.py`
5. Update this README if needed

## License

This is a practice project.

## Contributing

This is a practice project. Feel free to fork and experiment!
