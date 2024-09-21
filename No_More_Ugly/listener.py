from connection import Connection
import socket
class Listener:
    def __init__(self, ip, port, backlog = 100):
        s_socket = socket.socket()
        s_socket.bind((ip, port))
        self.sock = s_socket
        self.backlog = backlog
    def __repr__(self):
        """
        string with server info
        """
        sip, sport = self.sock.getsockname()
        return f"Listener(port={sport}, host={sip}, backlog={self.backlog})"

    def start(self):
        """
        starts to listen to connections
        """
        self.sock.listen()
    def stop(self):
        """
        stop listening to connections
        """
        self.sock.close()

    def accept(self):
        conn, addrs = self.sock.accept()
        return Connection(conn)

    def __enter__(self):
        self.start()
        return self
    def __exit__(self, *args):
        self.sock.close()

def main():
    with Listener("127.0.0.1", 8765) as listener:
        listener.start()
        with listener.accept() as conn:
            print(conn.receive_message())

if __name__ == "__main__":
    main()




