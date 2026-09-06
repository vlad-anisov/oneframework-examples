"""500 records: paging, infinite scroll and virtual list."""

from oneframework import Button, Create, Delete, Filter, List, Row, Search, Sort, View, expr

from .models import Row_

class BigItem(View):
    model = Row_

    def ui(self, record):
        #: ``visible=`` здесь **только про булево поле с умолчанием**, и это
        #: важнее, чем кажется: такое условие целиком считается колонкой ``CASE
        #: WHEN`` в том же SELECT, и весь список -- 500 записей -- отвечает
        #: одним запросом, ни разу не позвав вычислитель.
        return Row(
            record.seq(widget="handle"),
            record.checked(widget="toggle"),
            record.code(widget="title"),
            record.region(widget="badge"),
            record.amount(),
            Button(icon="delete", action=record.delete(), visible=expr("!record.checked")),
        )

class BigDetail(View):
    model = Row_

    def ui(self, record):
        return (record.code(), record.region(widget="segmented"),
                record.amount(widget="stepper"), record.checked(),
                Button("Удалить", action=record.delete()))

class BigData(View):
    def ui(self, record):
        return (
            Button(place="fab", action=Row_.create(open=BigDetail)),
            List(
                Row_,
                item=BigItem,
                open=BigDetail,
                page_size=60,
                index=True,
                search=Search(
                    record.code,
                    Filter("Не проверено", expr("!record.checked"), default=True),
                    Filter("Север", expr('record.region = "n"')),
                    # `section=True` -- заголовок раздела над строками.
                    Sort("Вручную", record.seq, default=True, section=True),
                    Sort("По сумме", record.amount.desc()),
                ),
            ),
        )
