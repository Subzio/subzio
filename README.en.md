# Free Proxy Keys for Russian mobile internet (LTE/4G)

This repository collects keys from free proxy servers with a focus on bypassing blocks.

## Repository contents
- `WHITE_LIST_PROXY_COLLECTION.txt` — main proxy list with the current full set of entries
- `HYSTERIA2.txt` — extracted `hysteria2://` entries. These keys accumulate, with the latest keys at the beginning of the list.
- `source-list.txt` — list of sources
- `input/` — temporary folder

## Features
- The lists do not include Russian servers to support access to AI services
- `HYSTERIA2.txt` contains only `hysteria2://` links extracted from `WHITE_LIST_PROXY_COLLECTION.txt`

## Local usage
Run the local workflow simulation with:

```bash
./run-local.sh
```

## TODO
- Add lists for `xhttp`, `trojan`
- Generate XRAY Json with auto-balancer from `WHITE_LIST_PROXY_COLLECTION.txt`

## Contribution
You may suggest a source by sending a pull request.
