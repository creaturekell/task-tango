import json
from pathlib import Path

import pytest
from task_manager import TaskManager

def make_tm(tmp_path: Path) -> TaskManager:
    """Helper to create a TaskManager with its own isolated tasks.json."""
    tasks_path = tmp_path / "tasks.json"
    return TaskManager(str(tasks_path))


def test_add_task_creates_file_and_stores_task(tmp_path):
    tm = make_tm(tmp_path)

    task = tm.add_task("Buy milk")

    assert task["id"] == 1
    assert task["description"] == "Buy milk"
    assert task["status"] == "todo"
    assert "createdAt" in task
    assert "updatedAt" in task

    tasks_file = tmp_path / "tasks.json"
    assert tasks_file.exists()

    data = json.loads(tasks_file.read_text(encoding="utf-8"))
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["description"] == "Buy milk"

