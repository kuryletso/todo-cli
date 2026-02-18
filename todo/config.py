from pathlib import Path
import toml

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
TODO_DIR = PROJECT_ROOT / ".todo"
TODO_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_CONFIG_PATH = TODO_DIR / "config.toml"
DEFAULT_TASK_FILE = TODO_DIR / "tasks.json"

class Config:
    def __init__(self, path: Path = None) -> None:
        self.path = path or DEFAULT_CONFIG_PATH
        self.color_enabled = True
        self.task_file = DEFAULT_TASK_FILE
        self.load()


    def load(self):
        if self.path.exists():
            data = toml.loads(self.path.read_text())
            self.color_enabled = data.get("color_enabled", True)
            task_file_str = data.get("task_file")
            if task_file_str:
                self.task_file = Path(task_file_str)
        else:
            self.save()

    def save(self):
        data = {
            "color_enabled": self.color_enabled,
            "task_file": str(self.task_file),
        }

        self.path.write_text(toml.dumps(data))