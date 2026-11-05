#!/usr/bin/env python3
import argparse
import asyncio
import base64
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit


CHECK_URL = "https://www.gstatic.com/generate_204"
BATCH_SIZE = 100
PROBE_TIMEOUT_SECONDS = 12


def _query_value(query: dict[str, list[str]], key: str, default: str = "") -> str:
    return query.get(key, [default])[0]


def _enabled(value: str) -> bool:
    return value.lower() in {"1", "true", "yes"}


def _tls_options(query: dict[str, list[str]], server_name: str, enabled: bool = True) -> dict:
    if not enabled:
        return {}

    tls = {
        "enabled": True,
        "server_name": _query_value(query, "sni", server_name),
        "insecure": _enabled(_query_value(query, "allowInsecure"))
        or _enabled(_query_value(query, "insecure")),
    }
    alpn = _query_value(query, "alpn")
    if alpn:
        tls["alpn"] = [item for item in alpn.split(",") if item]
    fingerprint = _query_value(query, "fp")
    if fingerprint == "unsafe":
        fingerprint = ""
    if _query_value(query, "security") == "reality" and not fingerprint:
        fingerprint = "chrome"
    if fingerprint:
        tls["utls"] = {"enabled": True, "fingerprint": fingerprint}
    if _query_value(query, "security") == "reality":
        public_key = _query_value(query, "pbk")
        if not public_key:
            raise ValueError("Reality proxy is missing pbk")
        tls["reality"] = {
            "enabled": True,
            "public_key": public_key,
            "short_id": _query_value(query, "sid"),
        }
    return tls


def _transport_options(query: dict[str, list[str]], network: str) -> dict | None:
    if network in {"", "tcp", "raw"}:
        return None

    if network == "ws":
        transport = {"type": "ws", "path": _query_value(query, "path", "/")}
        host = _query_value(query, "host")
        if host:
            transport["headers"] = {"Host": host}
        return transport

    if network in {"grpc", "gun"}:
        return {
            "type": "grpc",
            "service_name": _query_value(query, "serviceName")
            or _query_value(query, "service_name"),
        }

    if network in {"h2", "http"}:
        transport = {"type": "http"}
        host = _query_value(query, "host")
        if host:
            transport["host"] = [host]
        path = _query_value(query, "path")
        if path:
            transport["path"] = path
        return transport

    if network in {"httpupgrade", "xhttp"}:
        transport = {
            "type": network,
            "path": _query_value(query, "path", "/"),
        }
        host = _query_value(query, "host")
        if host:
            transport["host"] = host
        return transport

    raise ValueError(f"Unsupported transport: {network}")


def _parse_vmess(uri: str) -> tuple[str, dict]:
    encoded = uri.split("://", 1)[1].split("#", 1)[0].split("?", 1)[0]
    try:
        padded = encoded + "=" * (-len(encoded) % 4)
        details = json.loads(base64.urlsafe_b64decode(padded).decode("utf-8"))
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("Invalid VMess payload") from error

    server = details.get("add")
    try:
        port = int(details["port"])
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("VMess URI is missing a valid port") from error
    if not server or not details.get("id"):
        raise ValueError("VMess URI is missing server or UUID")

    query = {
        "sni": [str(details.get("sni") or details.get("host") or server)],
        "fp": [str(details.get("fp") or "")],
        "alpn": [str(details.get("alpn") or "")],
        "host": [str(details.get("host") or "")],
        "path": [str(details.get("path") or "")],
        "serviceName": [str(details.get("path") or "")],
    }
    tls_enabled = str(details.get("tls", "")).lower() in {"tls", "true", "1"}
    outbound = {
        "type": "vmess",
        "server": server,
        "server_port": port,
        "uuid": details["id"],
        "security": details.get("scy") or "auto",
        "alter_id": int(details.get("aid") or 0),
        "tls": _tls_options(query, server, tls_enabled),
    }
    transport = _transport_options(query, str(details.get("net") or "tcp").lower())
    if transport:
        outbound["transport"] = transport
    return str(server), outbound


