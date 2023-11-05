import pygame

import math


def delete_duplicate(list_of_objects: list):
    unique_list_of_objects = []
    for element in list_of_objects:
        if element not in unique_list_of_objects:
            unique_list_of_objects.append(element)

    return unique_list_of_objects


def collision_test(main_rect: pygame.Rect, rects: list[pygame.Rect]) -> list[pygame.Rect]:
    hit_list: list[pygame.Rect] = []

    for rect in rects:
        if main_rect.colliderect(rect):
            hit_list.append(rect.copy())

    return hit_list


class Spark:
    def __init__(self, loc: list | tuple | pygame.Vector2, angle: float, speed: float, color: tuple = (255, 255, 255),
                 scale: float = 1,
                 dis_amount: float = 0.25):
        self.loc = loc
        self.angle = angle
        self.speed = speed
        self.scale = scale
        self.color = color
        self.dis_amount = dis_amount
        self.alive = True

    def calculate_movement(self, dt: float):
        return [math.cos(self.angle) * self.speed * dt, math.sin(self.angle) * self.speed * dt]

    def velocity_adjust(self, friction, force, terminal_velocity, dt):
        movement = self.calculate_movement(dt)
        movement[1] = min(terminal_velocity, movement[1] + force * dt)
        movement[0] *= friction
        self.angle = math.atan2(movement[1], movement[0])

    def move(self, dt: float, gravity: float = 0.0):
        movement = self.calculate_movement(dt)
        self.loc[0] += movement[0]
        self.loc[1] += movement[1]
        if gravity > 0:
            self.velocity_adjust(0.975, gravity, 8, dt)

        self.speed -= self.dis_amount * dt

        if self.speed <= 0:
            self.alive = False

    def draw(self, surf):
        if self.alive:
            points = [
                [self.loc[0] + math.cos(self.angle) * self.speed * self.scale,
                 self.loc[1] + math.sin(self.angle) * self.speed * self.scale],
                [self.loc[0] + math.cos(self.angle + math.pi / 2) * self.speed * self.scale * 0.3,
                 self.loc[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                [self.loc[0] - math.cos(self.angle) * self.speed * self.scale * 3.5,
                 self.loc[1] - math.sin(self.angle) * self.speed * self.scale * 3.5],
                [self.loc[0] + math.cos(self.angle - math.pi / 2) * self.speed * self.scale * 0.3,
                 self.loc[1] - math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
            ]
            pygame.draw.polygon(surf, self.color, points)
