import pytest
import struct
import socket
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

NUM = 4
class MockSocket:
    sent_data = []
    addr = None

    def connect(self, addr):
        MockSocket.addr = addr

    def send(self, data: bytes):
        MockSocket.sent_data.append(data)

    def recv(self, data):
        return data

    def close(self):
        pass


@pytest.fixture
def mock_socket(monkeypatch):
    monkeypatch.setattr(socket, 'socket', MockSocket)


def test_run_client(mock_socket):
    from client import send

    MockSocket.sent_data = []
    send('127.0.0.1', 8080, b"hello")

    #assert MockSocket.addr == ('127.0.0.1', 8080)
    #assert MockSocket.sent_data[0] == b"hello"
