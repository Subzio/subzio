# Free Proxy Keys for Russian mobile internet (LTE/4G)

Russian version: [README.md](README.md)

This repository collects keys from free proxy servers with an emphasis on bypassing censorship/blocking.

The lists are adapted for sing-box clients and are 100% compatible with xray core.

## Subscription (direct links to the lists)
Copy any link below and paste it as a subscription in your client:
- [Hysteria2](https://raw.githubusercontent.com/Subzio/subzio/main/HYSTERIA2.txt#HYSTERIA2@subzio)
- [Trojan](https://raw.githubusercontent.com/Subzio/subzio/main/TROJAN.txt#TROJAN@subzio)
- [XHTTP](https://raw.githubusercontent.com/Subzio/subzio/main/XHTTP.txt#XHTTP@subzio)
- [Full proxy list](https://raw.githubusercontent.com/Subzio/subzio/main/WHITE_LIST_PROXY_COLLECTION.txt#all-protocols@subzio) - This includes censorship bypasses

---

## Repository contents
- `WHITE_LIST_PROXY_COLLECTION/` — filtered snapshots from each run over the last 72 hours; duplicates within snapshots are preserved
- `WHITE_LIST_PROXY_COLLECTION.txt` — main list of unique entries found in snapshots from the last 72 hours
- `HYSTERIA2.txt` — extracted `hysteria2://` entries. These keys accumulate, with the latest keys at the beginning of the list.
- `TROJAN.txt` — extracted `trojan://` entries. New keys are added to the beginning of the list.
- `XHTTP.txt` — current list of links with the `type=xhttp` parameter; it is fully rebuilt on each run.
- `source-list.txt` — list of sources
- `input/` — temporary folder

## Features
- The lists do not include Russian servers to ensure access to AI services.
- The main list is built from snapshots from the last 72 hours; only exact duplicate lines are removed.
- `HYSTERIA2.txt` contains only `hysteria2://` links extracted from `WHITE_LIST_PROXY_COLLECTION.txt`
- `TROJAN.txt` contains only `trojan://` links extracted from `WHITE_LIST_PROXY_COLLECTION.txt`
- `XHTTP.txt` contains only links with the `type=xhttp` parameter extracted from `WHITE_LIST_PROXY_COLLECTION.txt`

## Local usage
Run the local workflow simulation:

```bash
./run-local.sh
```

## TODO
- Live proxies as a separate list: Resolve Outer IP + Geo
- Proxy list for Gemini API|Web

## Contribution
You can suggest a source via pull request.
