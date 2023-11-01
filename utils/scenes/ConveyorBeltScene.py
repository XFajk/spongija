import pygame
from icecream import ic

from dataclasses import dataclass
import time
import random as rnd

from utils import ToolBar


@dataclass
class Package:
    type: str
    spr: pygame.Surface
    rect: pygame.Rect


class ConveyorBeltScene:
    def __init__(self, display: pygame.Surface):
        self.init_was_ran: bool = False

        self.conveyor_belt_rect = pygame.Rect(120, 90, 80, 20)

        self.disposal_box = pygame.Rect(10, 125, 110, 25)

        self.boxes: dict = {
            "food": pygame.Rect(10, 40, 40, 16),
            "plants": pygame.Rect(60, 40, 40, 16),
            "extra_parts": pygame.Rect(110, 40, 40, 16)
        }

        self.types_of_packages: list[Package] = [
            Package("food", pygame.Surface((16, 16)), pygame.Rect(0, 0, 16, 16)),
            Package("plants", pygame.Surface((16, 16)), pygame.Rect(0, 0, 16, 16)),
            Package("parts", pygame.Surface((16, 16)), pygame.Rect(0, 0, 16, 16)),
        ]
        self.packages: list[Package] = []
        self.package_add_timer = 0
        self.package_add_time = 5

        self.gravity: float = 0.2

    def init(self, tool_bar: ToolBar):
        tool_bar.tools = []
        self.package_add_timer = time.perf_counter()

    def play(self, dt: float, tool_bar: ToolBar, display: pygame.Surface, mouse_pos: tuple,
             interaction_starter: bool) -> None:
        # this if statement makes sure that the init method is run only once
        if not self.init_was_ran:
            self.init(tool_bar)
            self.init_was_ran = True

        if time.perf_counter() - self.package_add_timer > self.package_add_time:
            pckg: Package = rnd.choice(self.types_of_packages)
            pckg.rect.x = 180
            pckg.rect.y = 74
            self.packages.append(pckg)

        pygame.draw.rect(display, (255, 0, 0), self.conveyor_belt_rect)
        pygame.draw.rect(display, (0, 0, 255), self.disposal_box)

        for pckg in self.packages:
            
            pygame.draw.rect(display, (255, 0, 255), pckg.rect)

        for key, box in self.boxes.items():
            pygame.draw.rect(display, (0, 255, 0), box)
