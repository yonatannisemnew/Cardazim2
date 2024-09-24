import socket
from card import Card
class Connection:
    def __init__(self, connection: socket.socket):
        self.sock = connection
    def __repr__(self):
        sip, sport = self.sock.getsockname()
        pip, pport = self.sock.getpeername()
        r_string  = f"<Connection from {pip}:{pport} to {sip}:{sport}>"
        #neads to find the client port
        return r_string

    def send_message(self, card: Card):

        self.sock.send(card.serialize())

    def receive_message(self):

        serialized = b''
        while True:
            data = self.sock.recv(1024)
            serialized+=data
            if not data:
                break

        self.close()
        return Card.deserialize(serialized)

    @classmethod
    def connect(cls, ip, port):
        client_socket = socket.socket()  # instantiate
        client_socket.connect((ip, port))
        return cls(client_socket)

    def __enter__(self):
        return self
    def __exit__(self,*args):
        self.sock.close()
    def close(self):
        self.sock.close()

    def listener(self, ip, port):
        s_socket = socket.socket()
        s_socket.bind()

def main():
    with Connection.connect("127.0.0.1", 8765) as conn:

        conn.send_message(b"it works!!")

if __name__ == '__main__':
    main()
