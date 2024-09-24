
import threading
from listener import Listener
def run_server(port, ip):
    with Listener("127.0.0.1", 8765) as listener:
        while True:
            with listener.accept() as conn:
                client_thread = threading.Thread(target=print(conn.receive_message()), args=())
                client_thread.start()

def main():
    run_server(8765, "0.0.0.0")


if __name__ == '__main__':
    main()
