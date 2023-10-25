import pygame

from utils import Interactable
from utils import ToolBar, Tool

from icecream import ic


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

        self.screws: list[list[Interactable, bool, float]] = [
            [Interactable((20, 15), (8, 8)), False, 0.0],
            [Interactable((display.get_width() - 15 * 2 - 5, display.get_height() - 20 * 2 - 5), (8, 8)), False, 0.0],
            [Interactable((20, display.get_height() - 20 * 2 - 5), (8, 8)), False, 0.0],
            [Interactable((display.get_width() - 15 * 2 - 5, 15), (8, 8)), False, 0.0]
        ]
        self.screw_image: pygame.Surface = pygame.image.load("Assets/sprites/screw.png").convert_alpha()
        self.upper_plate: Interactable = Interactable((15, 10),
                                                      (display.get_width() - 15 * 2, display.get_height() - 20 * 2))

    def play(self, dt: float, tool_bar: ToolBar, display: pygame.Surface, mouse_pos: tuple,
             interaction_starter: bool) -> None:

        display.fill((90, 90, 90))

        pygame.draw.rect(display, (80, 80, 90), self.upper_plate.rect)
        for i, screw in enumerate(self.screws):
            screw[0].update(mouse_pos, interaction_starter)
            if tool_bar.current_tool.name == "screw_driver" and screw[0].is_held:
                screw[2] += 5 * dt
                if screw[2] > 360:
                    self.screws.pop(i)
            ic(screw[2])
            rotated_screw = pygame.transform.rotate(self.screw_image, screw[2])
            display.blit(
                rotated_screw,
                (
                    screw[0].rect.x - rotated_screw.get_width() / 2 + self.screw_image.get_width()/2,
                    screw[0].rect.y - rotated_screw.get_height() / 2 + self.screw_image.get_height()/2
                )
            )
