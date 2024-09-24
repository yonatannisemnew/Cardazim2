import argparse
import socket
import struct
from connection import Connection
from card import Card

def send_data(server_ip, server_port, card_name, card_creator, card_riddle, card_solution, image_path):
    '''
    Send data to server in address (server_ip, server_port).
    '''
    card = Card.create_from_path(card_name, card_creator, image_path, card_riddle, card_solution)
    card.image.encrypt(card.solution)
    with Connection.connect(server_ip, server_port) as conn:
        conn.send_message(card)
def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('card_name', type=str,
                        help='card name')
    parser.add_argument('card_creator', type=str,
                        help='card creator')
    parser.add_argument('card_riddle', type=str,
                        help='card riddle')
    parser.add_argument('card_solution', type=str,
                        help='card solution')
    parser.add_argument('image_path', type=str,
                        help='image_path')

    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        # send_data(args.server_ip, args.server_port, args.data)
        send_data(args.server_ip, args.server_port, args.card_name, args.card_creator, args.card_riddle, args.card_solution, args.image_path)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    main()