def parse_proxy(uri: str, index: int) -> dict:
    scheme = uri.split("://", 1)[0].lower()
    if scheme == "vmess":
        server, outbound = _parse_vmess(uri)
    else:
        parsed = urlsplit(uri)
        query = parse_qs(parsed.query, keep_blank_values=True)
        server = parsed.hostname
        if not server:
            raise ValueError(f"{scheme} URI is missing a server")
        try:
            port = parsed.port
        except ValueError as error:
            raise ValueError(f"{scheme} URI has an invalid port") from error
        if port is None:
            raise ValueError(f"{scheme} URI is missing a port")

        outbound = {"server": server, "server_port": port}
        if scheme == "vless":
            if not parsed.username:
                raise ValueError("VLESS URI is missing a UUID")
            outbound.update({"type": "vless", "uuid": unquote(parsed.username)})
            flow = _query_value(query, "flow")
            if flow:
                outbound["flow"] = flow
            security = _query_value(query, "security")
            tls_enabled = security in {"tls", "reality"}
            outbound["tls"] = _tls_options(query, server, tls_enabled)
            packet_encoding = _query_value(query, "packetEncoding")
            if packet_encoding:
                outbound["packet_encoding"] = packet_encoding
        elif scheme == "trojan":
            password = unquote(parsed.password or parsed.username or "")
            if not password:
                raise ValueError("Trojan URI is missing a password")
            outbound.update({"type": "trojan", "password": password})
            outbound["tls"] = _tls_options(query, server)
        elif scheme in {"hysteria2", "hy2"}:
            password = unquote(parsed.username or "")
            if parsed.password is not None:
                password += ":" + unquote(parsed.password)
            password = password or _query_value(query, "auth")
            if not password:
                raise ValueError("Hysteria2 URI is missing a password")
            outbound.update({"type": "hysteria2", "password": password})
            outbound["tls"] = _tls_options(query, server)
            obfs = _query_value(query, "obfs")
            if obfs:
                outbound["obfs"] = {
                    "type": obfs,
                    "password": _query_value(query, "obfs-password"),
                }
        else:
            raise ValueError(f"Unsupported proxy scheme: {scheme}")

        transport = _transport_options(query, _query_value(query, "type"))
        if transport:
            outbound["transport"] = transport

    outbound["tag"] = f"proxy-{index}"
    return outbound


def build_config(lines: list[str], first_index: int, ports: list[int]) -> dict:
    outbounds = []
    inbounds = []
    rules = []
    for offset, line in enumerate(lines):
        index = first_index + offset
        outbound_tag = f"proxy-{index}"
        inbound_tag = f"check-{index}"
        outbounds.append(parse_proxy(line, index))
        inbounds.append(
            {
                "type": "socks",
                "tag": inbound_tag,
                "listen": "127.0.0.1",
                "listen_port": ports[offset],
            }
        )
        rules.append({"inbound": [inbound_tag], "outbound": outbound_tag})

    outbounds.append({"type": "direct", "tag": "direct"})
    return {
        "log": {"level": "error"},
        "inbounds": inbounds,
        "outbounds": outbounds,
        "route": {"rules": rules, "final": "direct"},
    }


