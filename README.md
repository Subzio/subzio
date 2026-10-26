# Бесплатные ключи прокси для российского мобильного интернета (LTE/4G)

English version: [README.en.md](README.en.md)

Этот репозиторий собирает ключи с бесплатных серверов с упором на обход БС.

Списки адаптированны под sing box клиенты и 100% совместимы с xray core.

## Подиски (прямые ссылки на списки)
- [Trojan](https://raw.githubusercontent.com/Subzio/subzio/main/TROJAN.txt#TROJAN@subzio) - Рекомендуется
- [XHTTP](https://raw.githubusercontent.com/Subzio/subzio/main/XHTTP.txt#XHTTP@subzio)
- [Hysteria2](https://raw.githubusercontent.com/Subzio/subzio/main/HYSTERIA2.txt#HYSTERIA2@subzio) - Раньше было лучше
- [Полный список прокси](https://raw.githubusercontent.com/Subzio/subzio/main/WHITE_LIST_PROXY_COLLECTION.txt#all-protocols@subzio) - Тут есть обходы БС

## Содержимое репозитория
- `WHITE_LIST_PROXY_COLLECTION.txt` — основной список прокси с текущим полным набором записей
- `HYSTERIA2.txt` — извлечённые записи вида `hysteria2://`. Эти ключи накапливаются, последние ключи в начале списка.
- `TROJAN.txt` — извлечённые записи вида `trojan://`. Новые ключи добавляются в начало списка.
- `XHTTP.txt` — текущий список ссылок с параметром `type=xhttp`; он полностью пересоздаётся при каждом запуске.
- `source-list.txt` — список источников
- `input/` — временная папка

## Фичи
- В списках нет российских серверов, чтобы обеспечить доступ к AI-сервисам.
- `HYSTERIA2.txt` содержит только ссылки `hysteria2://`, извлечённые из `WHITE_LIST_PROXY_COLLECTION.txt`
- `TROJAN.txt` содержит только ссылки `trojan://`, извлечённые из `WHITE_LIST_PROXY_COLLECTION.txt`
- `XHTTP.txt` содержит только ссылки с параметром `type=xhttp`, извлечённые из `WHITE_LIST_PROXY_COLLECTION.txt`

## Локальное использование
Запустите симуляцию workflow локально:

```bash
./run-local.sh
```

## TODO
- Список прокси для Gemini Api|Web


## Участие
Вы можете предложить источник через pull request.
