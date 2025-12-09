#!/usr/bin/env python3
import json
from datetime import datetime
from typing import Dict, List, Optional, Any

class TaskManager:
    """ Core task management logic """

    def __init__(self, path: str = "tasks.json") -> None:
        self.path = path

    # -----------------------------------------
    #  Internal Methods
    # -----------------------------------------

    def _next_id(self, tasks: List[Dict[str, Any]]) -> int:
        """ Get the next available id """
        return 1 if not tasks else max(t["id"] for t in tasks) + 1

    def get_tasks(self) -> List[Dict[str, Any]]:
        """ Get all tasks from file """
        try:
            with open(self.path,"r",encoding="utf-8") as tf:
                return json.load(tf)
        except (OSError, json.JSONDecodeError):
            return []
    
    def _get_timestamp(self) -> str:
        """ Get the current timestamp """
        return datetime.now().isoformat(timespec="seconds")

    def _find_task(self, tasks: List[Dict[str, Any]], task_id: int) -> Optional[Dict[str, Any]]:
        """ Find a task by id """
        for t in tasks:
            if t.get("id") == task_id:
                return t
        return None

    def save_tasks(self, tasks: List[Dict[str, Any]]) -> None:
        """ Save tasks to file """
        try:
            with open(self.path,"w", encoding="utf-8") as tf:
                json.dump(tasks, tf, indent=2)
        except (OSError, json.JSONDecodeError):
            raise ValueError(f"Failed to save tasks to {self.path}")

    # -----------------------------------------
    #  Public Methods
    # -----------------------------------------
    
    def add_task(self, description) -> Dict[str, Any]:
        """ Add a new task 

        1. get list of tasks from file
        2. get next available id
        3. get timestamp
        4. structure new task object
        5. append task to list
        6. save updated task list 
        7. return new task
        
        """

        tasks = self.get_tasks()
        new_id = self._next_id(tasks)  # get next available id
        timestamp = self._get_timestamp()
        
        task = {
            "id": new_id,
            "description": description,
            "status": "todo",
            "createdAt": timestamp,
            "updatedAt": timestamp,
        }

        tasks.append(task)
        self.save_tasks(tasks)

        return task

    def list_tasks(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """ List all tasks """
        
        tasks = self.get_tasks()
        if status is None:
            return tasks
        if status not in {"todo", "in-progress","done"}:
            raise ValueError(f"Invalid status filter: {status}")
        
        return [t for t in tasks if t.get("status") == status]  # filter tasks by status

    def update_task(self, id: int, updated_description: [str]) -> Dict[str, Any]:
        """ Update an existing task """

        tasks = self.get_tasks()
        task = self._find_task(tasks, id)
        if task is None:
            raise ValueError(f"Task with id {id} not found.")
        
        task["description"] = updated_description
        task["updatedAt"] = self._get_timestamp()

        self.save_tasks(tasks)
        return task