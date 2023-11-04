import pygame

from utils import Interactable
from utils import ToolBar, Tool
from dataclasses import dataclass
import random as rnd

class MainMenu:
    def __init__(self, display: pygame.Surface):
        pass
          
    def draw(self, dt: float, display: pygame.Surface) -> None:
        pass

    def play(self, dt: float, tool_bar: ToolBar, display: pygame.Surface, mouse_pos: tuple, interaction_starter: bool) -> None:
        self.draw(dt, display)