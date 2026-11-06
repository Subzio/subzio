#!/usr/bin/env python3
import base64
import json
import sys
from urllib.parse import unquote, parse_qsl, urlsplit


def _query_key(query):
    grouped = {}
    for key, value in parse_qsl(query, keep_blank_values=True):
        grouped.setdefault(key, []).append(value)
    return tuple((key, tuple(grouped[key])) for key in sorted(grouped))


def _host_key(hostname):
    if ":" in hostname:
        return hostname.lower()
    return hostname.encode("idna").decode("ascii").lower()


def canonical_key(line):
    try:
        uri = urlsplit(line)
        scheme = uri.scheme.lower()
        if not scheme or not uri.netloc:
            return ("line", line)

        if scheme == "vmess":
            payload = uri.netloc
            decoded = base64.urlsafe_b64decode(
                payload + "=" * (-len(payload) % 4)
            )
            config = json.loads(decoded)
            if not isinstance(config, dict):
                return ("line", line)
            config.pop("ps", None)
            return (
                "vmess",
                json.dumps(config, sort_keys=True, separators=(",", ":")),
                _query_key(uri.query),
            )

        scheme = "hysteria2" if scheme == "hy2" else scheme
        hostname = uri.hostname
        if hostname is None:
            return ("line", line)
        port = uri.port
        userinfo = uri.netloc.rsplit("@", 1)[0] if "@" in uri.netloc else ""
        authority = (
            unquote(userinfo),
            _host_key(hostname),
            port,
        )
        return (
            scheme,
            authority,
            uri.path,
            _query_key(uri.query),
        )
    except (UnicodeError, ValueError, json.JSONDecodeError):
        return ("line", line)


def deduplicate(lines):
    seen = set()
    for line in lines:
        key = canonical_key(line.rstrip("\r\n"))
        if key not in seen:
            seen.add(key)
            yield line


if __name__ == "__main__":
    sys.stdout.writelines(deduplicate(sys.stdin))
