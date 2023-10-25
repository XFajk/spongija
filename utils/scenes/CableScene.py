import pygame

from utils import Interactable
from utils import ToolBar, Tool
from dataclasses import dataclass

class CableScene:
    def __init__(self, tool_bar: ToolBar, display: pygame.Surface):
        tool_bar.tools = [
            Tool(
                pygame.image.load("Assets/sprites/filler_image.png").convert_alpha(),
                "grab", Interactable((0, 0), (16, 16))
            ),
            Tool(
                pygame.image.load("Assets/sprites/screw_driver_icon.png").convert_alpha(),
                "screw_driver", Interactable((0, 0), (18, 18))
            )
        ]
        
        self.screws: list[bool] = [
            [[20, 15], False],
            [[display.get_width()-15*2-5, display.get_height()-20*2-5], False],
            [[20, display.get_height()-20*2-5], False],
            [[display.get_width()-15*2-5, 15], False]
        ]
        self.screw_image: pygame.Surface = pygame.image.load("Assets/sprites/screw.png").convert_alpha()
        self.upper_plate: Interactable =  Interactable((15, 10), (display.get_width()-15*2, display.get_height()-20*2))
        
    def update(self, dt: float, tool_bar: ToolBar, mouse_pos: tuple, interaction_starter: bool) -> None:
        if tool_bar.current_tool.name == "screw_driver":
            pass
          
    def draw(self, dt: float, display: pygame.Surface) -> None:
        display.fill((90, 90, 90))
        
        pygame.draw.rect(display, (80, 80, 90), self.upper_plate.rect)
        for screw in self.screws:
            display.blit(self.screw_image, screw[0])
    
    def play(self, dt: float, tool_bar: ToolBar, display: pygame.Surface, mouse_pos: tuple, interaction_starter: bool) -> None:
        self.update(dt, tool_bar, mouse_pos, interaction_starter)
        self.draw(dt, display)
        