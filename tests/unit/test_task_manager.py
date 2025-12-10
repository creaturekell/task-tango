import json
from pathlib import Path
from time import sleep

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


def test_list_tasks_filtered_by_status(tmp_path):
    tm = make_tm(tmp_path)

    t1 = tm.add_task("Buy milk")
    t2 = tm.add_task("Buy eggs")
    t3 = tm.add_task("Buy bread")

    # for now, only todo is supported, once update_task is implemented, we can test other statuses
    todo_tasks = tm.list_tasks("todo")
    wip_tasks = tm.list_tasks("in-progress") 
    done_tasks = tm.list_tasks("done")
    
    assert isinstance(todo_tasks, list)
    assert len(todo_tasks) == 3
    assert {t["id"] for t in todo_tasks} == {t1["id"], t2["id"], t3["id"]}

def test_update_task_changes_description_and_updated_at(tmp_path):
    tm = make_tm(tmp_path)

    original = tm.add_task("Old description")
    sleep(3)
    updated = tm.update_task(original["id"], "New description")

    assert updated["id"] == original["id"]
    assert updated["description"] == "New description"
    assert updated["updatedAt"] != original["updatedAt"]

    # persisted
    tasks = tm._get_tasks()
    assert tasks[0]["description"] == "New description"

def test_delete_task_removes_task_from_list(tmp_path):
    tm = make_tm(tmp_path)

    t1 = tm.add_task("Buy milk")
    t2 = tm.add_task("Buy eggs")
    t3 = tm.add_task("Buy bread")

    tm.delete_task(t2["id"])

    tasks = tm.list_tasks()
    assert len(tasks) == 2
    assert {t["id"] for t in tasks} == {t1["id"], t3["id"]}

def test_mark_in_progress_changes_status_and_updated_at(tmp_path):
    tm = make_tm(tmp_path)

    original = tm.add_task("Buy milk")
    sleep(3)
    updated = tm.mark_in_progress(original["id"])

    assert updated["id"] == original["id"]
    assert updated["status"] == "in-progress"
    assert updated["updatedAt"] != original["updatedAt"]

    # persisted
    tasks = tm._get_tasks()
    assert tasks[0]["status"] == "in-progress"

def test_mark_done_changes_status_and_updated_at(tmp_path):
    tm = make_tm(tmp_path)

    original = tm.add_task("Buy milk")
    sleep(3)
    updated = tm.mark_done(original["id"])

    assert updated["id"] == original["id"]
    assert updated["status"] == "done"
    assert updated["updatedAt"] != original["updatedAt"]
    
    # persisted
    tasks = tm._get_tasks()
    assert tasks[0]["status"] == "done"
    assert tasks[0]["updatedAt"] != original["updatedAt"]