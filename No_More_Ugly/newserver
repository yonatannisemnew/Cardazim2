import os
import time
import socket
import struct
import threading
from listener import  Listener


def connect_to_client(conn, addrs):
    en_leangth = conn.recv(4)
    leangth = struct.unpack('<i', en_leangth)
    en_messege = conn.recv(leangth[0])
    messege = en_messege.decode()
    print(f" {messege} from ip {addrs} ")
    time.sleep(5)
    conn.close()
    print(f"connection from {threading.get_ident()} is closed")

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
