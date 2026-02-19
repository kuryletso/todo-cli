from datetime import date
from todo.models import TaskStorage, Status

def test_add_task(tmp_path):
    task_file = tmp_path / "tasks.json"
    storage = TaskStorage(task_file)

    task = storage.add_task(
        title="Test Task",
        description=None,
        task_date=date(2026,2,22),
    )

    assert task.id == 1
    assert task.title == "Test Task"
    assert task.status == Status.ACTIVE

def test_persistance(tmp_path):
    task_file = tmp_path / "tasks.json"
    storage = TaskStorage(task_file)

    task = storage.add_task(
        title="Persistant",
        description=None,
        task_date=date(2026,2,22),
    )

    storage2 = TaskStorage(task_file)
    assert len(storage2.list_tasks()) == 1
    assert storage2.list_tasks()[0].title == "Persistant"

def test_empty_file(tmp_path):
    task_file = tmp_path / "tasks.json"
    task_file.write_text("")

    storage = TaskStorage(task_file)

    assert storage.list_tasks() == []

def test_mark_done(tmp_path):
    task_file = tmp_path / "tasks.json"
    storage = TaskStorage(task_file)

    task = storage.add_task(
        title="Test Task",
        description=None,
        task_date=date(2026,2,22),
    )

    storage.update_task(task.id, status=Status.DONE)
    updated = storage.get_task(task.id)
    assert updated.status == Status.DONE

def test_delete_task(tmp_path):
    task_file = tmp_path / "tasks.json"
    storage = TaskStorage(task_file)

    task = storage.add_task(
        title="Test Task",
        description=None,
        task_date=date(2026,2,22),
    )

    storage.delete_task(task.id)

    assert storage.get_task(task.id) is None