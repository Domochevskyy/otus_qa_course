import os
import socket
from http import HTTPStatus
from urllib.parse import urlparse

ADDRESS = ('127.0.0.1', 5000)


def main():
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0) as sock:
        print(f'Server started on {ADDRESS[0]}:{ADDRESS[1]}, pid: {os.getpid()}')
        sock.bind(ADDRESS)
        sock.listen(1)

        while True:
            print('Wait for client connection...')
            connected_socket, raddress = sock.accept()
            print(f'Connection from {raddress}')
            while True:
                response = connected_socket.recv(1024)
                text = response.decode('utf-8')
                splitted_text = text.split('\r\n')

                method, origin_form, http_version = splitted_text[0].split()
                query = urlparse(origin_form).query
                match query:
                    case '':
                        status_code, status_phrase = 200, 'OK'
                    case _:
                        h = HTTPStatus(int(query.split('=')[1]))
                        status_code, status_phrase = h.value, h.phrase

                started_line = f'{http_version} {status_code} {status_phrase}'
                headers = '\r\n'.join(text.split('\r\n')[1:])

                message = f'{started_line}\r\n\r\n' \
                          f'\nRequest Method: {method}' \
                          f'\nRequest Source: {raddress}' \
                          f'\nResponse Status: {status_code} {status_phrase}' \
                          f'\r\n' \
                          f'\n{headers}'.encode('utf-8')

                connected_socket.send(message)
                connected_socket.close()
                break


if __name__ == '__main__':
    main()
