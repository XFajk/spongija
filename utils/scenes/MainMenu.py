import pygame

from utils import Interactable
from utils import ToolBar
from dataclasses import dataclass
import random as rnd


class MainMenu:
    def __init__(self, display: pygame.Surface):
        self.ticks = None
        self.x_2 = None
        self.y_1 = None
        self.x_1 = None
        self.y_0 = None
        self.x_0 = None
        self.y_2 = None

        self.background_image = pygame.image.load("Assets/backgrounds/main_menu/background.png").convert_alpha()
        self.rocket_image = pygame.image.load("Assets/backgrounds/main_menu/rocket.png").convert_alpha()
        self.start_button_image = pygame.image.load("Assets/backgrounds/main_menu/start_button.png").convert_alpha()
        self.start_button_over_image = pygame.image.load(
            "Assets/backgrounds/main_menu/start_button_over.png").convert_alpha()
        self.title_image = pygame.image.load("Assets/backgrounds/main_menu/title.png").convert_alpha()

        self.cloud_0_image = pygame.image.load("Assets/sprites/cloud_0.png").convert_alpha()
        self.cloud_1_image = pygame.image.load("Assets/sprites/cloud_1.png").convert_alpha()
        self.cloud_2_image = pygame.image.load("Assets/sprites/cloud_2.png").convert_alpha()

        self.cloud_0_pos = (150, 30)
        self.cloud_1_pos = (5, 10)
        self.cloud_2_pos = (65, 25)

        self.timer_0 = 0
        self.timer_1 = 0
        self.timer_2 = 0

        self.timer_0_goal = rnd.randint(500, 1800)
        self.timer_1_goal = rnd.randint(500, 1800)
        self.timer_2_goal = rnd.randint(500, 1800)

        self.start_button: Interactable = Interactable((18, 65), (103, 30))

        self.current_scene_num: list[int] = [0]

    def draw(self, dt: float, display: pygame.Surface) -> None:
        display.blit(self.background_image, (0, 0))

        display.blit(self.cloud_0_image, self.cloud_0_pos)
        display.blit(self.cloud_1_image, self.cloud_1_pos)
        display.blit(self.cloud_2_image, self.cloud_2_pos)

        display.blit(self.rocket_image, (0, 0))
        display.blit(self.title_image, (0, 0))

    def play(self, dt: float, tool_bar: ToolBar, display: pygame.Surface, mouse_pos: tuple,
             interaction_starter: bool) -> None:
        self.draw(dt, display)

        self.start_button.update(mouse_pos, interaction_starter)

        if self.start_button.is_hovering_over:
            display.blit(self.start_button_over_image, (0, 0))
        else:
            display.blit(self.start_button_image, (0, 0))

        if self.start_button.is_clicked:
            self.current_scene_num[0] += 1

        self.ticks = pygame.time.get_ticks()

        if self.ticks - self.timer_0 > self.timer_0_goal:
            self.x_0, self.y_0 = self.cloud_0_pos
            self.x_0 = self.x_0 + rnd.randint(-2, 2) * dt
            self.y_0 = self.y_0 + rnd.randint(-2, 2) * dt
            if self.x_0 > 150:
                self.x_0 = 150
            if self.x_0 < 100:
                self.x_0 = 100
            if self.y_0 > 35:
                self.y_0 = 35
            if self.y_0 < 15:
                self.y_0 = 15
            self.cloud_0_pos = self.x_0, self.y_0
            self.timer_0 = self.ticks
            self.timer_0_goal = rnd.randint(300, 1000)

        if self.ticks - self.timer_1 > self.timer_1_goal:
            self.x_1, self.y_1 = self.cloud_1_pos
            self.x_1 = self.x_1 + rnd.randint(-2, 2) * dt
            self.y_1 = self.y_1 + rnd.randint(-2, 2) * dt
            if self.x_1 > 20:
                self.x_1 = 20
            if self.x_1 < 0:
                self.x_1 = 0
            if self.y_1 > 25:
                self.y_1 = 25
            if self.y_1 < 3:
                self.y_1 = 3
            self.cloud_1_pos = self.x_1, self.y_1
            self.timer_1 = self.ticks
            self.timer_1_goal = rnd.randint(300, 1000)

        if self.ticks - self.timer_2 > self.timer_2_goal:
            self.x_2, self.y_2 = self.cloud_2_pos
            self.x_2 = self.x_2 + rnd.randint(-2, 2) * dt
            self.y_2 = self.y_2 + rnd.randint(-2, 2) * dt
            if self.x_2 > 80:
                self.x_2 = 80
            if self.x_2 < 55:
                self.x_2 = 55
            if self.y_2 > 32:
                self.y_2 = 32
            if self.y_2 < 18:
                self.y_2 = 18
            self.cloud_2_pos = self.x_2, self.y_2
            self.timer_2 = self.ticks
            self.timer_2_goal = rnd.randint(300, 1000)
