#!/usr/bin/env python3
"""
Serveur local pour le questionnaire IA.
- Sert les fichiers statiques sur http://localhost:8080
- Proxie les appels IA sur POST /api/proxy
  (évite le blocage CORS des APIs externes)

Usage :
    python3 server.py
    python3 server.py 8080          # port personnalisé
"""

import http.server
import json
import os
import sys
import urllib.request
import urllib.error
from http import HTTPStatus

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

ALLOWED_HOSTS = {
    "api.anthropic.com",
    "api.openai.com",
}

class ProxyHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        print(f"  {self.address_string()} — {format % args}")

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.NO_CONTENT)
        self._cors()
        self.end_headers()

    def do_POST(self):
        if self.path == "/api/proxy":
            self._handle_proxy()
        else:
            self.send_error(HTTPStatus.NOT_FOUND)

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _handle_proxy(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            req_data = json.loads(body)
        except json.JSONDecodeError:
            self.send_error(HTTPStatus.BAD_REQUEST, "JSON invalide")
            return

        target_url = req_data.get("url", "")
        headers    = req_data.get("headers", {})
        payload    = req_data.get("body", {})

        # Sécurité : n'autoriser que les hôtes connus
        from urllib.parse import urlparse
        host = urlparse(target_url).hostname or ""
        # Autoriser aussi les hôtes compatibles (Mistral, Groq, etc.)
        if not any(target_url.startswith(f"https://{h}") for h in ALLOWED_HOSTS) \
           and not target_url.startswith("https://"):
            self.send_error(HTTPStatus.FORBIDDEN, f"Hôte non autorisé : {host}")
            return

        encoded = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
        headers["Content-Length"] = str(len(encoded))
        # Retirer le header browser-only inutile côté serveur
        headers.pop("anthropic-dangerous-direct-browser-access", None)

        req = urllib.request.Request(target_url, data=encoded, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req) as resp:
                resp_body = resp.read()
                self.send_response(resp.status)
                self._cors()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(resp_body)
        except urllib.error.HTTPError as e:
            err_body = e.read()
            self.send_response(e.code)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(err_body)
        except urllib.error.URLError as e:
            self.send_error(HTTPStatus.BAD_GATEWAY, str(e.reason))


if __name__ == "__main__":
    os.chdir(DIRECTORY)
    with http.server.ThreadingHTTPServer(("", PORT), ProxyHandler) as httpd:
        print(f"\n  Questionnaire IA — serveur local")
        print(f"  ➜  http://localhost:{PORT}/index.html\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  Serveur arrêté.")
