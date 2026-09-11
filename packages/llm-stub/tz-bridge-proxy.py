"""TCP proxy to the host TensorZero gateway (deployed separately here)."""
import socket
import threading

LISTEN_PORT = 3000
UPSTREAM = ("169.254.1.2", 3000)  # podman host.containers.internal inside the node


def pipe(src, dst):
    try:
        while True:
            data = src.recv(65536)
            if not data:
                break
            dst.sendall(data)
    except OSError:
        pass
    finally:
        try:
            dst.shutdown(socket.SHUT_WR)
        except OSError:
            pass


def handle(conn):
    try:
        up = socket.create_connection(UPSTREAM, timeout=5)
    except OSError as e:
        print("upstream connect failed:", e, flush=True)
        conn.close()
        return
    threading.Thread(target=pipe, args=(conn, up), daemon=True).start()
    threading.Thread(target=pipe, args=(up, conn), daemon=True).start()


server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", LISTEN_PORT))
server.listen(64)
print("tz-bridge listening on", LISTEN_PORT, "->", UPSTREAM, flush=True)
while True:
    conn, _ = server.accept()
    threading.Thread(target=handle, args=(conn,), daemon=True).start()
