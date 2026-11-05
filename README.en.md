# Free Proxy Keys for Russian Mobile Internet (LTE/4G)

Russian version: [README.md](README.md)

This repository collects keys from open sources, with a focus on bypassing mobile network restrictions.

## Features

- All lists are assembled from keys collected during the last 72 hours, newest first. Duplicates are removed.
- Russian servers are excluded from the lists to ensure access to AI services.
- Filters exclude some keys with parameters that are not supported by the sing-box core.

## Usage

### Subscription links

Copy any link below and paste it as a subscription in your device client:

- [Alive proxies](https://raw.githubusercontent.com/Subzio/subzio/main/ALIVE.txt#ALIVE@subzio) — HTTPS ping of the Combined Proxy List, rebuilt hourly.
- [Hysteria2](https://raw.githubusercontent.com/Subzio/subzio/main/HYSTERIA2.txt#HYSTERIA2@subzio)
- [Trojan](https://raw.githubusercontent.com/Subzio/subzio/main/TROJAN.txt#TROJAN@subzio)
- [XHTTP](https://raw.githubusercontent.com/Subzio/subzio/main/XHTTP.txt#XHTTP@subzio)
- [Combined Proxy List](https://raw.githubusercontent.com/Subzio/subzio/main/WHITE_LIST_PROXY_COLLECTION.txt#all-protocols@subzio) — includes mobile network restriction bypasses

### Local usage

Run the local workflow simulation:

```bash
./check-alive-local.sh
```

The script uses matching installed binaries when available, otherwise downloads pinned Linux x86_64 binaries into the ignored `.bin/` directory. It runs the checker tests and rebuilds `ALIVE.txt`, but does not commit or push changes. Run `./run-local.sh` separately to refresh the source collection.

## For developers

### Repository structure

`WHITE_LIST_PROXY_COLLECTION.txt` — **the combined list**.

After each GitHub Actions run or `./run-local.sh` execution, a file named `<datetime>-...` is added to `WHITE_LIST_PROXY_COLLECTION/`. Only snapshots from the last 72 hours are included in *the combined list*.

### Protocol-based lists

- `HYSTERIA2.txt` — current `hysteria2://` entries from *the combined list*
- `TROJAN.txt` — current `trojan://` entries
- `XHTTP.txt` — current links with the `type=xhttp` parameter
- `ALIVE.txt` — entries that successfully make an HTTPS request from a GitHub Actions runner; rebuilt hourly

### Repository utility files

- `source-list.txt` — list of sources
- `input/` — temporary folder

### TODO

- Better deduplication by credentials (`login@server`)
- A proxy list for Gemini API and web
- ipv6 list

## Contribution

You can suggest changes via a pull request or by creating an issue.
