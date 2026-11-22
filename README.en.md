# Free Proxy Keys for Russian Mobile Internet (LTE/4G)

Russian version: [README.md](README.md)

This repository collects keys from open sources with a focus on bypassing censorship.

## Features

- All lists are assembled from keys collected over the last 72 hours, starting with the newest ones.
- Russian servers are excluded from the lists to ensure access to AI services.
- Shadowsocks and SOCKS keys are excluded, as are insecure connections using `security=none`.
- Duplicate configurations are removed; different transport and TLS parameters are preserved.
- When removing duplicates, the protocol, credentials, server, port, path, and all connection parameters are taken into account. URL parameter order and the display-name fragment are ignored.

## Usage

### Subscription links

Copy any link below and add it as a new subscription in your device client:

- [🔗 Combined proxy list](https://raw.githubusercontent.com/Subzio/subzio/main/WHITE_LIST_PROXY_COLLECTION.txt#Common-list@subzio) — includes censorship bypasses
- [🔗 XHTTP](https://raw.githubusercontent.com/Subzio/subzio/main/XHTTP.txt#XHTTP@subzio) — suitable for gaming
- [🔗 Trojan](https://raw.githubusercontent.com/Subzio/subzio/main/TROJAN.txt#TROJAN@subzio)
- [🔗 Hysteria2](https://raw.githubusercontent.com/Subzio/subzio/main/HYSTERIA2.txt#HYSTERIA2@subzio) — ☠️ Does not work on LTE

### Local usage

```bash
bash ./run-local.sh
```

## Repository structure

**Combined list** — `WHITE_LIST_PROXY_COLLECTION.txt`.

After each GitHub Actions run or `./run-local.sh` execution, a file named `<datetime>-...` appears in `WHITE_LIST_PROXY_COLLECTION/`. Only snapshots from the last 72 hours are included in the *combined list*.

### Protocol-based lists

- `HYSTERIA2.txt` — current `hysteria2://` entries from the *combined list*
- `TROJAN.txt` — current `trojan://` entries
- `XHTTP.txt` — current links with the `type=xhttp` parameter

### Repository utility files

- `source-list.txt` — list of sources
- `input/` — temporary folder

### TODO

- Proxy list for Gemini API|Web
- IPv6 list

## Contribution

You can suggest changes via a pull request or by creating an issue.
