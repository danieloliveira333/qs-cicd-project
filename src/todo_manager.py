"""
Todo Manager - Simple task management module
Used as base project for CI/CD Quality Gates study (QS 2025/26)
"""

class TodoManager:
    def __init__(self):
        self.tasks = []
        self._next_id = 1

    def add_task(self, title: str, priority: str = "medium") -> dict:
        """Add a new task. Priority: low, medium, high."""
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty.")
        if priority not in ("low", "medium", "high"):
            raise ValueError(f"Invalid priority '{priority}'. Must be low, medium or high.")
        task = {
            "id": self._next_id,
            "title": title.strip(),
            "priority": priority,
            "done": False,
        }
        self.tasks.append(task)
        self._next_id += 1
        return task

    def complete_task(self, task_id: int) -> dict:
        """Mark a task as done."""
        task = self._get_task(task_id)
        task["done"] = True
        return task

    def delete_task(self, task_id: int) -> dict:
        """Delete a task by ID."""
        task = self._get_task(task_id)
        self.tasks.remove(task)
        return task

    def get_pending(self) -> list:
        """Return all tasks not yet completed."""
        return [t for t in self.tasks if not t["done"]]

    def get_by_priority(self, priority: str) -> list:
        """Return tasks filtered by priority."""
        if priority not in ("low", "medium", "high"):
            raise ValueError(f"Invalid priority '{priority}'.")
        return [t for t in self.tasks if t["priority"] == priority]

    def summary(self) -> dict:
        """Return a summary of tasks."""
        return {
            "total": len(self.tasks),
            "done": sum(1 for t in self.tasks if t["done"]),
            "pending": sum(1 for t in self.tasks if not t["done"]),
        }
    
    def count_by_priority(self) -> dict:
        """Return count of tasks grouped by priority."""
        result = {"low": 0, "medium": 0, "high": 0}
        for task in self.tasks:
            priority = task.get("priority", "medium")
            if priority in result:
                result[priority] += 1
        return result
        
    def _get_task(self, task_id: int) -> dict:
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        raise KeyError(f"Task with id {task_id} not found.")
