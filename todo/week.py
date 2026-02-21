from datetime import date, timedelta
from collections.abc import Sequence
from todo.models import Task, Status

RESET = "\033[0m"
BG_COLOR = "\u001b[40m" #"\033[46m"
STATUS_COLORS = {
    Status.ACTIVE: "\033[93m",      # yellow
    Status.DONE: "\033[92m",      # green
    Status.CANCELED: "\033[91m",      # red
}

COLUMN_WIDTH = 22

def _colorize(text: str, status: Status, color_enabled: bool, highlight_today: bool = False) -> str:
    if not color_enabled:
        return text
    color = STATUS_COLORS.get(status, '')
    if highlight_today:
        return f"{BG_COLOR}{color}{text}{RESET}"
    return f"{color}{text}{RESET}"

def _truncate(text: str, width: int) -> str:
    if len(text) <= width:
        return text
    return text[:width-1] + "…"

def _build_border() -> str:
    cell = "+" + "+".join(["-" * COLUMN_WIDTH] * 7) + "+"
    return cell

def render_week(
    tasks: Sequence[Task],
    reference_date: date,
    color_enabled: bool = True,
    show_header:bool = True,
) -> str:
    
    monday = reference_date - timedelta(days=reference_date.weekday())
    sunday = monday + timedelta(days=6)

    # Map tasks for each date
    week_days = [monday + timedelta(days=i) for i in range(7)]
    day_task_map: dict[date, list[Task]] = {d: [] for d in week_days}

    for task in tasks:
        if task.task_date in day_task_map:
            day_task_map[task.task_date].append(task)

    # Build columns
    columns: list[list[str]] = []
    today = date.today()

    for day in week_days:
        header = f"{day:%a %d}"
        column_lines = [_truncate(header,COLUMN_WIDTH)]
        
        highlight_today = (day == today)

        for task in day_task_map[day]:
            raw_text = f"[{task.id}] {task.title}"
            truncated = _truncate(raw_text,COLUMN_WIDTH)
            colored = _colorize(truncated, task.status, color_enabled, highlight_today)
            column_lines.append(colored)

        columns.append(column_lines)
    max_height = max(len(col) for col in columns)

    for col in columns:
        while len(col) < max_height:
            col.append("")
    print(columns)    
    # Render row by row
    lines = []
    border = _build_border()
    if show_header:
        header_line = f"Week {monday:%Y-%m-%d} -> {sunday:%Y-%m-%d}"
        lines.append(header_line)

    lines.append(border)

    for row in range(max_height):
        row_cells = []
        for col in columns:
            cell = col[row]
            row_cells.append(cell.ljust(COLUMN_WIDTH))
        lines.append("|" + "|".join(row_cells) + "|")

        if row == 0:
            lines.append(border)

    lines.append(border)
    
    return "\n".join(lines)