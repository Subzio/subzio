# Free Proxy Keys for Russian Mobile Internet (LTE/4G)

Russian version: [README.md](README.md)

This repository collects free proxy keys with an emphasis on bypassing censorship and blocking.

The lists are optimized for sing-box clients and are 100% compatible with xray core.

## Subscriptions (direct links)
Copy any of the links below and paste it as a subscription in your device client:
- [Hysteria2](https://raw.githubusercontent.com/Subzio/subzio/main/HYSTERIA2.txt#HYSTERIA2@subzio)
- [Trojan](https://raw.githubusercontent.com/Subzio/subzio/main/TROJAN.txt#TROJAN@subzio)
- [XHTTP](https://raw.githubusercontent.com/Subzio/subzio/main/XHTTP.txt#XHTTP@subzio)
- [Full proxy list](https://raw.githubusercontent.com/Subzio/subzio/main/WHITE_LIST_PROXY_COLLECTION.txt#all-protocols@subzio) — includes censorship bypasses

---

## Repository contents
- `WHITE_LIST_PROXY_COLLECTION/` — filtered snapshots from each run over the last 72 hours; duplicate entries within snapshots are preserved.
- `WHITE_LIST_PROXY_COLLECTION.txt` — consolidated list of unique entries from the last 72 hours.
- `HYSTERIA2.txt` — extracted `hysteria2://` entries. These keys accumulate, with the newest entries at the top of the list.
- `TROJAN.txt` — extracted `trojan://` entries. New entries are added to the top of the list.
- `XHTTP.txt` — current list of links with the `type=xhttp` parameter; it is rebuilt from scratch on each run.
- `source-list.txt` — source list
- `input/` — temporary folder

## Features
- The lists exclude Russian servers to ensure access to AI services.
- The main list is built from snapshots collected over the last 72 hours.
- `HYSTERIA2.txt` contains only `hysteria2://` links extracted from `WHITE_LIST_PROXY_COLLECTION.txt`.
- `TROJAN.txt` contains only `trojan://` links extracted from `WHITE_LIST_PROXY_COLLECTION.txt`.
- `XHTTP.txt` contains only links with the `type=xhttp` parameter extracted from `WHITE_LIST_PROXY_COLLECTION.txt`.

## Local usage
Run the local workflow simulation:

```bash
./run-local.sh
```

## TODO
- A live-proxy list: Resolve Outer IP + Geo
- A proxy list for Gemini API|Web

## Contribution
You can suggest a source via pull request.
