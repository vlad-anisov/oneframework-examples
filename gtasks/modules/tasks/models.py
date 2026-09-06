from oneframework import (
    Boolean, Date, Integer, Many2one, Model, One2many, String, Text, expr,
)

class Board(Model):
    _label = "Список"

    name = String("Название списка", required=True)
    tasks = One2many("Task", "board", "Задачи")

    progress = Integer("Готовность, %", compute=expr(
        "if(!count(Task, via=board), 0,"
        " round(count(Task, record.done, via=board) * 100 / count(Task, via=board)))"))

class Task(Model):
    _label = "Задача"

    title = String("Задача", required=True)
    details = Text("Детали")
    date = Date("Дата")
    # Google keeps these apart: the day you mean to do it, and the day it stops
    # being useful.
    deadline = Date("Крайний срок")
    starred = Boolean("Отмеченная")
    done = Boolean("Выполнено")
    finished = Date("Выполнено")
    board = Many2one(Board, "Список", ondelete="cascade")
    parent = Many2one("Task", "Подзадача к")
    sequence = Integer()
