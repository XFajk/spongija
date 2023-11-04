import pygame
from pygame import Vector2
from icecream import ic

import time
import random as rnd

from utils import ToolBar, Interactable, Tool, collision_test


class Package:
    def __init__(self, type: str, spr: pygame.Surface, rect: pygame.Rect):
        self.type = type
        self.spr = spr
        self.pos: Vector2 = Vector2(rect.x, rect.y)
        self.rect = rect
        self.velocity: Vector2 = pygame.Vector2(0, 0)
        self.inter: Interactable = Interactable(tuple(self.pos), (rect.width, rect.height))

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

        self.pos.x += self.velocity[0] * dt
        self.rect.x = self.pos.x - 1
        self.rect.width += 2
        hit_list: list[pygame.Rect] = collision_test(self.rect, box_rects) + (
            [conveyor_belt_rect, ] if self.rect.colliderect(conveyor_belt_rect) else [])
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

        self.pos.y += self.velocity[1] * dt
        self.rect.y = self.pos.y - 1
        self.rect.height += 2
        hit_list = collision_test(self.rect, box_rects) + (
            [conveyor_belt_rect, ] if self.rect.colliderect(conveyor_belt_rect) else [])
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

        self.inter = Interactable(tuple(self.pos), (self.rect.width, self.rect.height))

        return collision_types


class ConveyorBeltScene:
    def __init__(self, display: pygame.Surface):
        self.init_was_ran: bool = False
        self.frame_counter = 0

        self.conveyor_belt_rect = pygame.Rect(120, 90, 80, 20)

        self.boxes: dict[str: pygame.Rect] = {
            "disposal": pygame.Rect(10, 125, 110, 25),
            "food": pygame.Rect(10, 40, 40, 16),
            "plants": pygame.Rect(60, 40, 40, 16),
            "extra_parts": pygame.Rect(110, 40, 40, 16),
            "wall1": pygame.Rect(-1, 0, 1, display.get_height()),
            "wall2": pygame.Rect(display.get_width() + 1, 0, 1, display.get_height()),
            "wall3": pygame.Rect(0, -1, display.get_width(), 1),
            "wall4": pygame.Rect(0, display.get_height(), display.get_width(), 1)
        }

        self.sorts: dict[str: pygame.Rect] = {
            "food": pygame.Rect(10, 20, 40, 36),
            "plants": pygame.Rect(60, 20, 40, 36),
            "parts": pygame.Rect(110, 20, 40, 36)
        }

        self.final_destinations: dict[str: list] = {
            "food": list(),
            "plants": list(),
            "parts": list()
        }

        self.types_of_packages: list[Package] = [
            Package("food", pygame.Surface((16, 16)), pygame.Rect(0, 0, 12, 16)),
            Package("plants", pygame.Surface((16, 16)), pygame.Rect(0, 0, 12, 16)),
            Package("parts", pygame.Surface((16, 16)), pygame.Rect(0, 0, 12, 16)),
        ]
        self.packages: list[Package] = []
        self.package_add_timer = 0
        self.package_add_time = 5

        self.package_held: int | None = None

        self.gravity: float = 0.2
        self.gravity_limit: float = 5

    def init(self, tool_bar: ToolBar):
        tool_bar.tools = [
            Tool(
                pygame.image.load("Assets/sprites/filler_image.png").convert_alpha(),
                "grab", Interactable((0, 0), (16, 16))
            ),
        ]
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

        pygame.draw.rect(display, (255, 0, 0), self.conveyor_belt_rect)

        for i, pckg in enumerate(self.packages):
            pckg.inter.update(mouse_pos, interaction_starter)

            pckg.velocity.y += self.gravity * dt
            pckg.velocity.y = self.gravity_limit if pckg.velocity.y > self.gravity_limit else pckg.velocity.y

            if tool_bar.current_tool.name == "grab" and pckg.inter.is_held and self.package_held is None or self.package_held == i:
                pckg.velocity = Vector2(
                    mouse_pos[0] - (pckg.pos.x + pckg.rect.width / 2),
                    mouse_pos[1] - (pckg.pos.y + pckg.rect.height / 2)
                ) / 10

                self.package_held = i
            if not interaction_starter and self.package_held == i:
                self.package_held = None

            collision_types: dict[str: bool] = pckg.move(dt, list(self.boxes.values()), self.conveyor_belt_rect)
            pckg.velocity.y = 0 if collision_types["bottom"] else pckg.velocity.y
            pckg.velocity.y = 1 if collision_types["top"] else pckg.velocity.y
            if collision_types["conveyor_belt"]:
                pckg.velocity.x = -1
            else:
                pckg.velocity.x += (0 - pckg.velocity.x) / rnd.randint(10, 100) * dt

            for key, rect in self.sorts.items():
                if pckg.rect.colliderect(rect):
                    if pckg.type == key:
                        self.final_destinations[key].append(0)
                        self.packages.pop(i)
                        self.package_held = None

            pygame.draw.rect(display, (255, 0, 255), pckg.rect)

        for box in self.boxes.values():
            pygame.draw.rect(display, (0, 255, 0), box)
