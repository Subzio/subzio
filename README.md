# Бесплатные ключи прокси для российского мобильного интернета (LTE/4G)

English version: [README.en.md](README.en.md)

Этот репозиторий собирает ключи с бесплатных серверов с упором на обход БС.

Списки адаптированны под sing box клиенты и 100% совместимы с xray core.

---

## Использование

### Подиски (прямые ссылки на списки)

Скопируйте любую ссылку ниже и вставьте её как подписку в клиент вашего устройства:

- [Hysteria2](https://raw.githubusercontent.com/Subzio/subzio/main/HYSTERIA2.txt#HYSTERIA2@subzio)
- [Trojan](https://raw.githubusercontent.com/Subzio/subzio/main/TROJAN.txt#TROJAN@subzio)
- [XHTTP](https://raw.githubusercontent.com/Subzio/subzio/main/XHTTP.txt#XHTTP@subzio)
- [Полный список прокси](https://raw.githubusercontent.com/Subzio/subzio/main/WHITE_LIST_PROXY_COLLECTION.txt#all-protocols@subzio) - Тут есть обходы БС

### Локальное использование

Запустите симуляцию workflow локально:

```bash
./run-local.sh
```

---

## Фичи

- Чтобы обеспечить доступ к AI-сервисам, в списках нет российских серверов.
- Общий список `WHITE_LIST_PROXY_COLLECTION.txt` собирается из снимков за последние 72 часа, начиная с самых новых; если запись повторяется, используется её вариант из самого нового снимка.
- `HYSTERIA2.txt` содержит ссылки `hysteria2://`
- `TROJAN.txt` содержит ссылки `trojan://`
- `XHTTP.txt` содержит только ссылки с параметром `type=xhttp`

---

## Для разработчиков

### Структура репозитория

После каждого запуска `GH Actions` или `./run-local.sh` в папке `WHITE_LIST_PROXY_COLLECTION/` появляется файл с именем `<datetime>-...`. Снимки автоматически не удаляются; в общий список включаются только снимки за последние 72 часа.

Пока что, фильтры исключают российские серверы и некоторые ключи, параметры которых не поддерживаются ядром sing-box.

`WHITE_LIST_PROXY_COLLECTION.txt` — общий список ключей (без дубликатов) за последние 72 часа.

### Списки по протоколам

- `HYSTERIA2.txt` — текущие записи вида `hysteria2://` из общего списка
- `TROJAN.txt` — текущие записи вида `trojan://`
- `XHTTP.txt` — текущий список ссылок с параметром `type=xhttp`

### Служебные файлы репозитория

- `source-list.txt` — список источников
- `input/` — временная папка

### TODO

- Живые прокси как отдельный список: Resolve Outer IP + Geo
- Список прокси для Gemini Api|Web

## Участие

Вы можете предложить изменения через Pull Request или создав Issue.
