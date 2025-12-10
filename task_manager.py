#!/usr/bin/env python3
import json
from datetime import datetime
from typing import Dict, List, Optional, Any

class TaskManager:
    """ Core task management logic """

    STATUS_TODO = "todo"
    STATUS_IN_PROGRESS = "in-progress"
    STATUS_DONE = "done"

    VALID_STATUSES = {STATUS_TODO, STATUS_IN_PROGRESS, STATUS_DONE}

    def __init__(self, path: str = "tasks.json") -> None:
        self.path = path

    # -----------------------------------------
    #  Internal Methods
    # -----------------------------------------

    def _next_id(self, tasks: List[Dict[str, Any]]) -> int:
        """ Get the next available id """
        return 1 if not tasks else max(t["id"] for t in tasks) + 1

    def _get_tasks(self) -> List[Dict[str, Any]]:
        """ Get all tasks from file """
        try:
            with open(self.path,"r",encoding="utf-8") as tf:
                return json.load(tf)
        except FileNotFoundError:
            return [] # File doesn't exist yet
        except json.JSONDecodeError:
            return [] # File is empty or invalid JSON
        except OSError as e:
            raise ValueError(f"Failed to read tasks from {self.path}: {e}")

    def _get_timestamp(self) -> str:
        """ Get the current timestamp """
        return datetime.now().isoformat(timespec="seconds")

    def _find_task(self, tasks: List[Dict[str, Any]], task_id: int) -> Optional[Dict[str, Any]]:
        """ Find a task by id """
        for t in tasks:
            if t["id"] == task_id:
                return t
        return None

    def _save_tasks(self, tasks: List[Dict[str, Any]]) -> None:
        """ Save tasks to file """
        try:
            with open(self.path,"w", encoding="utf-8") as tf:
                json.dump(tasks, tf, indent=2)
        except (OSError, json.JSONDecodeError):
            raise ValueError(f"Failed to save tasks to {self.path}")

    def _update_task_status(self, task_id: int, new_status: str) -> Dict[str, Any]:
        """ Update the status of a task """
        tasks = self._get_tasks()
        task = self._find_task(tasks, task_id)
        if task is None:
            raise ValueError(f"Task with id {task_id} not found.")
        
        task["status"] = new_status
        task["updatedAt"] = self._get_timestamp()
        self._save_tasks(tasks)
        return task

    # -----------------------------------------
    #  Public Methods
    # -----------------------------------------
    
    def add_task(self, description: str) -> Dict[str, Any]:
        """ Add a new task 

        1. get list of tasks from file
        2. get next available id
        3. get timestamp
        4. structure new task object
        5. append task to list
        6. save updated task list 
        7. return new task
        
        """

        if not description or not description.strip():
            raise ValueError("Task Description cannot be empty.")

        tasks = self._get_tasks()
        new_id = self._next_id(tasks)  # get next available id
        timestamp = self._get_timestamp()
        
        task = {
            "id": new_id,
            "description": description,
            "status": self.STATUS_TODO,
            "createdAt": timestamp,
            "updatedAt": timestamp,
        }

        tasks.append(task)
        self._save_tasks(tasks)

        return task

    def list_tasks(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """ List all tasks """
        
        tasks = self._get_tasks()
        if status is None:
            return tasks
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status filter: {status}")
        
        return [t for t in tasks if t.get("status") == status]  # filter tasks by status

    def update_task(self, id: int, updated_description: str) -> Dict[str, Any]:
        """ Update an existing task """

        if not updated_description or not updated_description.strip():
            raise ValueError("Updated Task Description cannot be empty.")

        tasks = self._get_tasks()
        task = self._find_task(tasks, id)
        if task is None:
            raise ValueError(f"Task with id {id} not found.")
        
        task["description"] = updated_description
        task["updatedAt"] = self._get_timestamp()

        self._save_tasks(tasks)
        return task

    def delete_task(self, id: int) -> Dict[str, Any]:
        """ Delete an existing task """

        tasks = self._get_tasks()
        task = self._find_task(tasks, id)
        if task is None:
            raise ValueError(f"Task with id {id} not found.")
        
        tasks.remove(task)
        self._save_tasks(tasks)
        return task

    def mark_in_progress(self, id: int) -> Dict[str, Any]:
        """ Mark a task as in progress """
        return self._update_task_status(id, self.STATUS_IN_PROGRESS)


    def mark_done(self, id: int) -> Dict[str, Any]:
        """ Mark a task as done """
        return self._update_task_status(id, self.STATUS_DONE)