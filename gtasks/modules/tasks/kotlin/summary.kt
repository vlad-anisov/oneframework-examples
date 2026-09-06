// Тот же самый вид работы, что и у питона, только на Kotlin.

@OptIn(kotlin.js.ExperimentalJsExport::class)
@JsExport
fun сводка(кадр: dynamic): dynamic {
    val записи = кадр.records
    val всего = записи.length as Int
    var букв = 0
    var самое = ""
    for (i in 0 until всего) {
        val имя = (записи[i].name ?: "") as String
        букв += имя.length
        if (имя.length > самое.length) самое = имя
    }
    val ответ: dynamic = object {}
    ответ.строк = всего
    ответ.букв = букв
    ответ.самое_длинное = самое
    ответ.заглавными = самое.uppercase()
    return ответ
}
