"""
Unit tests for TodoManager
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from todo_manager import TodoManager


@pytest.fixture
def manager():
    return TodoManager()


# --- add_task ---

def test_add_task_returns_task(manager):
    task = manager.add_task("Buy milk")
    assert task["title"] == "Buy milk"
    assert task["done"] is False
    assert task["priority"] == "medium"
    assert task["id"] == 1

def test_add_task_increments_id(manager):
    t1 = manager.add_task("Task A")
    t2 = manager.add_task("Task B")
    assert t2["id"] == t1["id"] + 1

def test_add_task_custom_priority(manager):
    task = manager.add_task("Urgent thing", priority="high")
    assert task["priority"] == "high"

def test_add_task_empty_title_raises(manager):
    with pytest.raises(ValueError):
        manager.add_task("")

def test_add_task_whitespace_title_raises(manager):
    with pytest.raises(ValueError):
        manager.add_task("   ")

def test_add_task_invalid_priority_raises(manager):
    with pytest.raises(ValueError):
        manager.add_task("Something", priority="critical")


# --- complete_task ---

def test_complete_task_marks_done(manager):
    task = manager.add_task("Do laundry")
    manager.complete_task(task["id"])
    assert manager.tasks[0]["done"] is True

def test_complete_task_returns_updated_task(manager):
    task = manager.add_task("Do laundry")
    result = manager.complete_task(task["id"])
    assert result["done"] is True

def test_complete_nonexistent_task_raises(manager):
    with pytest.raises(KeyError):
        manager.complete_task(999)


# --- delete_task ---

def test_delete_task_removes_it(manager):
    task = manager.add_task("Temporary")
    manager.delete_task(task["id"])
    assert len(manager.tasks) == 0

def test_delete_nonexistent_task_raises(manager):
    with pytest.raises(KeyError):
        manager.delete_task(42)


# --- get_pending ---

def test_get_pending_excludes_done(manager):
    t1 = manager.add_task("Task 1")
    t2 = manager.add_task("Task 2")
    manager.complete_task(t1["id"])
    pending = manager.get_pending()
    assert len(pending) == 1
    assert pending[0]["id"] == t2["id"]

def test_get_pending_empty_when_all_done(manager):
    t = manager.add_task("Only task")
    manager.complete_task(t["id"])
    assert manager.get_pending() == []


# --- get_by_priority ---

def test_get_by_priority_filters_correctly(manager):
    manager.add_task("Low one", priority="low")
    manager.add_task("High one", priority="high")
    manager.add_task("High two", priority="high")
    highs = manager.get_by_priority("high")
    assert len(highs) == 2

def test_get_by_priority_invalid_raises(manager):
    with pytest.raises(ValueError):
        manager.get_by_priority("urgent")


# --- summary ---

def test_summary_counts(manager):
    manager.add_task("A")
    manager.add_task("B")
    t = manager.add_task("C")
    manager.complete_task(t["id"])
    s = manager.summary()
    assert s["total"] == 3
    assert s["done"] == 1
    assert s["pending"] == 2

def test_summary_empty(manager):
    s = manager.summary()
    assert s == {"total": 0, "done": 0, "pending": 0}
