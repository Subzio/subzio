# Бесплатные прокси-ключи для российского мобильного интернета (LTE/4G)

English version: [README.en.md](README.en.md)

Этот репозиторий собирает ключи из открытых источников с упором на обход БС.

## Фичи

- Все списки собираются из ключей, собранных за последние 72 часа, начиная с самых новых. Дублирующие конфигурации удаляются; разные параметры транспорта и TLS сохраняются.
- При удалении дублей учитываются протокол, учётные данные, сервер, порт, путь и все параметры подключения. Порядок параметров URL и фрагмент с отображаемым именем не учитываются.
- Чтобы обеспечить доступ к AI-сервисам, в списках нет российских серверов.
- Фильтры исключают некоторые ключи, параметры которых не поддерживаются ядром sing-box.

## Использование

### Подиски (прямые ссылки на списки)

Скопируйте любую ссылку ниже и вставьте её как подписку в клиент вашего устройства:

- [Живые прокси](https://raw.githubusercontent.com/Subzio/subzio/main/ALIVE.txt#ALIVE@subzio) — HTTPS ping общего списка.
- [Hysteria2](https://raw.githubusercontent.com/Subzio/subzio/main/HYSTERIA2.txt#HYSTERIA2@subzio)
- [Trojan](https://raw.githubusercontent.com/Subzio/subzio/main/TROJAN.txt#TROJAN@subzio)
- [XHTTP](https://raw.githubusercontent.com/Subzio/subzio/main/XHTTP.txt#XHTTP@subzio)
- [Общий список прокси](https://raw.githubusercontent.com/Subzio/subzio/main/WHITE_LIST_PROXY_COLLECTION.txt#Common-list@subzio) - Тут есть обходы БС

### Локальное использование

Запустите проверку доступности прокси:

```bash
./check-alive-local.sh
```

Скрипт использует установленные бинарные файлы нужных версий или загружает закреплённые версии для Linux x86_64 в игнорируемую Git папку `.bin/`. Он запускает тесты и обновляет `ALIVE.txt`, но не выполняет commit или push. Для обновления исходного списка отдельно запустите `./run-local.sh`.

## Для разработчиков

### Структура репозитория

**Общий список** — `WHITE_LIST_PROXY_COLLECTION.txt`.

После каждого запуска `GH Actions` или `./run-local.sh` в папке `WHITE_LIST_PROXY_COLLECTION/` появляется файл с именем `<datetime>-...`. В *общий список* включаются только снимки за последние 72 часа.

### Списки по протоколам

- `HYSTERIA2.txt` — текущие записи вида `hysteria2://` из *общего списка*
- `TROJAN.txt` — текущие записи вида `trojan://`
- `XHTTP.txt` — текущий список ссылок с параметром `type=xhttp`
- `ALIVE.txt` — записи, через которые GitHub Actions runner успешно выполнил HTTPS-запрос

### Служебные файлы репозитория

- `source-list.txt` — список источников
- `input/` — временная папка

### TODO

- Список прокси для Gemini Api|Web
- ipv6 list

## Участие

Вы можете предложить изменения через Pull Request или создав Issue.
