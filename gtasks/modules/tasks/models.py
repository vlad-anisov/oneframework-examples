from oneframework import (
    Boolean, Date, Integer, Many2one, Model, One2many, String, Text, expr,
)


class Board(Model):
    _label = "Список"

    name = String("Название списка", required=True)
    tasks = One2many("Task", "board", "Задачи")

    # Готовность списка -- доля выполненных задач, округлённая к проценту.
    #
    # Строкой, а не обычным питоном: одна запись выражения на все три языка.
    # Пока формулу писали питоном, её приходилось **исполнять** с подставными
    # объектами, чтобы получить дерево, -- и умел это только питон.
    #
    # `via=board` -- считать по объявленной связи, а не по условию: связь уже
    # описана полем `tasks` выше. Ветвление считает SQLite, и невыбранная ветка
    # там не вычисляется -- деления на ноль у пустого списка не происходит.
    #
    # Колонки у этого поля нет, и это главное в нём: готовность меняется от
    # правки *другой* записи, а число, положенное в колонку, об этом не узнает.
    progress = Integer("Готовность, %", compute=expr(
        "if(!count(Task, via=board), 0,"
        " round(count(Task, record.done, via=board) * 100 / count(Task, via=board)))"))


class Task(Model):
    _label = "Задача"

    title = String("Задача", required=True)
    details = Text("Детали")
    date = Date("Дата")
    # Google keeps these apart: the day you mean to do it, and the day it stops
    # being useful. They sort differently and are set from different rows.
    deadline = Date("Крайний срок")
    starred = Boolean("Отмеченная")
    done = Boolean("Выполнено")
    finished = Date("Выполнено")
    board = Many2one(Board, "Список", ondelete="cascade")
    parent = Many2one("Task", "Подзадача к")
    sequence = Integer()
