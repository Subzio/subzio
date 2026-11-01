# Free Proxy Keys for Russian Mobile Internet (LTE/4G)

Russian version: [README.md](README.md)

This repository collects free proxy keys with a focus on bypassing censorship and blocking.

The lists are optimized for sing-box clients and are 100% compatible with xray core.

---

## Usage

### Subscription links
Copy any link below and paste it as a subscription in your device client:

- [Hysteria2](https://raw.githubusercontent.com/Subzio/subzio/main/HYSTERIA2.txt#HYSTERIA2@subzio)
- [Trojan](https://raw.githubusercontent.com/Subzio/subzio/main/TROJAN.txt#TROJAN@subzio)
- [XHTTP](https://raw.githubusercontent.com/Subzio/subzio/main/XHTTP.txt#XHTTP@subzio)
- [Full proxy list](https://raw.githubusercontent.com/Subzio/subzio/main/WHITE_LIST_PROXY_COLLECTION.txt#all-protocols@subzio) — includes censorship bypasses

---

## Features

- Russian servers are excluded from the lists to ensure access to AI services.
- The main list `WHITE_LIST_PROXY_COLLECTION.txt` is built from servers collected over the last 72 hours.
- `HYSTERIA2.txt` contains only `hysteria2://` links extracted from `WHITE_LIST_PROXY_COLLECTION.txt`.
- `TROJAN.txt` contains only `trojan://` links extracted from `WHITE_LIST_PROXY_COLLECTION.txt`.
- `XHTTP.txt` contains only links with the `type=xhttp` parameter extracted from `WHITE_LIST_PROXY_COLLECTION.txt`.

---

## For developers

### Repository structure
After each GitHub Actions run or `./run-local.sh` execution, a new file named `<datetime>-...` is added to `WHITE_LIST_PROXY_COLLECTION/`. It contains all currently available keys gathered from `source-list.txt`.

At the moment, the filters exclude Russian servers and some keys whose parameters are not supported by the sing-box core.

`WHITE_LIST_PROXY_COLLECTION.txt` is the combined list of unique keys collected over the last 72 hours.

### Protocol-based lists

- `HYSTERIA2.txt` — extracted `hysteria2://` entries. These keys accumulate, with the newest entries at the top of the list.
- `TROJAN.txt` — extracted `trojan://` entries. New entries are added to the top of the list.
- `XHTTP.txt` — current list of links with the `type=xhttp` parameter; it is fully rebuilt on each run.

### Repository utility files

- `source-list.txt` — list of sources
- `input/` — temporary folder

### Local usage
Run the local workflow simulation:

```bash
./run-local.sh
```

### TODO

- Live proxies as a separate list: Resolve Outer IP + Geo
- Proxy list for Gemini API|Web

## Contribution

You can suggest changes via Pull Request or by creating an Issue.
