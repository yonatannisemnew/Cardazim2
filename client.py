import argparse 
import sys



def send_data(server_ip, server_port, data):
    """
    send {data} to thse server in address (server_ip, server port)
    """
    pass

def get_args():
    pass

def main():
    """
    implementation of CLI and sending data to server

    """
    args = get_args()
    try:
        send_data(args.server_ip, args.server_port, args.data)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1