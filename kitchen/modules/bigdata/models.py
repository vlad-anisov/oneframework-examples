from oneframework import Boolean, Integer, Model, Selection, String

class Row_(Model):
    _label = "Строка"

    code = String("Код", required=True)
    region = Selection(
        [("n", "Север"), ("s", "Юг"), ("e", "Восток"), ("w", "Запад")], "Регион"
    )
    amount = Integer("Сумма")
    checked = Boolean("Проверено")
    seq = Integer()
