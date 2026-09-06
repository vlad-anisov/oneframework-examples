"""Google Tasks: lists as tabs across the top, their tasks below."""

from oneframework import Screen

from .models import Board, Task
from .views import BoardCard, TaskCard, TaskDraftCard, TaskRow, Tasks

__all__ = ["Board", "Task", "BoardCard", "TaskCard", "TaskDraftCard", "TaskRow",
           "Tasks"]

SCREEN = Screen(Tasks, label="Задачи")

#: Бизнес-логика этого модуля -- скомпилированный WASM и то, что он умеет.
LOGIC = [{
    "actions": [
        {
            "name": "Task.complete", "model": "Task",
            "label": "Выполнить с подзадачами",
            "args": [{"name": "ids", "type": "ids"}],
            "returns": [{"name": "changed", "type": "integer"}],
            # Правило даёт множество: сама задача и её невыполненные потомки на
            # любую глубину.
            "rule": {
                "name": "subtree", "table": "task", "via": "parent_id",
                "include_seed": True, "seed": {"param": "root"},
                "where": {"op": "not", "args": [{"field": "done"}]},
            },
            "write": {
                "table": "task", "source": "subtree",
                # Дата приходит **параметром вызова**: `datetime('now')` внутри
                # запроса SQLite сама объявляет недетерминированной, и два
                # устройства разошлись бы, посчитав в разные секунды.
                "set": {"done": {"const": True}, "finished": {"param": "today"}},
            },
        },
        {
            "name": "Board.normalize", "model": "Board",
            "label": "Привести название к начальной форме",
            "args": [{"name": "ids", "type": "ids"}],
            "returns": [{"name": "records", "type": "json"}],
            "python": {
                "entry": "нормализовать",
                "writes": ["name"],
                "source": (
                    "import pymorphy3\n"
                    "\n"
                    "morph = pymorphy3.MorphAnalyzer()\n"
                    "\n"
                    "\n"
                    "def нормализовать(кадр):\n"
                    "    готово = []\n"
                    "    for запись in кадр.get('records', []):\n"
                    "        слова = (запись.get('name') or '').split()\n"
                    "        начальные = ' '.join(\n"
                    "            morph.parse(с)[0].normal_form for с in слова)\n"
                    "        готово.append({'id': запись['id'], 'name': начальные})\n"
                    "    return {'records': готово}\n"
                ),
            },
        },
    ],
}]
