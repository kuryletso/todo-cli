from datetime import date, datetime, timedelta
from calendar import monthrange
import pytest
from todo.week import render_week
from todo.month import render_month
from todo.models import Task, Status
import re


def make_task(title: str, day: date):
    return Task(
        id=1,
        title=title,
        description=None,
        task_date=day,
        status=Status.ACTIVE,
        created_at=datetime.today(),
    )

def test_render_week():
    today = date(2026, 2, 18)
    tasks = [
        make_task("Mon task", today - timedelta(days=2)),
        make_task("Wed task", today),
        make_task("Fri task", today + timedelta(days=2)),
    ]

    week_str = render_week(tasks, reference_date=today)

    assert "Mon task" in week_str
    assert "Wed task" in week_str
    assert "Fri task" in week_str

    assert "\033[" in week_str

def test_render_month_density():
    tasks = []
    today = date(2026,2,21)
    for i in range(1,6):
        tasks.append(make_task(f"Task {i}", today + timedelta(days=i-1)))
    tasks.append(make_task(f"Extra task 6", today - timedelta(days=5)))
    tasks.append(make_task(f"Extra task 6b", today - timedelta(days=5)))

    month_str = render_month(tasks, today.year, today.month, color_enabled=True)
    ANSI_re = re.compile(r"\x1b\[[0-9;]*m")
    no_ANSI = ANSI_re.sub("", month_str)

    for i in range(1, monthrange(today.year, today.month)[1]+1):
        assert str(i) in no_ANSI.split()

    assert "\033[" in month_str