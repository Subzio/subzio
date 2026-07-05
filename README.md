# Free VPN Keys for Russian mobile internet (LTE/4G)

- WHITE_LIST_PROXY_COLLECTION.txt - default filtered list
- HYSTERIA2.txt - extracted `hysteria2://` proxy entries

## Features
- The lists have non-Russian servers to provide an access to AI services
- `HYSTERIA2.txt` contains only `hysteria2://` links extracted from the default list

## TODO
- Add more `Hysteria` & `xhttp` to `source-list.txt`.
- Add output files for additional proxy protocols
- Filter Russian servers by GeoIP DB
- Add a better local run helper or script wrapper

## Local usage
Run the local workflow simulation with:

```bash
./run-local.sh
```

## Contribution
You may suggest a source by sending a pull request.