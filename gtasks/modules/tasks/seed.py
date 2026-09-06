"""First-run content, so the app opens on something rather than nothing."""

from .models import Board, Task

TERMINAL = [
    "Ооо",
    "Сделать коммит, который добавляею новый url и тему только для терминала",
    "Доделать 5940 и отправить на код ревью",
    "Создать задачу по удалению модуля website и отправить её на код ревью",
    "Создать задачу по типу поля и отправить её на код ревью",
    "Создать задачау на 1124 и отрпавить на код ревью",
]

#: Invented: the screenshots show only that this list holds eight.
GEORGIA = [
    "Продлить страховку на машину",
    "Купить билеты на обратный рейс",
    "Забрать документы из консульства",
    "Найти жильё на второй месяц",
    "Открыть счёт в местном банке",
    "Оформить местную симку",
    "Записаться на курсы языка",
    "Перевести права",
]

#: Invented: the screenshots show only that this list holds ten.
MOVING = [
    "Собрать книги в коробки",
    "Заказать грузовик на субботу",
    "Разобрать шкаф в спальне",
    "Сдать ключи от старой квартиры",
    "Переоформить интернет на новый адрес",
    "Отдать лишнюю мебель",
    "Купить плёнку и скотч",
    "Договориться с грузчиками",
    "Снять показания счётчиков",
    "Забрать залог у арендодателя",
]

def seed(db):
    boards = {
        name: db.create(Board, {"name": name})
        for name in ("Терминал", "Грузия", "Переезд")
    }

    sequence = 0
    for name, titles in (("Терминал", TERMINAL), ("Грузия", GEORGIA),
                         ("Переезд", MOVING)):
        for i, title in enumerate(titles):
            sequence += 10
            db.create(Task, {
                "title": title,
                "starred": name == "Терминал" and i == 0,
                "board": boards[name],
                "sequence": sequence,
            })
