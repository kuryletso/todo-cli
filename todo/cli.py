import argparse
from datetime import date, datetime, timedelta
from pathlib import Path
import sys

from todo.models import TaskStorage, Status
from todo.config import Config
from todo.week import render_week
from todo.month import render_month

# UTILITIES

def parse_date(date_str: str) -> date:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD")
        sys.exit(1)

def get_storage_and_config():
    config = Config()
    storage = TaskStorage(config.task_file)
    return storage, config

def handle_add(args):
    storage, _ = get_storage_and_config()
    task_date = parse_date(args.date)

    task = storage.add_task(
        title=args.title,
        description=args.description,
        task_date=task_date,
    )
    print(f"Task created with ID {task.id}")

def handle_edit(args):
    storage, _ = get_storage_and_config()
    task = storage.get_task(args.id)

    if not task:
        print(f"Task {args.id} not found.")
        return
    
    if args.title:
        task.title = args.title
    if args.description is not None:
        task.description = args.description
    if args.date:
        task.task_date = parse_date(args.date)

    storage.save_tasks()
    print(f"Task {task.id} updated")

def handle_delete(args):
    storage, _ = get_storage_and_config()
    if not storage.delete_task(args.id):
        print(f"Task {args.id} not found.")
        return
    
    print(f"Task {args.id} deleted.")

def handle_done(args):
    storage, _ = get_storage_and_config()
    task = storage.get_task(args.id)
    if not task:
        print(f"Task {args.id} not found.")
        return
    task.status = Status.DONE
    storage.save_tasks()
    print(f"Task {args.id} marked as done.")

def handle_cancel(args):
    storage, _ = get_storage_and_config()
    task = storage.get_task(args.id)
    if not task:
        print(f"Task {args.id} not found.")
        return
    task.status = Status.CANCELED
    storage.save_tasks()
    print(f"Task {args.id} canceled.")

def handle_list(args):
    storage, _ = get_storage_and_config()
    tasks = storage.list_tasks()

    if not tasks:
        print("Tasks not found.")
        return

    print(f"{'ID':<4} {'Date':<12} {'Status':<10} Title")
    print("-" * 50)

    for t in tasks:
        print(
            f"{t.id:<4} {t.task_date.isoformat():12}"
            f"{t.status.value:<10} {t.title}"
        )

def handle_week(args):
    storage, config = get_storage_and_config()
    tasks = storage.list_tasks()

    if args.date:
        reference_date = parse_date(args.date)
    else:
        reference_date = date.today()
    
    reference_date += timedelta(days=args.shift * 7)
    result = render_week(
        tasks,
        reference_date=reference_date,
        color_enabled=config.color_enabled,
    )
    print(result)


def shift_month(base_date: date, months: int) -> tuple[int, int]:
    year = base_date.year
    month = base_date.month + months

    while month > 12:
        month -= 12
        year += 1
    
    while months < 1:
        month += 12
        year -= 1

    return year, month

def handle_month(args):
    storage, config = get_storage_and_config()
    tasks = storage.list_tasks()
    
    if  args.date:
        reference_date = parse_date(args.date)
    else:
        reference_date = date.today()

    year, month = shift_month(reference_date, args.shift)

    result = render_month(
        tasks,
        year,
        month,
        color_enabled=config.color_enabled,
    )
    print(result)

# PARSER

def build_parser():
    parser = argparse.ArgumentParser(prog="todo")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ADD
    add = subparsers.add_parser("add")
    add.add_argument("--title", required=True)
    add.add_argument("--date", required=True)
    add.add_argument("--description")
    add.set_defaults(func=handle_add)

    # EDIT
    edit = subparsers.add_parser("edit")
    edit.add_argument("id", type=int)
    edit.add_argument("--title")
    edit.add_argument("--date")
    edit.add_argument("--description")
    edit.set_defaults(func=handle_edit)

    # DELETE
    delete = subparsers.add_parser("delete")
    delete.add_argument("id", type=int)
    delete.set_defaults(func=handle_delete)

    # DONE
    done = subparsers.add_parser("done")
    done.add_argument("id", type=int)
    done.set_defaults(func=handle_done)

    # CANCEL
    cancel = subparsers.add_parser("cancel")
    cancel.add_argument("id", type=int)
    cancel.set_defaults(func=handle_cancel)

    # LIST
    list_cmd = subparsers.add_parser("list")
    list_cmd.set_defaults(func=handle_list)

    # WEEK
    week = subparsers.add_parser("week")
    week.add_argument("shift", nargs="?", type=int, default=0, help="Shift weeks relative to reference date (e.g., -1, +2)")
    week.add_argument("--date", help="Reference date YYYY-MM-DD")
    week.set_defaults(func=handle_week)

    # MONTH
    month = subparsers.add_parser("month")
    month.add_argument("shift", nargs="?", type=int, default=0, help="Shift months relative to reference date (e.g., -1, +2)")
    month.add_argument("--date", help="Reference date YYYY-MM-DD")
    month.set_defaults(func=handle_month)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)



if __name__ == "__main__":
    main()