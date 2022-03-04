#!/usr/bin/env python3

import math

import matplotlib.pyplot as plt
import numpy as np


class Light:
    def __init__(self, x, y, z, θ, wavelength, ppf):
        self.x = x
        self.y = y
        self.z = z
        self.θ = θ
        self.wavelength = wavelength
        self.ppf = ppf


def angle_to(x0, y0, z0, x1, y1, z1):
    '''
        `A / sin a = B / sin b`
        `a` is the right-angle (90°) so `sin a = 1`
        Which leaves us with `A = B / sin b` -> `asin(B/A) = b
    '''
    dx = (x1 - x0) ** 2
    dy = (y1 - y0) ** 2
    dz = (z1 - z0) ** 2
    return math.asin(math.sqrt(dx + dy) / math.sqrt(dx + dy + dz))

def area_of_cone_at_point(x0, y0, z0, x1, y1, z1, θ1):
    ''' 2πr²(1 - cos θ) '''
    dx = (x1 - x0) ** 2
    dy = (y1 - y0) ** 2
    dz = (z1 - z0) ** 2

    return 2 * math.pi * (dx + dy + dz) * (1 - math.cos(θ1))

def ppf_at_point(x, y, z, light):
    if angle_to(light.x, light.y, light.z, x, y, z) > light.θ:
        return 0
    return light.ppf / area_of_cone_at_point(x, y, z, light.x, light.y, light.z, light.θ) ** 1


def distribute_lights(dist):
    lights = []

    for i in dist:
        for j in dist:
            lights.append(Light(0.5 + i / 100, 0.5 + j / 100, 0.5, math.radians(60), 660, 10))
    return lights


def calculate_map(lights):
    data = np.zeros((200, 200))
    for i in range(len(data)):
        for j in range (len(data[i])):
            for l in lights:
                # if (int(l.x * 100) == i and int(l.y * 100) == j):
                #     data[i][j] = 0
                #     break
                data[i][j] += ppf_at_point(i / 100, j / 100, 0, l)
    return data

data_1 = calculate_map(distribute_lights([10, 25, 40, 60, 75, 90]))
# data_1 = calculate_map(distribute_lights([50]))
data_2 = calculate_map(distribute_lights([10, 18, 35, 65, 82, 90]))

plt.imshow(data_1)
plt.imshow(data_2)
# plt.plot(data_1[25], label='Uniform at 25cm')
# plt.plot(data_1[50], label='Uniform at 50cm')
# plt.plot(data_2[25], label='Optimized at 25')
# plt.plot(data_2[50], label='Optimized at 50')
plt.legend()
plt.show()