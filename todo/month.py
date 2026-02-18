from datetime import date
from calendar import monthrange
from collections.abc import Sequence

from models import Task


WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

RESET = "\033[0m"

# Green heatmap
HEAT_COLORS = [
    "",             # no color
    "\033[92m",     # light green
    "\033[32m",     # green
    "\033[1;32m",   # bright green
]

def _heat_color(count: int) -> str:
    if count == 0:
        return HEAT_COLORS[0]
    if count == 1:
        return HEAT_COLORS[1]
    if 2 <= count <= 3:
        return HEAT_COLORS[2]
    else:
        return HEAT_COLORS[3]

def render_month(
    tasks: Sequence[Task],
    year: int,
    month: int,
    color_enabled: bool = True
) -> str:
    
    first_weekday, days_in_month = monthrange(year,month)
    # Map task count per day
    day_task_cnt = {day: 0 for day in range(1,days_in_month+1)}
    for task in tasks:
        if task.task_date.year == year and task.task_date.month == month:
            day_task_cnt[task.task_date.day] += 1
    
    lines = []
    # Header
    lines.append(f"{date(year,month,1)}:%B %Y")
    lines.append(" ".join(f"{wd:^3}" for wd in WEEKDAYS))

    current_week = ["   "] * first_weekday
    for day in range(1, days_in_month+1):
        cnt = day_task_cnt[day]
        day_str = f"{day:>2}"

        if color_enabled and cnt > 0:
            color = _heat_color(cnt)
            cell = f"{color} {day_str}{RESET}"
        else:
            cell = f"{day_str}"
        
        current_week.append(cell)

        if len(current_week) == 7:
            lines.append(" ".join(current_week))
            current_week = []

    if current_week:
        current_week += ["   "] * (7-len(current_week))
        lines.append(" ".join(current_week))

    return "\n".join(lines)