def parse_xray_xhttp(uri: str, index: int) -> dict:
    parsed = urlsplit(uri)
    if parsed.scheme.lower() != "vless":
        raise ValueError("Xray XHTTP checker only supports VLESS")
    query = parse_qs(parsed.query, keep_blank_values=True)
    server = parsed.hostname
    try:
        port = parsed.port
    except ValueError as error:
        raise ValueError("XHTTP URI has an invalid port") from error
    if not server or port is None or not parsed.username:
        raise ValueError("XHTTP URI is missing its server, port, or UUID")

    user = {"id": unquote(parsed.username), "encryption": _query_value(query, "encryption", "none")}
    flow = _query_value(query, "flow")
    if flow:
        user["flow"] = flow

    stream_settings = {"network": "xhttp"}
    security = _query_value(query, "security", "none")
    if security == "reality":
        public_key = _query_value(query, "pbk")
        if not public_key:
            raise ValueError("Reality XHTTP URI is missing pbk")
        stream_settings["security"] = "reality"
        stream_settings["realitySettings"] = {
            "serverName": _query_value(query, "sni", server),
            "fingerprint": _query_value(query, "fp", "chrome"),
            "publicKey": public_key,
            "shortId": _query_value(query, "sid"),
            "spiderX": _query_value(query, "spx"),
        }
    elif security == "tls":
        tls_settings = {
            "serverName": _query_value(query, "sni", server),
            "allowInsecure": _enabled(_query_value(query, "allowInsecure"))
            or _enabled(_query_value(query, "insecure")),
        }
        alpn = _query_value(query, "alpn")
        if alpn:
            tls_settings["alpn"] = [item for item in alpn.split(",") if item]
        fingerprint = _query_value(query, "fp")
        if fingerprint:
            tls_settings["fingerprint"] = fingerprint
        ech = _query_value(query, "ech")
        if ech:
            tls_settings["echConfigList"] = ech
        stream_settings["security"] = "tls"
        stream_settings["tlsSettings"] = tls_settings
    elif security != "none":
        raise ValueError(f"Unsupported XHTTP security: {security}")

    xhttp_settings = {
        "path": _query_value(query, "path", "/"),
        "mode": _query_value(query, "mode", "auto"),
    }
    host = _query_value(query, "host")
    if host:
        xhttp_settings["host"] = host
    extra = _query_value(query, "extra")
    if extra:
        try:
            xhttp_settings["extra"] = json.loads(extra)
        except json.JSONDecodeError as error:
            raise ValueError("XHTTP extra parameter is not valid JSON") from error
    stream_settings["xhttpSettings"] = xhttp_settings

    return {
        "tag": f"proxy-{index}",
        "protocol": "vless",
        "settings": {
            "vnext": [
                {
                    "address": server,
                    "port": port,
                    "users": [user],
                }
            ]
        },
        "streamSettings": stream_settings,
    }


def build_xray_config(lines: list[str], first_index: int, ports: list[int]) -> dict:
    outbounds = []
    inbounds = []
    rules = []
    for offset, line in enumerate(lines):
        index = first_index + offset
        outbound_tag = f"proxy-{index}"
        inbound_tag = f"check-{index}"
        outbounds.append(parse_xray_xhttp(line, index))
        inbounds.append(
            {
                "tag": inbound_tag,
                "listen": "127.0.0.1",
                "port": ports[offset],
                "protocol": "socks",
                "settings": {"auth": "noauth", "udp": True},
            }
        )
        rules.append(
            {
                "type": "field",
                "inboundTag": [inbound_tag],
                "outboundTag": outbound_tag,
            }
        )

    outbounds.append({"protocol": "freedom", "tag": "direct"})
    return {
        "log": {"loglevel": "error"},
        "inbounds": inbounds,
        "outbounds": outbounds,
        "routing": {"rules": rules},
    }


def build_legacy_xray_config(lines: list[str], first_index: int, ports: list[int]) -> dict:
    config = build_xray_config(lines, first_index, ports)
    for outbound in config["outbounds"]:
        stream_settings = outbound.get("streamSettings")
        if not stream_settings:
            continue
        stream_settings["network"] = "splithttp"
        stream_settings["splithttpSettings"] = stream_settings.pop("xhttpSettings")
    return config


def _free_ports(count: int) -> list[int]:
    import socket

    ports = []
    sockets = []
    try:
        for _ in range(count):
            sock = socket.socket()
            try:
                sock.bind(("127.0.0.1", 0))
            except OSError:
                sock.close()
                raise
            ports.append(sock.getsockname()[1])
            sockets.append(sock)
    finally:
        for sock in sockets:
            sock.close()
    return ports


