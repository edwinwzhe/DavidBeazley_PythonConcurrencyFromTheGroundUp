# Performance test -
# run fib_service.py first then this -
# slow request - running more of this slow down by the same factor - the GIL

import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 25000))

while True:
    start = time.time()
    sock.send(b'30')
    resp = sock.recv(100)

    end = time.time()
    print(end - start)