# Бесплатные прокси-ключи для российского мобильного интернета (LTE/4G)

English version: [README.en.md](README.en.md)

Этот репозиторий собирает ключи с бесплатных серверов с упором на обход БС.

## Фичи

- Все списки собираются из ключей, собранных за последние 72 часа, начиная с самых новых. Дубли удаляются.
- Чтобы обеспечить доступ к AI-сервисам, в списках нет российских серверов.
- Фильтры исключают некоторые ключи, параметры которых не поддерживаются ядром sing-box.

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

## Для разработчиков

### Структура репозитория

**Общий список** — `WHITE_LIST_PROXY_COLLECTION.txt`.

После каждого запуска `GH Actions` или `./run-local.sh` в папке `WHITE_LIST_PROXY_COLLECTION/` появляется файл с именем `<datetime>-...`. В *общий список* включаются только снимки за последние 72 часа.

### Списки по протоколам

- `HYSTERIA2.txt` — текущие записи вида `hysteria2://` из *общего списка*
- `TROJAN.txt` — текущие записи вида `trojan://`
- `XHTTP.txt` — текущий список ссылок с параметром `type=xhttp`

### Служебные файлы репозитория

- `source-list.txt` — список источников
- `input/` — временная папка

### TODO

- Better dedublication by creds (login@server)
- Живые прокси как отдельный список: Resolve Outer IP + Geo
- Список прокси для Gemini Api|Web

## Участие

Вы можете предложить изменения через Pull Request или создав Issue.
