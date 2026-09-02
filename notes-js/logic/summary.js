/**
 * Сводка по тексту заметки.
 *
 * Файлом, а не прямо в модели, ровно по одной причине: у функции, взятой
 * через `toString()`, импортов нет. Нужна сторонняя библиотека -- логика
 * пишется файлом, и сборка упакует его вместе со всем, что он ввёз.
 *
 * Заглавные расставляет `lodash` -- пакет с npm, которого нет ни в одном
 * движке. Работает -- значит упаковщик действительно положил чужой код в
 * модуль, а не оставил его на машине сборки.
 */
import upperFirst from "lodash/upperFirst.js";
import toLower from "lodash/toLower.js";

export function summary(self) {
  for (const record of self) {
    const words = String(record.title || "").split(/\s+/).filter(Boolean);
    const first = words.slice(0, 5).map((w) => upperFirst(toLower(w))).join(" ");
    record.details = `${words.length} слов: ${first}`;
  }
}
