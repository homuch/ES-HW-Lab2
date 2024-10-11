#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from vpython import *
import socket
import time


def convert_to_hex(data):
    x = data[2:4]+data[0:2]
    y = data[6:8]+data[4:6]
    z = data[10:12]+data[8:10]
    # hex to signed 16-bits integer
    # signed !!!
    x = int(x, 16) - 0x10000 if int(x, 16) > 0x7fff else int(x, 16)
    y = int(y, 16) - 0x10000 if int(y, 16) > 0x7fff else int(y, 16)
    z = int(z, 16) - 0x10000 if int(z, 16) > 0x7fff else int(z, 16)

    return x, y, z


scene = canvas(title="3D Vector Visualization", width=800,
               height=600, center=vector(0, 0, 0))
scene.autoscale = True
# Create an arrow for the vector
vector_arrow = arrow(pos=vector(0, 0, 0), axis=vector(
    3, 2, 1), shaftwidth=10, color=color.red)
# Create a flat box with normal vector vector_arrow
bx = cylinder(pos=vector(0, 0, 0), axis=vector(0, 0, 1),
              radius=500, color=color.blue)


# Function to update the vector


def update_vector(x, y, z):
    vector_arrow.axis = vector(x, y, z)
    magnitude = (x**2 + y**2 + z**2)**0.5
    if magnitude != 0:
        x /= magnitude
        y /= magnitude
        z /= magnitude
    bx.axis = vector(x, y, z)


HOST = '192.168.9.187'
PORT = 8002

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...')

while True:
    rate(10)
    conn, addr = s.accept()
    print('connected by ' + str(addr))

    while True:
        # outdata = input('Enter response: ')
        outdata = 'trash'
        time.sleep(0.1)
        conn.send(outdata.encode())

        indata = conn.recv(1024)
        if len(indata) == 0:  # connection closed
            conn.close()
            print('client closed connection.')
            break
        receive = indata.hex()
        x, y, z = convert_to_hex(receive)
        print('x: %d, y: %d, z: %d' % (x, y, z))
        # Initial vector
        update_vector(x, y, z)

        # Get input from server
s.close()
