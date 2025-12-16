import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Tuple


class HealthHandler(BaseHTTPRequestHandler):
    """Simple HTTP handler that returns JSON payloads for any GET request."""

    server_version = "gitops-devops-pipeline/1.0"

    def _send_response(self, payload: dict, status_code: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802  # linting: keep BaseHTTPRequestHandler signature
        if self.path not in {"/", "/health"}:
            self._send_response({"status": "not_found", "path": self.path}, status_code=404)
            return

        self._send_response({
            "service": "gitops-devops-pipeline",
            "status": "ok",
            "path": self.path,
        })



def run_server(host: str, port: int) -> Tuple[str, int]:
    server = HTTPServer((host, port), HealthHandler)
    print(f"Starting HTTP server on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return host, port


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    run_server(host, port)
