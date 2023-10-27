import pygame

from utils import Interactable
from utils import ToolBar, Tool
from dataclasses import dataclass

class FuelScene:
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
        
        self.screws: list[list[Interactable, bool, float]] = [
            [Interactable((188, 78), (2, 2)), False, 0.0],
            [Interactable((188, 95), (2, 2)), False, 0.0],
            [Interactable((171, 95), (2, 2)), False, 0.0],
            [Interactable((171, 78), (2, 2)), False, 0.0]
        ]
        self.screw_image: pygame.Surface = pygame.image.load("Assets/sprites/small_screw.png").convert_alpha()

        self.hose: Interactable = Interactable((151, 94), (8, 8))

        self.images: list[pygame.Surface] = [
            pygame.transform.scale(pygame.image.load("Assets/backgrounds/image_1.png").convert_alpha(), (200, 150)),
            pygame.transform.scale(pygame.image.load("Assets/backgrounds/image_2.png").convert_alpha(), (200, 150)),
            pygame.transform.scale(pygame.image.load("Assets/backgrounds/image_3.png").convert_alpha(), (200, 150))
        ]
        
        self.panel_image = pygame.transform.scale(pygame.image.load("Assets/sprites/fuel_panel.png").convert_alpha(), (25, 25))

        self.panel_state = True
        self.pannel_x = 169
        self.pannel_y = 75

        self.frame = 0
          
    def draw(self, dt: float, display: pygame.Surface) -> None:
        display.fill((37, 36, 70))

        display.blit(self.images[self.frame], (0, 0))
        
        if self.panel_state == True:
            display.blit(self.panel_image, (self.pannel_x, self.pannel_y))

        for screw in self.screws:
            display.blit(self.screw_image, screw[0])
        
        self.hose.debug_draw(display, (255, 0, 0))
    
    def play(self, dt: float, tool_bar: ToolBar, display: pygame.Surface, mouse_pos: tuple, interaction_starter: bool) -> None:
        self.draw(dt, display)

        for i, screw in enumerate(self.screws):
            screw[0].update(mouse_pos, interaction_starter)
            if tool_bar.current_tool.name == "screw_driver" and screw[0].is_held:
                screw[2] += 5 * dt
                if screw[2] > 360:
                    self.screws.pop(i)
            rotated_screw = pygame.transform.rotate(self.screw_image, screw[2])
            display.blit(
                rotated_screw,
                (
                    screw[0].rect.x - rotated_screw.get_width() / 2 + self.screw_image.get_width() / 2,
                    screw[0].rect.y - rotated_screw.get_height() / 2 + self.screw_image.get_height() / 2
                )
            )
        
        if not len(self.screws) and self.panel_state:
            self.pannel_x += 0.5*dt
            display.blit(self.panel_image, (self.pannel_x, self.pannel_y))
            self.panel_state = False if self.pannel_x > 201 else True

        if self.hose.is_clicked and not self.panel_state and tool_bar.current_tool.name == "grab":
            self.frame = 1

        if self.frame == 0:
            self.hose.update(mouse_pos, interaction_starter)