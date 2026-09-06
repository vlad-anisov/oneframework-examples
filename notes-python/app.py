"""Заметки на питоне: дополнительный интерпретатор на устройстве."""

from oneframework import (
    App, Boolean, Button, Create, Delete, List, Model, Row, Save,
    String, Text, View,
)

class Note(Model):
    _label = "Заметка"
    title = String("Текст", required=True)
    details = Text("Подробности")
    done = Boolean("Выполнено")

    def summary(self):
        from slugify import slugify

        for record in self:
            words = slugify(record.title, separator=" ", allow_unicode=True).split()
            first = " ".join(word.capitalize() for word in words[:5])
            record.details = f"{len(words)} слов: {first}"

class Line(View):
    model = Note

    def ui(self, record):
        return Row(
            record.done(widget="toggle"),
            record.title(widget="title"),
            Button(icon="delete", action=record.delete()),
        )

class Card(View):
    model = Note
    # Карточка -- работа, а не шаг пути: путь сюда весь состоит из списка, из
    # которого пришли, и цепочка из двух звеньев повторила бы стрелку «назад» в
    # том же баре.
    crumbs = False

    def ui(self, record):
        return (
            # Сохранение объявляется явно: карточка открывается черновиком, и
            # до сохранения записи ещё нет -- звать логику не о чем.
            Button("Сохранить", action=record.save(), place="navbar",
                   enabled=record.title),
            record.title(),
            record.details(widget="textarea"),
            record.done(),
            Button("Пересчитать сводку", action=record.summary()),
        )

class Board(View):
    _title = "Заметки"

    def ui(self, record):
        return (
            List(Note, item=Line, open=Card,
                 empty=("Пусто", "Нажмите +, чтобы добавить")),
            Button(place="fab", action=Note.create(open=Card, draft=True)),
        )

app = App(Board, title="Заметки (питон)", color="#4a6b45",
          locale="ru",
          # Колесо едет на устройство вместе с приложением: в webview сети
          # может не быть, и ставить оттуда нечего.
          python_packages=["python-slugify"])
