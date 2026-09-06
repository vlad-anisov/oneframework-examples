/** Заметки на Kotlin -- ни строчки на другом языке. */

package notes

import org.apache.commons.text.WordUtils

import oneframework.Model
import oneframework.Records
import oneframework.Screen
import oneframework.View
import oneframework.app
import oneframework.boolean
import oneframework.button
import oneframework.list
import oneframework.row
import oneframework.string
import oneframework.text

object Note : Model("Note", label = "Заметка") {
    val title by string("Текст", required = true)
    val details by text("Подробности")
    val done by boolean("Выполнено")

    /** Пересчитать сводку по тексту заметки. */
    fun summary(self: Records) {
        for (record in self) {
            val words = Regex("\\s+").split(record.text(title)).filter { it.isNotEmpty() }
            // Заглавные расставляет **сторонняя** библиотека с Maven Central.
            val first = WordUtils.capitalizeFully(words.take(5).joinToString(" "))
            record[details] = "${words.size} слов: $first"
        }
    }
}

object Line : View("Line", model = Note) {
    override fun ui() = nodes(
        row(
            Note.done(widget = "toggle"),
            Note.title(widget = "title"),
            button(icon = "delete", action = Note.delete()),
        ),
    )
}

// Карточка -- работа, а не шаг пути: путь сюда весь состоит из списка, из
// которого пришли, и цепочка из двух звеньев повторила бы стрелку «назад» в
// том же баре.
object Card : View("Card", model = Note, crumbs = false) {
    override fun ui() = nodes(
        // Сохранение объявляется явно: карточка открывается черновиком, и до
        // сохранения записи ещё нет -- звать логику не о чем.
        button("Сохранить", action = Note.save(), place = "navbar", enabled = Note.title),
        Note.title(),
        Note.details(widget = "textarea"),
        Note.done(),
        // Метод модели прямо в кнопке.
        button("Пересчитать сводку", action = Note.action("summary")),
    )
}

object Board : View("Board", title = "Заметки") {
    override fun ui() = nodes(
        list(Note, item = Line, open = Card, empty = listOf("Пусто", "Нажмите +, чтобы добавить")),
        button(place = "fab", action = Note.create(open = Card, draft = true)),
    )
}

val application = app(
    title = "Заметки (Kotlin)",
    // Обе, а не одна: `commons-text` опирается на `commons-lang3`, а сборка
    // транзитивные зависимости не разрешает намеренно -- разрешатель это
    // Maven, и полурабочая его копия однажды соврала бы о версии.
    dependencies = listOf(
        "org.apache.commons:commons-text:1.12.0",
        "org.apache.commons:commons-lang3:3.14.0",
    ),
    color = "#45566b",
    locale = "ru",
    models = listOf(Note),
    views = listOf(Line, Card, Board),
    screens = listOf(Screen(Board)),
)
