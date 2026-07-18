# Free Proxy Keys for Russian mobile internet (LTE/4G)

This repository keeps a set of proxy-related lists and a local workflow helper for maintaining and testing them.

## Repository contents
- WHITE_LIST_PROXY_COLLECTION.txt - main proxy list with the current full set of entries
- HYSTERIA2.txt - extracted `hysteria2://` proxy entries
- source-list.txt - source reference list
- input/ - sample input files used for local workflow checks
- test-Hysteria-worflow.txt - notes and test data for the Hysteria workflow

## Features
- The lists include non-Russian servers to support access to AI services
- `HYSTERIA2.txt` contains only `hysteria2://` links extracted from the main list
- A local helper script is available for running the workflow simulation

## Local usage
Run the local workflow simulation with:

```bash
./run-local.sh
```

## Recent updates
Updated on 2026-07-18 based on the latest local commits:
- refreshed the proxy lists and kept previous HYSTERIA2 key entries intact
- added a dedicated test list for workflow validation
- updated the HYSTERIA2 export and local helper script
- added datetime annotations to HYSTERIA2 entries for easier tracking

## TODO
- Add an `xhttp` list
- Add output files for additional proxy protocols
- Improve the local run helper

## Contribution
You may suggest a source by sending a pull request.