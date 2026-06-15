from __future__ import annotations

import socket
import sys


def free_port(host: str, start: int, attempts: int = 100) -> int:
    bind_host = "127.0.0.1" if host in {"", "0.0.0.0", "::"} else host
    family = socket.AF_INET6 if ":" in bind_host else socket.AF_INET
    for port in range(start, start + attempts):
        with socket.socket(family, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((bind_host, port))
            except OSError:
                continue
            return port
    raise SystemExit(f"No free port found from {start} to {start + attempts - 1}.")


if __name__ == "__main__":
    host_arg = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port_arg = int(sys.argv[2]) if len(sys.argv) > 2 else 8765
    print(free_port(host_arg, port_arg))
