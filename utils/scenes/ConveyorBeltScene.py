import pygame
from icecream import ic

import time
import random as rnd

from utils import ToolBar, collision_test


class Package:
    def __init__(self, type: str, spr: pygame.Surface, rect: pygame.Rect):
        self.type = type
        self.spr = spr
        self.rect = rect
    
    def move(self, velocity: pygame.Vector2 | list, box_rects: list[pygame.Rect], conveyor_belt_rect: pygame.Rect) -> dict[str: bool]:
        collision_types: dict[str: bool] = {
            "top": False,
            "bottom": False,
            "left": False,
            "right": False
        }
        
        self.rect.x += velocity[0] 
        hit_list: list[pygame.Rect] = collision_test(self.rect, box_rects) + ([conveyor_belt_rect,] if self.rect.colliderect(conveyor_belt_rect) else [])
        for collider in hit_list:
            if velocity[0] > 0:
                collision_types["right"] = True
                self.rect.right = collider.left
            elif velocity[0] < 0:
                collision_types["left"] = True
                self.rect.left = collider.right
        
        self.rect.y += velocity[1]
        hit_list = collision_test(self.rect, box_rects) + ([conveyor_belt_rect,] if self.rect.colliderect(conveyor_belt_rect) else [])
        for collider in hit_list:
            if velocity[1] > 0:
                collision_types["bottom"] = True
                self.rect.bottom = collider.top
            elif velocity[1] < 0:
                collision_types["top"] = True
                self.rect.top = collider.bottom
        return collision_types
        
        

class ConveyorBeltScene:
    def __init__(self, display: pygame.Surface):
        self.init_was_ran: bool = False

        self.conveyor_belt_rect = pygame.Rect(120, 90, 80, 20) 

        self.boxes: dict = {
            "disposal": pygame.Rect(10, 125, 110, 25),
            "food": pygame.Rect(10, 40, 40, 16),
            "plants": pygame.Rect(60, 40, 40, 16),
            "extra_parts": pygame.Rect(110, 40, 40, 16)
        }

        self.types_of_packages: list[Package] = [
            Package("food", pygame.Surface((16, 16)), pygame.Rect(0, 0, 12, 16)),
            Package("plants", pygame.Surface((16, 16)), pygame.Rect(0, 0, 12, 16)),
            Package("parts", pygame.Surface((16, 16)), pygame.Rect(0, 0, 12, 16)),
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

        for pckg in self.packages:
            pckg.move([0, 0], list(self.boxes.values()), self.conveyor_belt_rect)
            pygame.draw.rect(display, (255, 0, 255), pckg.rect)

        for box in self.boxes.values():
            pygame.draw.rect(display, (0, 255, 0), box)
