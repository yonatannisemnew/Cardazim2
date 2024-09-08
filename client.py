import argparse
import sys
import socket
import struct


def send_data(server_ip, server_port, data):
    '''
    Send data to server in address (server_ip, server_port).
    '''
    client_socket = socket.socket()  # instantiate
    client_socket.connect((server_ip, server_port))  # connect to the server
    en_data = data.encode()
    size = len(en_data)
    en_size = struct.pack('<i', size)
    messege = en_size + en_data
    client_socket.send(messege)  # send message
    client_socket.close()  # close the connection


###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('data', type=str,
                        help='the data')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        # send_data(args.server_ip, args.server_port, args.data)
        send_data(args.server_ip, args.server_port, args.data)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1
    
def foo() :
    ip = '172.20.10.3'
    port = 1234
    while True:
        send_data(ip, port, "sddssdfffsdfdsffdsfsfdfdsfdsfjdsfijdshfshdfsfhsdfijdhfdijsfhdsjifhsdijfhdisjfhdsjifhsdihsdighsdijghdsjighsdijghjisghohsfoighdiofshgodfghosdhgosdfhgoidsfhgoidshgodsfighodisfghodfshgdsofghdsofhgoshgosifdhgoisfdhgoidfghoijsdghijodfhgiosfhgighdsfijoghgihdsoghoidfsgdhfgohgsdoghodshgdoifjghodsihgodshgosidhgsdfoig")
if __name__ == '__main__':
    main()