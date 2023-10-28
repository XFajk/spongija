import pygame

import random as rnd

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
            ),
            Tool(
                pygame.image.load("Assets/sprites/cable_icon.png").convert_alpha(),
                "cable", Interactable((0, 0), (18, 18))
            )
        ]

        self.screws: list[list[Interactable, bool, float]] = [
            [Interactable((20, 15), (8, 8)), False, 0.0],
            [Interactable((display.get_width() - 15 * 2 - 5, display.get_height() - 20 * 2 - 5), (8, 8)), False, 0.0],
            [Interactable((20, display.get_height() - 20 * 2 - 5), (8, 8)), False, 0.0],
            [Interactable((display.get_width() - 15 * 2 - 5, 15), (8, 8)), False, 0.0]
        ]
        self.screw_image: pygame.Surface = pygame.image.load("Assets/sprites/screw.png").convert_alpha()

        self.upper_plate: Interactable = Interactable(
            (15, 10),
            (display.get_width() - 15 * 2, display.get_height() - 20 * 2)
        )

        self.electrical_box: pygame.Surface = pygame.image.load("Assets/sprites/electrical_box.png").convert_alpha()

        # the difference between the mouse position and the plates rect position
        self.mouse_plate_delta: tuple = (0, 0)

        self.cable_connector: pygame.Surface = pygame.image.load("Assets/sprites/cable_connector.png").convert_alpha()
        self.cable_connector_shadow: pygame.Surface = pygame.image.load("Assets/sprites/cable_connector_shadow.png").convert_alpha()

        self.cable_colors: list[tuple[int, int, int]] = [(255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 150, 255)]

        self.left_cables: list = list()
        self.right_cables: list = list()

        self.randomize_cables()
        self.apply_colors_to_cables()

        self.cable_connections: list[tuple] = list()
        self.selected_cables: list = [None, None]

    def play(self, dt: float, tool_bar: ToolBar, display: pygame.Surface, mouse_pos: tuple,
             interaction_starter: bool) -> None:

        self.upper_plate.update(mouse_pos, interaction_starter)

        display.fill((90, 90, 90))

        # electrical box drawing
        display.blit(self.electrical_box, (15, 10))

        # drawing all the cable connectors
        for i, (left, right) in enumerate(zip(self.left_cables, self.right_cables)):
            left[1].update(mouse_pos, interaction_starter)
            right[1].update(mouse_pos, interaction_starter)

            if left[1].is_clicked and not self.upper_plate.is_held and tool_bar.current_tool.name == "cable":
                self.selected_cables[0] = i
            if right[1].is_clicked and not self.upper_plate.is_held and tool_bar.current_tool.name == "cable":
                self.selected_cables[1] = i

            display.blit(self.cable_connector_shadow, (left[1].rect.x, left[1].rect.y+1))
            display.blit(
                pygame.transform.flip(self.cable_connector_shadow, True, False),
                (right[1].rect.x, right[1].rect.y+1)
            )

            display.blit(left[0], (left[1].rect.x, left[1].rect.y))
            display.blit(right[0], (right[1].rect.x, right[1].rect.y))

        # creating the cable connections
        if self.selected_cables[0] is not None and self.selected_cables[1] is not None:
            if self.left_cables[self.selected_cables[0]][2] == self.right_cables[self.selected_cables[1]][2]:
                self.cable_connections.append(tuple(self.selected_cables))
                self.cable_connections = ic(list(set(self.cable_connections)))
                self.selected_cables = [None, None]

        # drawing the cable connections
        for cable_connection in self.cable_connections:
            pygame.draw.line(
                display, (0, 0, 0),
                (self.left_cables[cable_connection[0]][1].rect.x+9, self.left_cables[cable_connection[0]][1].rect.y+4),
                (self.right_cables[cable_connection[1]][1].rect.x+3, self.right_cables[cable_connection[1]][1].rect.y+4),
                8
            )

            pygame.draw.line(
                display, self.left_cables[cable_connection[0]][2],
                (self.left_cables[cable_connection[0]][1].rect.x+9, self.left_cables[cable_connection[0]][1].rect.y+3),
                (self.right_cables[cable_connection[1]][1].rect.x+3, self.right_cables[cable_connection[1]][1].rect.y+3),
                8
            )
            pygame.draw.line(
                display, pygame.Color(self.left_cables[cable_connection[0]][2])-pygame.Color(50, 50, 50, 0),
                (self.left_cables[cable_connection[0]][1].rect.x+9, self.left_cables[cable_connection[0]][1].rect.y+7),
                (self.right_cables[cable_connection[1]][1].rect.x+3, self.right_cables[cable_connection[1]][1].rect.y+7),
            )

        # upper plate logic and drawing
        if not len(self.screws) and self.upper_plate.is_held and tool_bar.current_tool.name == "grab":
            if self.upper_plate.is_clicked:
                self.mouse_plate_delta = mouse_pos[0] - self.upper_plate.rect.x, mouse_pos[1] - self.upper_plate.rect.y

            self.upper_plate.rect.x = mouse_pos[0] - self.mouse_plate_delta[0]
            self.upper_plate.rect.y = mouse_pos[1] - self.mouse_plate_delta[1]

        pygame.draw.rect(display, (80, 80, 90), self.upper_plate.rect)

        # screws logic and drawing
        for i, screw in enumerate(self.screws):
            screw[0].update(mouse_pos, interaction_starter)
            if tool_bar.current_tool.name == "screw_driver" and screw[0].is_held:
                screw[2] += 5 * dt
                if screw[2] > 36:
                    self.screws.pop(i)
            rotated_screw = pygame.transform.rotate(self.screw_image, screw[2])
            display.blit(
                rotated_screw,
                (
                    screw[0].rect.x - rotated_screw.get_width() / 2 + self.screw_image.get_width() / 2,
                    screw[0].rect.y - rotated_screw.get_height() / 2 + self.screw_image.get_height() / 2
                )
            )

    def randomize_cables(self):
        chosable_colors: list[tuple[int, int, int]] = self.cable_colors.copy()

        self.left_cables: list = list()

        choice = rnd.randint(0, len(chosable_colors)-1)
        self.left_cables.append(chosable_colors[choice])
        chosable_colors.pop(choice)

        choice = rnd.randint(0, len(chosable_colors)-1)
        self.left_cables.append(chosable_colors[choice])
        chosable_colors.pop(choice)

        choice = rnd.randint(0, len(chosable_colors)-1)
        self.left_cables.append(chosable_colors[choice])
        chosable_colors.pop(choice)

        choice = rnd.randint(0, len(chosable_colors)-1)
        self.left_cables.append(chosable_colors[choice])
        chosable_colors.pop(choice)

        chosable_colors: list[tuple[int, int, int]] = self.cable_colors.copy()

        choice = rnd.randint(0, len(chosable_colors)-1)
        self.right_cables.append(chosable_colors[choice])
        chosable_colors.pop(choice)

        choice = rnd.randint(0, len(chosable_colors)-1)
        self.right_cables.append(chosable_colors[choice])
        chosable_colors.pop(choice)

        choice = rnd.randint(0, len(chosable_colors)-1)
        self.right_cables.append(chosable_colors[choice])
        chosable_colors.pop(choice)

        choice = rnd.randint(0, len(chosable_colors)-1)
        self.right_cables.append(chosable_colors[choice])
        chosable_colors.pop(choice)

    def apply_colors_to_cables(self):
        for i, cable_color in enumerate(self.left_cables):
            spr_copy = self.cable_connector.copy()
            for y in range(spr_copy.get_height()):
                for x in range(spr_copy.get_width()):
                    match tuple(spr_copy.get_at((x, y))):
                        case (255, 255, 255, 255):
                            spr_copy.set_at((x, y), cable_color)
                        case (12, 230, 242, 255):
                            spr_copy.set_at(
                                (x, y), pygame.Color(cable_color)-pygame.Color(50, 50, 50, 0)
                            )
            self.left_cables[i] = spr_copy, Interactable((25, 30+i*20), (12, 8)), cable_color

        for i, cable_color in enumerate(self.right_cables):
            spr_copy = pygame.transform.flip(self.cable_connector.copy(), True, False)
            for y in range(spr_copy.get_height()):
                for x in range(spr_copy.get_width()):
                    match tuple(spr_copy.get_at((x, y))):
                        case (255, 255, 255, 255):
                            spr_copy.set_at((x, y), cable_color)
                        case (12, 230, 242, 255):
                            spr_copy.set_at(
                                (x, y), pygame.Color(cable_color)-pygame.Color(50, 50, 50, 0)
                            )
            self.right_cables[i] = spr_copy, Interactable((162, 30+i*20), (12, 8)), cable_color
