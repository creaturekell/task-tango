#!/usr/bin/env python3
import json
from datetime import datetime
from typing import Dict, List, Any

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

        try:
            with open(self.path,"r") as tf:
                tasks =json.loads(tf)
        except (OSError, json.JSONDecodeError):
            tasks = []

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