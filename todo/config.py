from pathlib import Path
import toml
import os

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
TODO_DIR = PROJECT_ROOT / ".todo"
TODO_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_CONFIG_PATH = TODO_DIR / "config.toml"
DEFAULT_TASK_FILE = TODO_DIR / "tasks.json"

class Config:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or DEFAULT_CONFIG_PATH

        self.color_enabled: bool = True
        self.task_file: Path = DEFAULT_TASK_FILE
        
        self._load_from_file()

        self._apply_env_overrides()




    def _load_from_file(self) -> None:
        if not self.path.exists():
            return
        data = toml.loads(self.path.read_text())

        self.color_enabled = data.get("color_enabled", self.color_enabled)

        task_file_str = data.get("task_file")
        if task_file_str:
            self.task_file = Path(task_file_str)

    def _apply_env_overrides(self) -> None:
        env_task_file = os.getenv("TODO_TASK_FILE")
        if env_task_file:
            self.task_file = Path(env_task_file)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "color_enabled": self.color_enabled,
            "task_file": str(self.task_file)
        }

        self.path.write_text(toml.dumps(data))