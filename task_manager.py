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
        timestamp = datetime.now().isoformat(timespec="seconds") 
        
        task = {
            "id": new_id,
            "description": description,
            "status": "todo",
            "createdAt": timestamp,
            "updatedAt": timestamp,
        }

        tasks.append(task)

        try:
            with open(self.path,"w") as tf:
                json.dump(tasks, tf, indent=2)
        except (OSError, json.JSONDecodeError):
            raise ValueError(f"Failed to save tasks to {self.path}")

        return task

    def list_tasks(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """ List all tasks """
        
        tasks = self.get_tasks()
        if status is None:
            return tasks
        if status not in {"todo", "in-progress","done"}:
            raise ValueError(f"Invalid status filter: {status}")
        
        return [t for t in tasks if t.get("status") == status]  # filter tasks by status
