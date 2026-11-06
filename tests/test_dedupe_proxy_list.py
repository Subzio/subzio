import base64
import json
import unittest

from scripts.dedupe_proxy_list import canonical_key, deduplicate


class DeduplicateProxyListTests(unittest.TestCase):
    def test_ignores_fragment_and_query_order(self):
        entries = [
            "vless://id@example.com:443?security=tls&type=ws&path=%2Fedge#one\n",
            "vless://id@example.com:443?path=%2Fedge&type=ws&security=tls#two\n",
        ]
        self.assertEqual(list(deduplicate(entries)), entries[:1])

    def test_preserves_distinct_transport_and_tls_options(self):
        entries = [
            "vless://id@example.com:443?security=tls&type=ws&fp=firefox\n",
            "vless://id@example.com:443?security=tls&type=ws&fp=ios\n",
            "vless://id@example.com:443?security=tls&type=grpc&fp=firefox\n",
        ]
        self.assertEqual(list(deduplicate(entries)), entries)

    def test_normalizes_hostname_case_and_hysteria_scheme_alias(self):
        self.assertEqual(
            canonical_key("hy2://secret@EXAMPLE.com:443?sni=front.example"),
            canonical_key("hysteria2://secret@example.com:443?sni=front.example"),
        )

    def test_ignores_vmess_display_name_but_keeps_configuration(self):
        first = {"add": "example.com", "port": "443", "id": "user", "ps": "first"}
        second = {**first, "ps": "second"}

        def link(config):
            payload = base64.urlsafe_b64encode(
                json.dumps(config).encode()
            ).decode().rstrip("=")
            return f"vmess://{payload}\n"

        entries = [link(first), link(second), link({**second, "net": "ws"})]
        self.assertEqual(list(deduplicate(entries)), [entries[0], entries[2]])

    def test_keeps_malformed_lines_and_removes_only_exact_repeat(self):
        entries = ["not a proxy\n", "not a proxy\n", "also not a proxy\n"]
        self.assertEqual(
            list(deduplicate(entries)), [entries[0], entries[2]]
        )


if __name__ == "__main__":
    unittest.main()
