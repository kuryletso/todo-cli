import sys
from datetime import date
from pathlib import Path

import pytest

from todo.cli import main
from todo.models import TaskStorage

def run_cli(monkeypatch,args):
    monkeypatch.setattr(sys, "argv", ["todo"] + args)
    main()

def test_cli_add_creates_task(tmp_path, monkeypatch):
    task_file = tmp_path / "tasks.json"
    monkeypatch.setenv("TODO_TASK_FILE", str(task_file))

    run_cli(
        monkeypatch,
        ["add", "--title", "CLI Task", "--date", "2022-02-22"],
    )

    storage = TaskStorage(task_file)
    assert len(storage.list_tasks()) == 1
    assert storage.list_tasks()[0].title == "CLI Task"

def test_cli_add_print_confirmation(tmp_path, monkeypatch, capsys):
    task_file = tmp_path / "tasks.json"
    monkeypatch.setenv("TODO_TASK_FILE", str(task_file))

    run_cli(
        monkeypatch,
        ["add", "--title", "CLI Task", "--date", "2022-02-22"],
    )

    captured = capsys.readouterr()
    assert "created" in captured.out.lower()

def test_cli_list_outputs_tasks(tmp_path, monkeypatch, capsys):
    task_file = tmp_path / "tasks.json"
    monkeypatch.setenv("TODO_TASK_FILE", str(task_file))

    run_cli(
        monkeypatch,
        ["add", "--title", "CLI Task", "--date", "2022-02-22"],
    )

    run_cli(monkeypatch, ["list"])

    captured = capsys.readouterr()
    assert "CLI Task" in captured.out