import pygame
from pygame import Vector2
from icecream import ic

import time
import random as rnd

from utils import ToolBar, collision_test


class Package:
    def __init__(self, type: str, spr: pygame.Surface, rect: pygame.Rect):
        self.type = type
        self.spr = spr
        self.pos: Vector2 = Vector2(rect.x, rect.y)
        self.rect = rect
        self.velocity: Vector2 = pygame.Vector2(0, 0)
        
    def copy(self):
        new_instance = self.__class__(self.type, self.spr.copy(), self.rect.copy())
        return new_instance
    
    def move(self, dt: float, box_rects: list[pygame.Rect], conveyor_belt_rect: pygame.Rect) -> dict[str: bool]:
        collision_types: dict[str: bool] = {
            "top": False,
            "bottom": False,
            "left": False,
            "right": False,
            "conveyor_belt": False
        }
              
        self.pos.x += self.velocity[0]*dt
        self.rect.x = self.pos.x-1
        self.rect.width += 2
        hit_list: list[pygame.Rect] = collision_test(self.rect, box_rects) + ([conveyor_belt_rect,] if self.rect.colliderect(conveyor_belt_rect) else []) 
        self.rect.x = self.pos.x
        self.rect.width -= 2
        if self.rect.colliderect(conveyor_belt_rect):
            collision_types["conveyor_belt"] = True
            
        for collider in hit_list:
            if self.rect.colliderect(conveyor_belt_rect):
                collision_types["conveyor_belt"] = True
            
            if self.velocity[0] > 0:
                collision_types["right"] = True
                self.rect.right = collider.left
                self.pos.x = self.rect.x
                
            elif self.velocity[0] < 0:
                collision_types["left"] = True
                self.rect.left = collider.right
                self.pos.x = self.rect.x
                 
        self.pos.y += self.velocity[1]*dt
        self.rect.y = self.pos.y-1
        self.rect.height += 2
        hit_list = collision_test(self.rect, box_rects) + ([conveyor_belt_rect,] if self.rect.colliderect(conveyor_belt_rect) else [])
        if self.rect.colliderect(conveyor_belt_rect):
                collision_types["conveyor_belt"] = True
        self.rect.y = self.pos.y
        self.rect.height -= 2
        for collider in hit_list: 
            if self.velocity[1] > 0:
                collision_types["bottom"] = True
                self.rect.bottom = collider.top
                self.pos.y = self.rect.y
            elif self.velocity[1] < 0:
                collision_types["top"] = True
                self.rect.top = collider.bottom
                self.pos.y = self.rect.y 
                
        return collision_types
        
        

class ConveyorBeltScene:
    def __init__(self, display: pygame.Surface):
        self.init_was_ran: bool = False
        self.frame_counter = 0

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
        self.gravity_limit: float = 5

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
            self.packages.append(pckg.copy())
            self.package_add_timer = time.perf_counter()
            ic(len(self.packages))

        pygame.draw.rect(display, (255, 0, 0), self.conveyor_belt_rect)

        for pckg in self.packages:
            pckg.velocity.y += self.gravity*dt
            pckg.velocity.y = self.gravity_limit if pckg.velocity.y > self.gravity_limit else pckg.velocity.y
            
            collision_types: dict[str: bool] = pckg.move(dt, list(self.boxes.values()), self.conveyor_belt_rect)
            pckg.velocity.y = 0 if collision_types["bottom"] else pckg.velocity.y
            if collision_types["conveyor_belt"]:
                pckg.velocity.x = -1
            else:
                pckg.velocity.x += rnd.randint(1, 30)/1000 if pckg.velocity.x < 0 else -pckg.velocity.x
            
            pygame.draw.rect(display, (255, 0, 255), pckg.rect)

        for box in self.boxes.values():
            pygame.draw.rect(display, (0, 255, 0), box)
