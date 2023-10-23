import pygame
from dataclasses import dataclass
from icecream import ic


class ElectricalBoardTask:
    def __init__(self):
        pass

    def update(self, dt, mouse_pos, mouse_input):
        pass

    def draw(self, dt, display: pygame.Surface):
        pass

    def play(self, dt, display, mouse_pos, mouse_input):
        self.draw(dt, display)
        self.update(dt, mouse_pos, mouse_input)
