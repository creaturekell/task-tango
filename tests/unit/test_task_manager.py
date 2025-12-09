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


def test_list_all_tasks(tmp_path):
    tm = make_tm(tmp_path)

    t1 = tm.add_task("Buy milk")
    t2 = tm.add_task("Buy eggs")
    t3 = tm.add_task("Buy bread")

    all_tasks = tm.list_tasks()

    assert isinstance(all_tasks, list)
    assert len(all_tasks) == 3
    assert {t["id"] for t in all_tasks} == {t1["id"], t2["id"], t3["id"]}
    assert all_tasks[0]["description"] == "Buy milk"
    assert all_tasks[1]["description"] == "Buy eggs"
    assert all_tasks[2]["description"] == "Buy bread"
