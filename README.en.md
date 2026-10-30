# Free Proxy Keys for Russian mobile internet (LTE/4G)

Russian version: [README.md](README.md)

This repository collects keys from free proxy servers with a focus on bypassing blocks.

The lists are apdopted for sing box based clients, and 100% compatible with xray core clients.

## Subscription (direct links to the lists)
- [Hysteria2](https://raw.githubusercontent.com/Subzio/subzio/main/HYSTERIA2.txt#HYSTERIA2@subzio)
- [Trojan](https://raw.githubusercontent.com/Subzio/subzio/main/TROJAN.txt#TROJAN@subzio)
- [XHTTP](https://raw.githubusercontent.com/Subzio/subzio/main/XHTTP.txt#XHTTP@subzio)
- [Full proxy list](https://raw.githubusercontent.com/Subzio/subzio/main/WHITE_LIST_PROXY_COLLECTION.txt#all-protocols@subzio)

## Repository contents
- `WHITE_LIST_PROXY_COLLECTION.txt` — main list of unique entries found in snapshots from the last 72 hours
- `WHITE_LIST_PROXY_COLLECTION/` — filtered snapshots from each run, retained for 72 hours; duplicates within snapshots are preserved
- `HYSTERIA2.txt` — extracted `hysteria2://` entries. These keys accumulate, with the latest keys at the beginning of the list.
- `TROJAN.txt` — extracted `trojan://` entries, with the latest keys at the beginning of the list.
- `XHTTP.txt` — current links with the `type=xhttp` parameter; this list is rebuilt on every run.
- `source-list.txt` — list of sources
- `input/` — temporary folder

## Features
- The lists do not include Russian servers to support access to AI services
- The main list is rebuilt from snapshots from the last 72 hours; only exact duplicate lines are removed.
- `HYSTERIA2.txt` contains only `hysteria2://` links extracted from `WHITE_LIST_PROXY_COLLECTION.txt`
- `TROJAN.txt` contains only `trojan://` links extracted from `WHITE_LIST_PROXY_COLLECTION.txt`
- `XHTTP.txt` contains only links with the `type=xhttp` parameter extracted from `WHITE_LIST_PROXY_COLLECTION.txt`

## Local usage
Run the local workflow simulation with:

```bash
./run-local.sh
```

## TODO
### Urgent
- Create a proxy list for Gemini API and Web
### Later
- Generate XRAY Json with auto-balancer from `WHITE_LIST_PROXY_COLLECTION.txt`

## Contribution
You may suggest a source by sending a pull request.
