import base64
import json
import tempfile
import unittest
from pathlib import Path

from scripts.check_alive import (
    build_config,
    build_legacy_xray_config,
    build_xray_config,
    parse_proxy,
    parse_xray_xhttp,
    _write_snapshot,
)


class ParseProxyTests(unittest.TestCase):
    def test_vless_reality_tcp(self):
        outbound = parse_proxy(
            "vless://user-id@example.com:443?security=reality"
            "&sni=front.example&pbk=public-key&sid=1234&type=tcp",
            1,
        )
        self.assertEqual(outbound["type"], "vless")
        self.assertEqual(outbound["uuid"], "user-id")
        self.assertEqual(outbound["tls"]["server_name"], "front.example")
        self.assertTrue(outbound["tls"]["reality"]["enabled"])
        self.assertNotIn("transport", outbound)

    def test_unsafe_fingerprint_uses_standard_tls_or_reality_default(self):
        tls = parse_proxy(
            "vless://user-id@example.com:443?security=tls&fp=unsafe",
            8,
        )
        reality = parse_proxy(
            "vless://user-id@example.com:443?security=reality"
            "&pbk=public-key&fp=unsafe",
            9,
        )
        self.assertNotIn("utls", tls["tls"])
        self.assertEqual(reality["tls"]["utls"]["fingerprint"], "chrome")

    def test_vless_websocket(self):
        outbound = parse_proxy(
            "vless://user-id@example.com:443?security=tls&type=ws"
            "&host=cdn.example&path=%2Fsocket",
            2,
        )
        self.assertEqual(
            outbound["transport"],
            {"type": "ws", "path": "/socket", "headers": {"Host": "cdn.example"}},
        )

    def test_xhttp_reality(self):
        outbound = parse_xray_xhttp(
            "vless://user-id@example.com:443?security=reality&type=xhttp"
            "&sni=front.example&pbk=public-key&sid=1234&path=%2Fedge&mode=packet-up",
            7,
        )
        self.assertEqual(outbound["streamSettings"]["network"], "xhttp")
        self.assertEqual(
            outbound["streamSettings"]["xhttpSettings"],
            {"path": "/edge", "mode": "packet-up"},
        )
        self.assertEqual(
            outbound["streamSettings"]["realitySettings"]["serverName"],
            "front.example",
        )

    def test_vmess_websocket(self):
        vmess = {
            "add": "example.com",
            "port": "443",
            "id": "user-id",
            "aid": "0",
            "net": "ws",
            "host": "cdn.example",
            "path": "/socket",
            "tls": "tls",
        }
        encoded = base64.urlsafe_b64encode(json.dumps(vmess).encode()).decode().rstrip("=")
        outbound = parse_proxy(f"vmess://{encoded}", 3)
        self.assertEqual(outbound["type"], "vmess")
        self.assertEqual(outbound["transport"]["type"], "ws")
        self.assertEqual(outbound["tls"]["server_name"], "cdn.example")

    def test_trojan(self):
        outbound = parse_proxy(
            "trojan://secret@example.com:443?sni=front.example&type=grpc&serviceName=svc",
            4,
        )
        self.assertEqual(outbound["password"], "secret")
        self.assertEqual(outbound["transport"]["service_name"], "svc")
        self.assertEqual(outbound["tls"]["server_name"], "front.example")

    def test_hysteria2(self):
        outbound = parse_proxy(
            "hy2://secret@example.com:443?sni=front.example"
            "&obfs=salamander&obfs-password=hidden",
            5,
        )
        self.assertEqual(outbound["type"], "hysteria2")
        self.assertEqual(outbound["password"], "secret")
        self.assertEqual(outbound["obfs"]["password"], "hidden")

    def test_hysteria2_password_containing_colon(self):
        outbound = parse_proxy(
            "hysteria2://user:secret@example.com:443",
            6,
        )
        self.assertEqual(outbound["password"], "user:secret")

    def test_build_config_routes_each_inbound_to_its_proxy(self):
        config = build_config(
            [
                "trojan://secret@one.example:443",
                "trojan://secret@two.example:443",
            ],
            1,
            [24001, 24002],
        )
        self.assertEqual(config["inbounds"][1]["listen_port"], 24002)
        self.assertEqual(config["route"]["rules"][0]["outbound"], "proxy-1")
        self.assertEqual(config["route"]["rules"][1]["outbound"], "proxy-2")

    def test_build_xray_config_routes_each_inbound_to_its_proxy(self):
        config = build_xray_config(
            [
                "vless://id1@one.example:443?security=tls&type=xhttp",
                "vless://id2@two.example:443?security=tls&type=xhttp",
            ],
            1,
            [24001, 24002],
        )
        self.assertEqual(config["inbounds"][1]["port"], 24002)
        self.assertEqual(config["routing"]["rules"][0]["outboundTag"], "proxy-1")
        self.assertEqual(config["routing"]["rules"][1]["outboundTag"], "proxy-2")

    def test_build_legacy_xray_config_uses_splithttp(self):
        config = build_legacy_xray_config(
            ["vless://id@one.example:443?security=none&type=xhttp"],
            1,
            [24001],
        )
        self.assertEqual(config["outbounds"][0]["streamSettings"]["network"], "splithttp")
        self.assertIn("splithttpSettings", config["outbounds"][0]["streamSettings"])

    def test_rejects_unsupported_scheme(self):
        with self.assertRaisesRegex(ValueError, "Unsupported proxy scheme"):
            parse_proxy("ss://secret@example.com:443", 1)

    def test_snapshot_replaces_old_contents_with_empty_successful_result(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "ALIVE.txt"
            path.write_text("old-entry\n", encoding="utf-8")
            _write_snapshot(path, [])
            self.assertEqual(path.read_text(encoding="utf-8"), "")
            self.assertEqual(list(Path(temp_dir).iterdir()), [path])


if __name__ == "__main__":
    unittest.main()
