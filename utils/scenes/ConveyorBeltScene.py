import pygame
from pygame import Vector2
from icecream import ic

import time
import sys
import random as rnd

from utils import ToolBar, Interactable, Tool, collision_test


class Package:
    def __init__(self, pckg_type: str, spr: pygame.Surface, rect: pygame.Rect):
        self.type = pckg_type
        self.spr = spr
        self.pos: Vector2 = Vector2(rect.x, rect.y)
        self.rect = rect
        self.velocity: Vector2 = pygame.Vector2(0, 0)
        self.inter: Interactable = Interactable(tuple(self.pos), (rect.width, rect.height))

        self.fall_sound: pygame.mixer.Sound = pygame.mixer.Sound("Assets/sound_effects/falling_bag.wav")
        self.fall_played: bool = False
        self.bottom: bool = False

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
        self.rect.x = self.pos.x
        hit_list: list[pygame.Rect] = collision_test(self.rect, box_rects) + (
            [conveyor_belt_rect, ] if self.rect.colliderect(conveyor_belt_rect) else [])
        self.rect.x = self.pos.x - 1
        self.rect.width += 2
        if self.rect.colliderect(conveyor_belt_rect):
            collision_types["conveyor_belt"] = True
        self.rect.x = self.pos.x
        self.rect.width -= 2
        for collider in hit_list:
            if self.velocity[0] > 0:
                collision_types["right"] = True
                self.rect.right = collider.left
                self.pos.x = self.rect.x

            elif self.velocity[0] < 0:
                collision_types["left"] = True
                self.rect.left = collider.right
                self.pos.x = self.rect.x

        self.pos.y += self.velocity[1] * dt
        self.rect.y = self.pos.y
        hit_list = collision_test(self.rect, box_rects) + (
            [conveyor_belt_rect, ] if self.rect.colliderect(conveyor_belt_rect) else [])

        self.rect.y = self.pos.y - 1
        self.rect.height += 2
        sound_hit_list = collision_test(self.rect, box_rects) + (
            [conveyor_belt_rect, ] if self.rect.colliderect(conveyor_belt_rect) else [])
        if self.rect.colliderect(conveyor_belt_rect):
            collision_types["conveyor_belt"] = True
        self.rect.y = self.pos.y
        self.rect.height -= 2

        if not len(sound_hit_list):
            self.bottom = False

        for collider in hit_list:
            if self.velocity[1] > 0:
                collision_types["bottom"] = True
                self.bottom = True
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

        self.won: bool = False
        self.won_timer = sys.maxsize
        self.end_won: bool = False
        self.font: pygame.font.Font = pygame.font.Font("Assets/fonts/Pixeboy.ttf", 20)
        self.text: pygame.Surface = self.font.render("Level Complete", False, (255, 255, 255), (0, 0, 0))
        self.text_pos: pygame.Vector2 = pygame.Vector2(display.get_width()/2-self.text.get_width()/2, -40)

        self.background: pygame.Surface = pygame.image.load("Assets/backgrounds/conveyor_belt/background.png")

        self.conveyor_belt_rect = pygame.Rect(120, 90, 100, 20)
        self.conveyer_belt_animation_frames: list[pygame.Surface] = [
            pygame.image.load(f"Assets/sprites/conveyor_belt_{i + 1}.png").convert_alpha() for i in range(3)
        ]
        self.conveyer_belt_animation_index: int = 0
        self.conveyor_belt_animation_timer = time.perf_counter()

        self.boxes: dict[str: pygame.Rect] = {
            "disposal": pygame.Rect(10, 140, 110, 2),
            "disposal1": pygame.Rect(10, 129, 2, 25),
            "disposal2": pygame.Rect(118, 129, 2, 25),

            "food": pygame.Rect(10, 46, 40, 2),
            "food1": pygame.Rect(10, 40, 2, 16),
            "food2": pygame.Rect(48, 40, 2, 16),

            "plants": pygame.Rect(60, 46, 40, 2),
            "plants1": pygame.Rect(60, 40, 2, 16),
            "plants2": pygame.Rect(98, 40, 2, 16),

            "extra_parts": pygame.Rect(110, 46, 40, 2),
            "extra_parts1": pygame.Rect(110, 40, 2, 16),
            "extra_parts2": pygame.Rect(148, 40, 2, 16),

            "wall1": pygame.Rect(-1, 0, 1, display.get_height()),
            "wall2": pygame.Rect(display.get_width() + 20, 0, 1, display.get_height()),
            "wall3": pygame.Rect(0, -1, display.get_width(), 1),
            "wall4": pygame.Rect(0, display.get_height(), display.get_width(), 1),
            "wall5": pygame.Rect(10, 56, 150, 2)
        }

        self.sorts: dict[str: pygame.Rect] = {
            "food": pygame.Rect(10, 20, 40, 36),
            "plants": pygame.Rect(60, 20, 40, 36),
            "parts": pygame.Rect(110, 20, 40, 36)
        }

        self.plates: dict[str: pygame.Surface] = {
            "food": pygame.image.load("Assets/sprites/food_plate.png").convert_alpha(),
            "plants": pygame.image.load("Assets/sprites/plant_plate.png").convert_alpha(),
            "parts": pygame.image.load("Assets/sprites/parts_plate.png").convert_alpha()
        }
        self.crate = pygame.image.load("Assets/sprites/crate.png").convert_alpha()
        self.big_crate = pygame.image.load("Assets/sprites/big_crate.png").convert_alpha()

        self.final_destinations: dict[str: int] = {
            "food": 0,
            "plants": 0,
            "parts": 0
        }

        self.types_of_packages: list[Package] = [
            Package("food", pygame.image.load("Assets/sprites/packs/food.png").convert_alpha(),
                    pygame.Rect(0, 0, 12, 16)),
            Package("plants", pygame.image.load("Assets/sprites/packs/plants.png").convert_alpha(),
                    pygame.Rect(0, 0, 12, 16)),
            Package("parts", pygame.image.load("Assets/sprites/packs/parts.png").convert_alpha(),
                    pygame.Rect(0, 0, 12, 16)),
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
                pygame.image.load("Assets/sprites/grab_icon.png").convert_alpha(),
                "grab", Interactable((0, 0), (16, 16))
            ),
        ]
        self.package_add_timer = time.perf_counter()

    def play(self, dt: float, tool_bar: ToolBar, display: pygame.Surface, mouse_pos: tuple,
             interaction_starter: bool) -> None:

        display.blit(self.background, (0, 0))

        # this if statement makes sure that the init method is run only once
        if not self.init_was_ran:
            self.init(tool_bar)
            self.init_was_ran = True

        if time.perf_counter() - self.package_add_timer > self.package_add_time and len(self.packages) < 10:
            pckg: Package = rnd.choice(self.types_of_packages)
            pckg.rect.x = 200
            pckg.rect.y = 74
            self.packages.append(pckg.copy())
            self.package_add_timer = time.perf_counter()

        if time.perf_counter() - self.package_add_timer > 0.2:
            self.conveyer_belt_animation_index += 1
            if self.conveyer_belt_animation_index >= len(self.conveyer_belt_animation_frames):
                self.conveyer_belt_animation_index = 0

        pygame.draw.rect(display, (100, 100, 100), (185, 70, 40, 40))
        pygame.draw.rect(display, (32, 21, 51), (188, 72, 40, 20))
        display.blit(self.conveyer_belt_animation_frames[self.conveyer_belt_animation_index], (
            self.conveyor_belt_rect.x, self.conveyor_belt_rect.y
        ))

        self.final_destinations = {
            "food": 0,
            "plants": 0,
            "parts": 0
        }
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
            if collision_types["bottom"]:
                pckg.velocity.y = 0

            if not pckg.fall_played and pckg.bottom:
                pckg.fall_sound.play(0)
                pckg.fall_played = True
            elif not pckg.bottom:
                pckg.fall_played = False

            pckg.velocity.y = 1 if collision_types["top"] else pckg.velocity.y
            if collision_types["conveyor_belt"]:
                pckg.velocity.x = -1
            else:
                pckg.velocity.x += (0 - pckg.velocity.x) / rnd.randint(10, 100) * dt

            for key, rect in self.sorts.items():
                if pckg.rect.colliderect(rect):
                    if pckg.type == key:
                        self.final_destinations[key] += 1

            display.blit(pckg.spr, pckg.pos)

        pygame.draw.rect(display, (100, 100, 100), (195, 70, 40, 40))

        display.blit(self.big_crate, (10, 125))

        for key, crate in self.sorts.items():
            display.blit(self.crate, (crate.x, crate.y + 11))
            display.blit(self.plates[key], (crate.x + 12, crate.y + 19))

        # checking for winning
        box_packages = 0
        for i in self.final_destinations.values():
            box_packages += i

        if box_packages == 10:
            if self.text_pos.y < 0:
                self.won = True

        if self.won:
            if self.text_pos.y < display.get_height()/2:
                self.text_pos.y += 3 * dt
            else:
                self.won_timer = time.perf_counter()
                self.won = False

        display.blit(
            self.font.render("Level Complete", False, (255, 255, 255)),
            self.text_pos
        )

        if time.perf_counter() - self.won_timer > 2:
            self.end_won = True

