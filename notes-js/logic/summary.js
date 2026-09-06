/** Сводка по тексту заметки. */
import upperFirst from "lodash/upperFirst.js";
import toLower from "lodash/toLower.js";

export function summary(self) {
  for (const record of self) {
    const words = String(record.title || "").split(/\s+/).filter(Boolean);
    const first = words.slice(0, 5).map((w) => upperFirst(toLower(w))).join(" ");
    record.details = `${words.length} слов: ${first}`;
  }
}