async def _listener_ready(port: int, process: subprocess.Popen) -> bool:
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        if process.poll() is not None:
            return False
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection("127.0.0.1", port), timeout=0.5
            )
            del reader
            writer.close()
            await writer.wait_closed()
            return True
        except (OSError, asyncio.TimeoutError):
            await asyncio.sleep(0.1)
    return False


async def _probe(port: int, index: int) -> bool:
    try:
        process = await asyncio.create_subprocess_exec(
            "curl",
            "--silent",
            "--show-error",
            "--output",
            os.devnull,
            "--write-out",
            "%{http_code}",
            "--max-time",
            str(PROBE_TIMEOUT_SECONDS),
            "--connect-timeout",
            "5",
            "--socks5-hostname",
            f"127.0.0.1:{port}",
            CHECK_URL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )
        stdout, _ = await process.communicate()
        success = process.returncode == 0 and stdout.decode().strip() == "204"
    except OSError as error:
        raise RuntimeError(f"Could not run curl for proxy entry {index}") from error
    print(f"Proxy entry {index}: {'alive' if success else 'failed'}")
    return success


async def _check_batch(binary: str, lines: list[str], first_index: int) -> list[str]:
    ports = _free_ports(len(lines))
    config = build_config(lines, first_index, ports)
    with tempfile.TemporaryDirectory(prefix="proxy-health-") as temp_dir:
        config_path = Path(temp_dir) / "config.json"
        log_path = Path(temp_dir) / "sing-box.log"
        config_path.write_text(json.dumps(config), encoding="utf-8")

        validation = subprocess.run(
            [binary, "check", "-c", str(config_path)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if validation.returncode:
            raise RuntimeError(f"sing-box rejected generated config:\n{validation.stderr}")

        with log_path.open("w+", encoding="utf-8") as log_file:
            process = subprocess.Popen(
                [binary, "run", "-c", str(config_path)],
                stdout=log_file,
                stderr=log_file,
            )
            try:
                ready = await asyncio.gather(
                    *(_listener_ready(port, process) for port in ports)
                )
                if not all(ready):
                    log_file.flush()
                    log_file.seek(0)
                    raise RuntimeError(
                        "sing-box failed to start all local listeners:\n"
                        + log_file.read()
                    )
                results = await asyncio.gather(
                    *(
                        _probe(port, first_index + offset)
                        for offset, port in enumerate(ports)
                    )
                )
            finally:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()

    return [line for line, success in zip(lines, results) if success]


async def _check_xray_batch(
    binary: str, lines: list[str], first_index: int, legacy: bool = False
) -> list[str]:
    ports = _free_ports(len(lines))
    config = (
        build_legacy_xray_config(lines, first_index, ports)
        if legacy
        else build_xray_config(lines, first_index, ports)
    )
    with tempfile.TemporaryDirectory(prefix="proxy-health-xray-") as temp_dir:
        config_path = Path(temp_dir) / "config.json"
        log_path = Path(temp_dir) / "xray.log"
        config_path.write_text(json.dumps(config), encoding="utf-8")

        validation = subprocess.run(
            [binary, "run", "-test", "-config", str(config_path)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if validation.returncode:
            details = validation.stderr.strip() or validation.stdout.strip()
            raise RuntimeError(f"Xray rejected generated config:\n{details}")

        with log_path.open("w+", encoding="utf-8") as log_file:
            process = subprocess.Popen(
                [binary, "run", "-config", str(config_path)],
                stdout=log_file,
                stderr=log_file,
            )
            try:
                ready = await asyncio.gather(
                    *(_listener_ready(port, process) for port in ports)
                )
                if not all(ready):
                    log_file.flush()
                    log_file.seek(0)
                    raise RuntimeError(
                        "Xray failed to start all local listeners:\n" + log_file.read()
                    )
                results = await asyncio.gather(
                    *(
                        _probe(port, first_index + offset)
                        for offset, port in enumerate(ports)
                    )
                )
            finally:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()

    return [line for line, success in zip(lines, results) if success]


def _check_direct_connection() -> None:
    result = subprocess.run(
        [
            "curl",
            "--silent",
            "--show-error",
            "--output",
            os.devnull,
            "--write-out",
            "%{http_code}",
            "--max-time",
            "15",
            "--noproxy",
            "*",
            CHECK_URL,
        ],
        capture_output=True,
        text=True,
        timeout=20,
    )
    if result.returncode or result.stdout.strip() != "204":
        raise RuntimeError(
            "Direct health-check endpoint preflight failed "
            f"(curl exit {result.returncode}, HTTP {result.stdout.strip() or 'none'}): "
            f"{result.stderr.strip()}"
        )


def _read_proxy_lines(path: Path) -> list[str]:
    lines = [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not lines:
        raise ValueError(f"Proxy source list is empty: {path}")
    return lines


async def check_proxies(
    binary: str, xray_binary: str, legacy_xray_binary: str, lines: list[str]
) -> list[str]:
    _check_direct_connection()
    sing_box_lines = []
    xray_lines = []
    legacy_xhttp_lines = []
    for line in lines:
        proxy = parse_proxy(line, 0)
        if proxy.get("transport", {}).get("type") == "xhttp":
            query = parse_qs(urlsplit(line).query, keep_blank_values=True)
            if _query_value(query, "security", "none") in {"tls", "reality"}:
                xray_lines.append(line)
            else:
                legacy_xhttp_lines.append(line)
        else:
            sing_box_lines.append(line)

    alive = set()
    for checker, candidates in (
        (lambda batch, start: _check_batch(binary, batch, start), sing_box_lines),
        (lambda batch, start: _check_xray_batch(xray_binary, batch, start), xray_lines),
        (
            lambda batch, start: _check_xray_batch(
                legacy_xray_binary, batch, start, legacy=True
            ),
            legacy_xhttp_lines,
        ),
    ):
        for start in range(0, len(candidates), BATCH_SIZE):
            batch = candidates[start : start + BATCH_SIZE]
            if candidates is sing_box_lines:
                engine = "sing-box"
            elif candidates is xray_lines:
                engine = "Xray"
            else:
                engine = "legacy Xray"
            print(
                f"Checking {len(batch)} entries with {engine} "
                f"({start + 1}-{start + len(batch)} of {len(candidates)})"
            )
            alive.update(await checker(batch, start + 1))
    return [line for line in lines if line in alive]


def _write_snapshot(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)
            if lines:
                temp_file.write("\n".join(lines) + "\n")
            temp_file.flush()
            os.fsync(temp_file.fileno())
        os.replace(temp_path, path)
    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description="Rebuild the live proxy snapshot.")
    parser.add_argument("sing_box", help="Path to the sing-box executable")
    parser.add_argument("xray", help="Path to the Xray executable")
    parser.add_argument("legacy_xray", help="Path to legacy Xray XHTTP executable")
    parser.add_argument("source", type=Path, help="Combined proxy list")
    parser.add_argument("output", type=Path, help="ALIVE.txt output path")
    args = parser.parse_args()

    source_lines = _read_proxy_lines(args.source)
    # Parse every entry before probing so malformed or unsupported URIs cannot
    # silently make the published snapshot incomplete.
    for index, line in enumerate(source_lines, start=1):
        try:
            parse_proxy(line, index)
        except ValueError as error:
            raise ValueError(f"Invalid proxy entry {index}: {error}") from error

    alive = asyncio.run(
        check_proxies(args.sing_box, args.xray, args.legacy_xray, source_lines)
    )
    _write_snapshot(args.output, alive)
    print(f"Published {len(alive)} alive proxies from {len(source_lines)} entries")


if __name__ == "__main__":
    main()
