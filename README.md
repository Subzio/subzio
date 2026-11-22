# Бесплатные прокси-ключи для российского мобильного интернета (LTE/4G)

English version: [README.en.md](README.en.md)

Этот репозиторий собирает ключи из открытых источников с упором на обход БС.

## Фичи

- Все списки собираются из ключей, собранных за последние 72 часа, начиная с самых новых.
- Чтобы обеспечить доступ к AI-сервисам, в списках нет российских серверов.
- Из списков исключаются ключи протоколов Shadowsocks и SOCKS, а также небезопасные соединения с `security=none`.
- Дублирующие конфигурации удаляются; разные параметры транспорта и TLS сохраняются.
- При удалении дублей учитываются протокол, учётные данные, сервер, порт, путь и все параметры подключения. Порядок параметров URL и фрагмент с отображаемым именем не учитываются.

## Использование

### Подиски (прямые ссылки на списки)

Скопируйте любую ссылку ниже и добавьте её как новую подписку в клиент вашего устройства:

- [🔗 Общий список прокси](https://raw.githubusercontent.com/Subzio/subzio/main/WHITE_LIST_PROXY_COLLECTION.txt#Common-list@subzio) / Тут есть обходы БС
- [🔗 XHTTP](https://raw.githubusercontent.com/Subzio/subzio/main/XHTTP.txt#XHTTP@subzio) / Подходит для игр
- [🔗 Trojan](https://raw.githubusercontent.com/Subzio/subzio/main/TROJAN.txt#TROJAN@subzio)
- [🔗 Hysteria2](https://raw.githubusercontent.com/Subzio/subzio/main/HYSTERIA2.txt#HYSTERIA2@subzio) / ☠️ В LTE не работает

### Локальное использование

```bash
bash ./run-local.sh
```

## Структура репозитория

**Общий список** — `WHITE_LIST_PROXY_COLLECTION.txt`.

После каждого запуска `GH Actions` или `./run-local.sh` в папке `WHITE_LIST_PROXY_COLLECTION/` появляется файл с именем `<datetime>-...`. В *общий список* включаются только снимки за последние 72 часа.

### Списки по протоколам

- `HYSTERIA2.txt` — текущие записи вида `hysteria2://` из *общего списка*
- `TROJAN.txt` — текущие записи вида `trojan://`
- `XHTTP.txt` — текущий список ссылок с параметром `type=xhttp`

### Служебные файлы репозитория

- `source-list.txt` — список источников
- `input/` — временная папка

## TODO

- Список прокси для Gemini Api|Web
- ipv6 list

## Участие

Вы можете предложить изменения через Pull Request или создав Issue.
