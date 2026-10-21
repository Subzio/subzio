# Бесплатные ключи прокси для российского мобильного интернета (LTE/4G)

English version: [README.en.md](README.en.md)

Этот репозиторий собирает ключи с бесплатных серверов с упором на обход БС.

## Прямые ссылки на списки
- [Полный список прокси](https://raw.githubusercontent.com/Subzio/subzio/main/WHITE_LIST_PROXY_COLLECTION.txt)
- [Hysteria2](https://raw.githubusercontent.com/Subzio/subzio/main/HYSTERIA2.txt)
- [Trojan](https://raw.githubusercontent.com/Subzio/subzio/main/TROJAN.txt)

## Содержимое репозитория
- `WHITE_LIST_PROXY_COLLECTION.txt` — основной список прокси с текущим полным набором записей
- `HYSTERIA2.txt` — извлечённые записи вида `hysteria2://`. Эти ключи накапливаются, последние ключи в начале списка.
- `TROJAN.txt` — извлечённые записи вида `trojan://`. Новые ключи добавляются в начало списка.
- `source-list.txt` — список источников
- `input/` — временная папка

## Фичи
- В списках нет российских серверов, чтобы обеспечить доступ к AI-сервисам.
- `HYSTERIA2.txt` содержит только ссылки `hysteria2://`, извлечённые из `WHITE_LIST_PROXY_COLLECTION.txt`
- `TROJAN.txt` содержит только ссылки `trojan://`, извлечённые из `WHITE_LIST_PROXY_COLLECTION.txt`

## Локальное использование
Запустите симуляцию workflow локально:

```bash
./run-local.sh
```

## TODO
### Urgent
- Список прокси для Gemini Api|Web
### Later
- Добавить списоки для `xhttp`


## Участие
Вы можете предложить источник через pull request.
