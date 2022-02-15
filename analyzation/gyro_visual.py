import pygame
import numpy as np
from math import *
import time
import scipy.integrate as integrate

from matplotlib.font_manager import json_dump, json_load

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 600
pygame.display.set_caption("3D projection in pygame!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

scale = 100

circle_pos = [WIDTH / 2, HEIGHT / 2]  # x, y

angle = 0

points = []

# all the cube vertices
points.append(np.matrix([-1, -1, 1]))
points.append(np.matrix([1, -1, 1]))
points.append(np.matrix([1, 1, 1]))
points.append(np.matrix([-1, 1, 1]))
points.append(np.matrix([-1, -1, -1]))
points.append(np.matrix([1, -1, -1]))
points.append(np.matrix([1, 1, -1]))
points.append(np.matrix([-1, 1, -1]))

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])

projected_points = [
    [n, n] for n in range(len(points))
]


def connect_points(i, j, points):
    pygame.draw.line(
        screen, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]))


##################


data = json_load("flightdata48.json")["imu"]

##################
clock = pygame.time.Clock()
v = 0

for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()

preset = np.matrix([
    [1, 0, 0],
    [0, cos(np.pi / 4), -sin(np.pi / 4)],
    [0, sin(np.pi / 4), cos(np.pi / 4)],
])

for i in range(0, len(data[5]) - 5, 5):

    # print(len(data[5]))
    # print(i)
    deltav = np.trapz(data[5][i:i + 6], data[9][i:i + 6])

    v += deltav

    clock.tick(60)

    # update stuff

    rotation_z = np.matrix([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1],
    ])

    rotation_y = np.matrix([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)],
    ])

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)],
    ])

    angle = v

    screen.fill(WHITE)
    # drawining stuff

    i = 0
    for point in points:
        rotated2d = np.dot(rotation_y, point.reshape((3, 1)))
        rotated2d = np.dot(preset, rotated2d)
        # rotated2d = np.dot(rotation_x, rotated2d)

        projected2d = np.dot(projection_matrix, rotated2d)

        x = int(projected2d[0][0] * scale) + circle_pos[0]
        y = int(projected2d[1][0] * scale) + circle_pos[1]

        projected_points[i] = [x, y]
        pygame.draw.circle(screen, RED, (x, y), 5)
        i += 1

    for p in range(4):
        connect_points(p, (p + 1) % 4, projected_points)
        connect_points(p + 4, ((p + 1) % 4) + 4, projected_points)
        connect_points(p, (p + 4), projected_points)

    pygame.display.update()

    time.sleep((data[9][i + 5] - data[9][i]))
