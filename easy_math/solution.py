"""
[Problem]

Given an IP address HOST and port PORT, connect to the server (hint: use nc [HOST]
[PORT]) to get a math problem: given 2 numbers and a result, fill in (send back)
the operation +, -, *, or / so that num1 op num2 = result. If the calculation can
be solved using multiple operations, answer either + or *. Repeat 1000 times to
get the flag.
"""

import socket

HOST = ""
PORT = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.recv(4096)

operations = ["+", "-", "*", "/"]

for _ in range(1000):
    data = s.recv(1024).decode()

    _, eq = data.strip("\n").split(": ")

    # equation is in the form of "number1 _ number2 = result"
    eq = eq.replace("=", "==")
    for op in operations:
        if eval(eq.replace("_", op)):
            s.send(op.encode())
            continue

flag = s.recv(1024).decode()
s.close()

print(flag)
