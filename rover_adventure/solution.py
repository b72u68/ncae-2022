"""
[Problem]

Connect to 172.18.64.4:5225 or use netcat nc 172.18.64.4 5225 to receive a 71
columns x 51 rows grid showing the path that the rover has to take. "R" represents
the current location of the rover and "E" represents the end (goal). The rover
can only go through blank places denoted by spaces (" "). Send back a series of
coordinates on the path from "R" to "E" to receive the flag.

Note:
    - Format: (2,3),(4,5)
    - Format: (row,column)
    - From top to bottom.
    - The answer contains coordinates of the corners in the path and point "E".
    - Submit the full path.
    - Repeat the process above 1000 times to receive the flag.
"""

from pwn import *

HOST = "172.18.64.4"
PORT = 5225

conn = remote(HOST, PORT)
conn.recv(4096)

for _ in range(1001):
    path = []
    conn.recvuntil('\n')
    for row in range(51):
        line = conn.recvuntil('\n').decode('utf-8', 'ignore').strip('\n')
        rows = []
        for col, c in enumerate(line):
            if c == "R":
                path.append((row, col))
                rows.append((row, col))
            elif c == " ":
                rows.append((row, col))
            elif c == "E":
                path.append((row, col))
                rows.append((row, col))
                break
        if path:
            _, lcol = path[-1]
            if rows[0][1] != lcol:
                rows = rows[::-1]
            if len(rows) > 1:
                path.extend([rows[0], rows[-1]])
    path.pop(0)
    data = ",".join([f"({r},{c})" for r, c in path])
    conn.send(data.encode())

print(conn.recv(4096).decode('utf-8', 'ignore'))
conn.close()


"""
[Credit]

This solution uses pwntools, a library built on top of socket to solve this
challenge. The provided VMs did not have pip, and we weren't able to use the
package manager to install this package. The hack through this was using
get-pip.py in this link: https://pip.pypa.io/en/stable/installation/.

Thank you Wyatt for showing pwntools library!
"""
