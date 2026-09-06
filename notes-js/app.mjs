/** Заметки на JavaScript -- ни строчки на другом языке. */

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
    // нет, а логике нужна сторонняя библиотека.
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
  // Карточка -- работа, а не шаг пути: путь сюда весь состоит из списка, из
  // которого пришли, и цепочка из двух звеньев повторила бы стрелку «назад» в
  // том же баре.
  crumbs: false,
  ui: (record) => [
    Button("Сохранить", { action: record.save(), place: "navbar", enabled: record.title }),
    record.title(),
    record.details({ widget: "textarea" }),
    record.done(),
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
