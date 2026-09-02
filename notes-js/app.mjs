/**
 * Заметки на JavaScript -- ни строчки на другом языке.
 *
 * Три приложения этой тройки одинаковы снаружи: те же модели, тот же экран, та
 * же кнопка и тот же ответ. Различается ровно одно -- на чём написано
 * приложение и чем исполняется его логика на устройстве:
 *
 * * `notes-python` -- в приложение кладётся **дополнительный интерпретатор**
 *   (Pyodide, 13 МБ), и он исполняет исходник;
 * * `notes-js`     -- исполняет **встроенный** движок webview, класть нечего;
 * * `notes-kotlin` -- на сборке получается **скомпилированный модуль** `.wasm`.
 *
 * Одинаковы они не на глаз: объявления всех трёх дают побайтово одни и те же
 * документы моделей и видов, и это закреплено `tests/test_three_languages.py`.
 *
 *     npx oneframework build web examples/notes-js/app.mjs
 */

import {
  Button, List, Row, Screen, action, app, boolean, model, string, text,
  view,
} from "oneframework";

const Note = model("Note", {
  label: "Заметка",
  fields: {
    title: string("Текст", { required: true }),
    details: text("Подробности"),
    done: boolean("Выполнено"),
  },
  logic: {
    // Тело файлом, а не здесь: у функции, взятой через `toString()`, импортов
    // нет, а логике нужна сторонняя библиотека. Сборка упакует файл вместе со
    // всем, что он ввёз.
    summary: action(new URL("logic/summary.js", import.meta.url)),
  },
});

const Line = view("Line", {
  model: Note,
  ui: (record) => Row(
    record.done({ widget: "toggle" }),
    record.title({ widget: "title" }),
    Button({ icon: "delete", action: record.delete() }),
  ),
});

const Card = view("Card", {
  model: Note,
  // Карточка -- работа, а не шаг пути: путь сюда весь состоит из списка,
  // из которого пришли, и цепочка из двух звеньев повторила бы стрелку
  // «назад» в том же баре.
  crumbs: false,
  ui: (record) => [
    // Сохранение объявляется явно: карточка открывается черновиком, и до
    // сохранения записи ещё нет -- звать логику не о чем.
    Button("Сохранить", { action: record.save(), place: "navbar", enabled: record.title }),
    record.title(),
    record.details({ widget: "textarea" }),
    record.done(),
    // Метод записи прямо в кнопке: ни строки с именем, ни обёртки. Скобки
    // значат «на этой записи», а не «прямо сейчас». Что за методом стоит --
    // питон, JavaScript или скомпилированный модуль -- отсюда не видно, и это
    // главное.
    Button("Пересчитать сводку", { action: record.summary() }),
  ],
});

const Board = view("Board", {
  title: "Заметки",
  ui: () => [
    List(Note, { item: Line, open: Card, empty: ["Пусто", "Нажмите +, чтобы добавить"] }),
    Button({ place: "fab", action: Note.create({ open: Card, draft: true }) }),
  ],
});

export default app({
  title: "Заметки (JavaScript)",
  color: "#6b5a45",
  locale: "ru",
  models: [Note],
  views: [Line, Card, Board],
  screens: [Screen(Board)],
});
