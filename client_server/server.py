
import threading
from listener import Listener
from card import Card
from CardManager import CardManager


def save_to_database(card: Card):
    print("Received card.")
    manager = CardManager('./database')
    manager.save(card)
    print(f"Saved card to path ./database/{card.creator}/{card.name}")
def run_server(port, ip):
    with Listener("127.0.0.1", 8745) as listener:
        while True:
            with listener.accept() as conn:
                client_thread = threading.Thread(target=save_to_database(conn.receive_message()), args=())
                client_thread.start()

def main():
    run_server(8745, "0.0.0.0")


if __name__ == '__main__':
    main()
