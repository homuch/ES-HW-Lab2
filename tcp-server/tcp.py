#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from vpython import *

# import cv2
from math import pi
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import socket
import time
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# os.environ["QT_QPA_PLATFORM"] = "xcb"
# export OPENCV_VIDEOIO_PRIORITY=GTK
# os.environ["OPENCV_VIDEOIO_PRIORITY"] = "GTK"
# os.environ["QT_QPA_PLATFORM"] = "offscreen"


# Create an OpenCV window
# cv2.namedWindow("Dynamic Image", cv2.WINDOW_NORMAL)


# matplotlib.use('QtAgg')  # Use TkAgg backend


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


# scene = canvas(title="3D Vector Visualization", width=800,
#                height=600, center=vector(0, 0, 0))
# scene.autoscale = True
# # Create an arrow for the vector
# vector_arrow = arrow(pos=vector(0, 0, 0), axis=vector(
#     3, 2, 1), shaftwidth=10, color=color.red)
# # Create a flat box with normal vector vector_arrow
# bx = cylinder(pos=vector(0, 0, 0), axis=vector(0, 0, 1),
#               radius=500, color=color.blue)


# Parameters
window_size = 50  # Number of data points in the sliding window

# Initialize data
x_data = list(range(window_size))
y_datalist = [0] * window_size
y_data2_list = [0] * window_size

fig, ax = plt.subplots()
line, = ax.plot([], [], 'b-', lw=2)
line2, = ax.plot([], [], 'r-', lw=2)

# Set axis limits
ax.set_xlim(0, 20)  # Adjust to fit the sliding window
# Adjust to fit the data range
ax.set_ylim(-100+pi**2*100+100, 100+pi**2*100+100)

# Update function
y_data_g = 0
y_data_g2 = 0


def get_data():
    return y_data_g, y_data_g2


def update(frame):
    y_data1, y_data2 = get_data()
    # x_data.append(frame / 10)
    y_datalist.append(y_data1)
    y_data2_list.append(y_data2)

    # minimum = min(min(y_datalist), min(y_data2_list))
    # maximum = max(max(y_datalist), max(y_data2_list))

    # ax.set_ylim(minimum, maximum)  # Adjust the y-axis dynamically

    # Apply sliding window
    # if len(x_data) > window_size:
    #     # x_data.pop(0)
    y_datalist.pop(0)
    y_data2_list.pop(0)

    line.set_data(x_data, y_datalist)
    line2.set_data(x_data, y_data2_list)
    # ax.set_xlim(x_data[0], x_data[-1])  # Adjust the x-axis dynamically
    return line,


# Animation
# ani = FuncAnimation(fig, update, frames=range(200), interval=50, blit=True)

# plt.show()


# Function to update the vector


# def update_vector(x, y, z):
#     vector_arrow.axis = vector(x, y, z)
#     magnitude = (x**2 + y**2 + z**2)**0.5
#     if magnitude != 0:
#         x /= magnitude
#         y /= magnitude
#         z /= magnitude
#     bx.axis = vector(x, y, z)


HOST = '192.168.63.188'
PORT = 8002

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)

# img = mpimg.imread('test.png')
# imgplot = plt.imshow(img)
# plt.show(block=False)

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...')


while True:
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
        y_data_g = x
        y_data_g2 = y
        update(0)
        plt.savefig('test.png')
        # plt.(block=False)
        print('x: %d, y: %d, z: %d' % (x, y, z))

        # Load the saved image
        # image = cv2.imread("test.png")

        # # Display the image in the OpenCV window
        # cv2.imshow("Dynamic Image", image)
        # Convert to RGB for Matplotlib
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # plt.imshow(image)
        # plt.show()
        # plt.close()
        # img = mpimg.imread('test.png')
        # imgplot = plt.imshow(img)
        # plt.show(block=False)

        # # Initial vector
        # update_vector(x, y, z)
# cv2.destroyAllWindows()
# Get input from server
s.close()
