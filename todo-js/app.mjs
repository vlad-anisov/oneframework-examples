/** Тот же todo, что `examples/todo/app.py`, -- на JavaScript. */

import {
  Button, Filter, List, Row, Screen, Search, Sort, app, boolean, color, integer,
  many2one, model, string, text, view,
  expr,
} from "oneframework";

const Tag = model("Tag", {
  fields: {
    name: string("Название", { required: true }),
    color: color("Цвет"),
  },
});

const TodoLine = model("TodoLine", {
  fields: {
    text: string("Задача", { required: true }),
    description: text("Описание"),
    tag: many2one(Tag, "Тег"),
    completed: boolean("Выполнено"),
    sequence: integer(),
  },
});

const TodoLineItem = view("TodoLineItem", {
  model: TodoLine,
  ui: (record) => Row(
    record.sequence({ widget: "handle" }),
    record.completed({ widget: "toggle" }),
    record.text({ widget: "title" }),
    record.tag({ widget: "tag" }),
    Button({ icon: "delete", action: record.delete() }),
  ),
});

const TodoLineDetail = view("TodoLineDetail", {
  model: TodoLine,
  // Карточка -- работа, а не шаг пути: путь сюда весь состоит из списка, из
  // которого пришли, и цепочка из двух звеньев повторила бы стрелку «назад» в
  // том же баре.
  crumbs: false,
  ui: (record) => [
    record.text(),
    record.description({ widget: "textarea" }),
    record.tag(),
    record.completed(),
    Button("Удалить", { action: record.delete() }),
  ],
});

const Todo = view("Todo", {
  state: { tag: many2one(Tag, "Тег") },
  ui: (record, view_) => [
    view_.tag({ widget: "chips" }),
    Button({ place: "fab",
             action: TodoLine.create({ open: TodoLineDetail, values: { tag: view_.tag } }) }),
    List(TodoLine, {
      item: TodoLineItem,
      open: TodoLineDetail,
      domain: expr("record.tag = view.tag"),
      search: Search(
        record.text,
        Filter("Осталось", expr("!record.completed"), { default: true }),
        Filter("Выполнено", record.completed),
        Sort("По порядку", record.sequence, { default: true }),
        Sort("Сначала новые", record.created_at.desc()),
      ),
    }),
  ],
});

export const application = app({
  title: "Todo",
  models: [Tag, TodoLine],
  views: [TodoLineItem, TodoLineDetail, Todo],
  screens: [Screen(Todo)],
  root: Todo,
});
