
import socket
import struct
import sys
def run_server(port, ip):
    server_socket = socket.socket()
    server_socket.bind((ip, port))  # bind host address and port together
    server_socket.listen()
    while True:
        conn, address = server_socket.accept()
        en_leangth = conn.recv(4)
        leangth = struct.unpack('<i', en_leangth)
        en_messege = conn.recv(leangth[0])
        messege = en_messege.decode()
        print(messege)
        conn.close()
    server_socket.close()


def main():
    run_server(5553, "127.0.0.1")


if __name__ == '__main__':
    main()