import pygame

import time

from utils.interactable import Interactable
from dataclasses import dataclass


@dataclass
class Tool:
    sprite: pygame.Surface
    name: str
    interaction: Interactable


class ToolBar:
    def __init__(self, pos: tuple):

        self.pos: pygame.Vector2 = pygame.Vector2(pos)

        self.tools: list[Tool] = []

        # here to know if the tools in the tool_bar are showing or not
        self._is_retracted: bool = True

        # collection of sprites and the current sprite we are drawing
        self._sprites: dict[str: pygame.Surface] = {
            "retracted": pygame.image.load("Assets/sprites/tool_bar_0003.png").convert_alpha(),
            "retracted_press": pygame.image.load("Assets/sprites/tool_bar_0004.png").convert_alpha(),
            "expanded": pygame.image.load("Assets/sprites/tool_bar_0001.png").convert_alpha(),
            "expanded_press": pygame.image.load("Assets/sprites/tool_bar_0002.png").convert_alpha(),
        }
        self._current_sprite: pygame.Surface = self._sprites.get("retracted")

        # here so we know what sprite to draw
        self._state: str = "retracted"

        # here to record if the tool_bar icon was clicked
        self.interaction: Interactable = Interactable(tuple(self.pos), (16, 16))

        self._press_timer = 0

        self.current_tool: Tool = Tool(pygame.Surface((0, 0)), "None", Interactable((0, 0), (0, 0)))
        self.select_sound = pygame.mixer.Sound("Assets/sound_effects/select.wav")

    def update(self, dt: float, mouse_pos: tuple, interaction_starter: bool) -> None:
        self.interaction.update(mouse_pos, interaction_starter)

        if (time.perf_counter() - self._press_timer) > 0.1:
            match self._state:
                case "retracted_press":
                    self._state = "expanded"
                    self._is_retracted = False
                case "expanded_press":
                    self._state = "retracted"
                    self._is_retracted = True

        if self.interaction.is_clicked:
            match self._state:
                case "retracted":
                    self._state = "retracted_press"
                    self._press_timer = time.perf_counter()
                case "expanded":
                    self._state = "expanded_press"
                    self._press_timer = time.perf_counter()

        self._current_sprite = self._sprites.get(self._state)

        for tool in self.tools:
            tool.interaction.update(mouse_pos, interaction_starter)
            if tool.interaction.is_clicked and tool != self.current_tool:
                self.select_sound.play(0)
                self.current_tool = tool


    def draw(self, dt: float, display: pygame.Surface) -> None:
        display.blit(self._current_sprite, self.pos)

        circle_data: tuple = (0, 0, 0, 0)
        if not self._is_retracted:
            for i, tool in enumerate(self.tools):
                display.blit(tool.sprite, (display.get_width() - 50 - i * 20, self.pos.y))
                tool.interaction.rect.x = display.get_width() - 50 - i * 20
                tool.interaction.rect.y = self.pos.y
                tool.interaction.rect.w = tool.sprite.get_width()
                tool.interaction.rect.h = tool.sprite.get_height()
                if tool == self.current_tool:
                    circle_data = (
                        self.current_tool.interaction.rect.x + self.current_tool.sprite.get_width() / 2,
                        self.current_tool.interaction.rect.y + self.current_tool.sprite.get_height() / 2,
                        14, 1
                    )

            if circle_data[2] > 0:
                pygame.draw.circle(
                    display, (255, 255, 255),
                    (circle_data[0], circle_data[1]), circle_data[2], circle_data[3]
                )
        else:
            for i, tool in enumerate(self.tools):
                tool.interaction.rect.w = 0
                tool.interaction.rect.h = 0
                tool.interaction.rect.x = self.pos.x
                tool.interaction.rect.y = self.pos.y
