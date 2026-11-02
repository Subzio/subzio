# Free Proxy Keys for Russian Mobile Internet (LTE/4G)

Russian version: [README.md](README.md)

This repository collects keys from free servers, with a focus on bypassing mobile network restrictions.

## Features

- All lists are assembled from keys collected during the last 72 hours, newest first. Duplicates are removed.
- Russian servers are excluded from the lists to ensure access to AI services.
- Filters exclude some keys with parameters that are not supported by the sing-box core.

## Usage

### Subscription links

Copy any link below and paste it as a subscription in your device client:

- [Hysteria2](https://raw.githubusercontent.com/Subzio/subzio/main/HYSTERIA2.txt#HYSTERIA2@subzio)
- [Trojan](https://raw.githubusercontent.com/Subzio/subzio/main/TROJAN.txt#TROJAN@subzio)
- [XHTTP](https://raw.githubusercontent.com/Subzio/subzio/main/XHTTP.txt#XHTTP@subzio)
- [Full proxy list](https://raw.githubusercontent.com/Subzio/subzio/main/WHITE_LIST_PROXY_COLLECTION.txt#all-protocols@subzio) — includes mobile network restriction bypasses

### Local usage

Run the local workflow simulation:

```bash
./run-local.sh
```

## For developers

### Repository structure

- `WHITE_LIST_PROXY_COLLECTION.txt` — the combined list
- `HYSTERIA2.txt` contains `hysteria2://` links
- `TROJAN.txt` contains `trojan://` links
- `XHTTP.txt` contains only links with the `type=xhttp` parameter

After each GitHub Actions run or `./run-local.sh` execution, a file named `<datetime>-...` is added to `WHITE_LIST_PROXY_COLLECTION/`. Snapshots are not automatically deleted; only snapshots from the last 72 hours are included in the combined list.

### Protocol-based lists

- `HYSTERIA2.txt` — current `hysteria2://` entries from the combined list
- `TROJAN.txt` — current `trojan://` entries
- `XHTTP.txt` — current links with the `type=xhttp` parameter

### Repository utility files

- `source-list.txt` — list of sources
- `input/` — temporary folder

### TODO

- Better deduplication by credentials (`login@server`)
- A separate list of live proxies: resolve outer IP and geolocation
- A proxy list for Gemini API and web

## Contribution

You can suggest changes via a pull request or by creating an issue.
