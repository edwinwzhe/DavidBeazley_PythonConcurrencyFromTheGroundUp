# this version of the server uses concurrent.futures
# to off load works to a pool, running a heavy load task
# e.g. nc localhost 25000 -> 40, no longer significantly
# drops the performance of quick tasks.

import socket
from fib import fib
from threading import Thread
from concurrent.futures import ProcessPoolExecutor as Pool


pool = Pool(4)


def fib_server(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)

    while True:
        client, addr = sock.accept()
        print('Connection from {}'.format(addr))
        Thread(target=fib_handler, args=(client,)).start()


def fib_handler(client):
    while True:
        req = client.recv(100)
        if not req:
            break

        n = int(req)
        future = pool.submit(fib, n)
        result = future.result()

        resp = str(result).encode('ascii') + b'\n'
        client.send(resp)

    print('Closed')


fib_server(('', 25000))


