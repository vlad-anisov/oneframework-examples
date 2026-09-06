"""Экраны Google Tasks, сказанные документом, а не программой."""

from oneframework import *
from oneframework import expr
from .models import Board, Task

class BoardCard(View):
    model = Board
    # Переименование -- работа, а не шаг пути: путь сюда весь состоит из
    # списка, из которого пришли, и он же виден слева.
    crumbs = False

    def _title(board):
        return "Создать список" if board is None else "Переименовать список"

    def ui(self, record):
        return (
            Button("Готово", action=record.save(), place="navbar", enabled=record.name),
            record.name(placeholder="Введите название списка"),
            # Число, которого нет в базе: его считает сама SQLite тем же
            # запросом, которым набирается экран.
            record.progress(),
            # Считает настоящий питон на устройстве -- pymorphy3.
            Button("Привести название к начальной форме",
                   action=Logic("Board.normalize"), visible=record.name),
        )

class TaskRow(View):
    model = Task

    def ui(self, record):
        return Row(
            record.sequence(widget="handle", visible=False),
            record.done(widget="checkbox", icon="check_circle", icon_off="radio_button_unchecked"),
            Col(record.title(widget="title", wrap=True), record.details(widget="subtitle", wrap=True, visible=expr("!record.done"))),
            record.date(widget="title", visible=expr("!record.done")),
            record.finished(widget="title", visible=record.done),
            record.starred(widget="checkbox", icon="star", icon_off="star_border", place="after", visible=expr("!record.done")),
            Button(icon="delete", action=Delete(confirm="Удалить задачу?"), place="after", visible=record.done),
        )

class TaskCard(View):
    model = Task
    _title = ""
    # По той же причине, что у BoardCard выше: глубже двух кадров gtasks не
    # ходит, и цепочка вышла бы парой, где первое звено -- стрелка «назад».
    crumbs = False

    def ui(self, record):
        return (
            record.starred(widget="checkbox", icon="star", icon_off="star_border", place="navbar"),
            Menu(Button("Удалить задачу", action=Delete(confirm="Удалить задачу?"), style="destructive"), place="navbar"),
            Group(
                record.board(widget="inline"),
                record.title(widget="headline", placeholder="Новая задача"),
                record.details(widget="textarea", icon="notes", placeholder="Добавить дополнительную информацию"),
                record.deadline(icon="track_changes", placeholder="Добавить срок"),
                record.date(icon="schedule", placeholder="Добавить дату и время"),
                record.parent(icon="subdirectory_arrow_right", placeholder="Добавить подзадачи"),
                surface="sheet",
            ),
            # Не `Set(record.done, True)`: завершить надо и подзадачи -- на
            # любую глубину, -- и проставить дату выполнения, которую строка
            # списка уже показывает.
            Button("Выполнено", action=Logic("Task.complete"), place="fab"),
        )

class TaskDraftCard(View):
    model = Task
    _title = ""

    details_shown = Boolean()
    date_shown = Boolean()

    def ui(self, record):
        return (
            Group(
                record.title(placeholder="Новая задача"),
                record.details(widget="text", placeholder="Добавить дополнительную информацию",
                               visible=view.details_shown),
                record.date(placeholder="Добавить дату и время", visible=view.date_shown),
                surface="sheet",
            ),
            Row(
                Button(icon="notes", action=Set(view.details_shown, True)),
                Button(icon="schedule", action=Set(view.date_shown, True)),
                record.starred(widget="checkbox", icon="star", icon_off="star_border"),
                Button("Сохранить", action=record.save(), style="plain", place="after", enabled=record.title),
            ),
        )

class Tasks(View):
    _title = "Задачи"

    def ui(self, record):
        return Tabs(
            Tab(
                Icon("star"),
                Button(place="fab", action=Task.create(open=TaskCard, values={"starred": True})),
                List(
                    Task,
                    item=TaskRow,
                    open=TaskCard,
                    label="Помеченная",
                    row_height=72,
                    empty=("Помеченных задач нет", "Отметьте задачу звёздочкой, чтобы она была здесь"),
                    domain=expr("record.starred & !record.done"),
                    search=Search(
                        Sort("Недавно отмеченные", record.updated_at.desc(), default=True),
                        Sort("Дата", record.created_at.desc()),
                        Sort("Крайний срок", record.deadline),
                        Sort("Название", record.title),
                    ),
                ),
            ),
            Repeat(
                Board,
                Tab(
                    "{item.name}",
                    Pill(expr("count(Task, record.board = item.id & !record.done)"), when="closed"),
                    Button(place="fab", action=Task.create(open=TaskDraftCard, draft=True, target="sheet", values={"board": item.id})),
                    List(
                        Task,
                        item=TaskRow,
                        open=TaskCard,
                        row_height=72,
                        label="{item.name}",
                        empty=("Задач нет", "Нажмите +, чтобы добавить задачу"),
                        menu=Menu(
                            Button("Переименовать список", action=Open(BoardCard, item.id)),
                            Button("Удалить список", action=Delete(Board, item.id, confirm="Удалить «{item.name}»?")),
                            Button(
                                "Удалить все выполненные задачи",
                                action=Task.search(
                                    expr("record.board = item.id & record.done"),
                                ).delete(confirm="Удалить все выполненные задачи?"),
                                enabled=expr("exists(Task, record.board = item.id & record.done)"),
                            ),
                        ),
                        domain=expr("record.board = item.id & !record.done"),
                        search=Search(
                            Sort("В моем порядке", record.sequence, default=True),
                            Sort("Дата", record.created_at.desc()),
                            Sort("Крайний срок", record.deadline),
                            Sort("Недавно отмеченные", record.updated_at.desc()),
                            Sort("Название", record.title),
                        ),
                    ),
                    Accordion(
                        List(
                            Task,
                            item=TaskRow,
                            open=TaskCard,
                            domain=expr("record.board = item.id & record.done"),
                            order=[record.finished.desc(), record.updated_at.desc()],
                        ),
                        label="Выполненные",
                        visible=expr("exists(Task, record.board = item.id & record.done)"),
                    ),
                ),
            ),
            Button("+ Новый список", action=Board.create(open=BoardCard, draft=True)),
        )
