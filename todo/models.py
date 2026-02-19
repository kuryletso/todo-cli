from dataclasses import dataclass
from datetime import datetime, date
from enum import Enum
from typing import Optional
from pathlib import Path
import json

class Status(str, Enum):
    ACTIVE = "active"
    DONE = "done"
    CANCELED = "canceled"

@dataclass
class Task:
    id: int
    title: str
    created_at: datetime
    task_date: date
    status: Status = Status.ACTIVE
    description: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "task_date": self.task_date.isoformat(),
            "status": self.status.value
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description"),
            created_at=datetime.fromisoformat(data["created_at"]),
            task_date=datetime.fromisoformat(data["task_date"]),
            status=Status(data.get("status", "active"))
        )

class TaskStorage:
    def __init__(self, filename: Path) -> None:
        self.filename = Path(filename)
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        self.tasks: list[Task] = self.load_tasks()

    def load_tasks(self) -> list[Task]:
        if not self.filename.exists():
            return []
        try:
            with self.filename.open("r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                data = json.loads(content)
                return [Task.from_dict(item) for item in data]
        except json.JSONDecodeError:
            return []
    
    def save_tasks(self) -> None:
        with self.filename.open('w', encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)

    def _next_id(self) -> int:
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1
    
    def add_task(
        self,
        title: str,
        task_date: date,
        description: Optional[str] = None
    ) -> Task:
        task = Task(
        id=self._next_id(),
        title=title,
        task_date=task_date,
        description=description,
        created_at=datetime.now()
        )
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        return next((t for t in self.tasks if t.id == task_id), None)
    
    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        task_date: Optional[date] = None,
        description: Optional[str] = None,
        status: Optional[Status] = None
    ) -> Optional[Task]:
        task = self.get_task(task_id)
        if not task:
            return None
        if title is not None:
            task.title = title
        if task_date is not None:
            task.task_date = task_date
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        self.save_tasks()
        return task
    
    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if not task:
            return False
        self.tasks.remove(task)
        self.save_tasks()
        return True
    
    def list_tasks(self, status: Optional[Status] = None, task_date: Optional[date] = None) -> list[Task]:
        result = self.tasks
        if status:
            result = [t for t in result if t.status == status]
        if task_date:
            result = [t for t in result if t.task_date == task_date]
        return sorted(result, key = lambda t: t.task_date)