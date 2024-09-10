import os
import time
import socket
import struct
import threading
from _thread import *


import sys

def connect_to_client(conn, addrs):
    en_leangth = conn.recv(4)
    leangth = struct.unpack('<i', en_leangth)
    en_messege = conn.recv(leangth[0])
    messege = en_messege.decode()
    print(f" {messege} from ip {addrs} and thread {os.getpid()}")
    conn.close()

def run_server(port, ip):
    server_socket = socket.socket()
    server_socket.bind((ip, port)) # bind host address and port together
    server_socket.listen()
    try:
        while True:
            conn, addrs = server_socket.accept()
            client_thread = threading.Thread(target=connect_to_client, args=(conn, addrs))
            client_thread.start()


    except KeyboardInterrupt:
        server_socket.close()


def main():
    run_server(8888, "0.0.0.0")


if __name__ == '__main__':
    main()
