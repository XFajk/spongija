import pygame
from icecream import ic

import random as rnd
import time
import math
import sys
from dataclasses import dataclass

from utils import ToolBar, Tool, Interactable, delete_duplicate


@dataclass
class Screw:
    inter: Interactable
    rotation_angle: float


@dataclass
class CableConnector:
    spr: pygame.Surface
    inter: Interactable
    color: tuple


class CableScene:
    def __init__(self, display: pygame.Surface):
        self.won: bool = False
        self.won_timer = sys.maxsize
        self.end_won: bool = False
        self.font: pygame.font.Font = pygame.font.Font("Assets/fonts/Pixeboy.ttf", 20)
        self.text: pygame.Surface = self.font.render("Level Complete", False, (255, 255, 255))
        self.text_pos: pygame.Vector2 = pygame.Vector2(display.get_width()/2-self.text.get_width()/2, -40)
        self.complete_sound = pygame.mixer.Sound("Assets/sound_effects/complete.wav")

        self.screws: list[Screw] = [
            Screw(Interactable((20, 15), (8, 8)), 0.0),
            Screw(Interactable((display.get_width() - 15 * 2 - 5, display.get_height() - 20 * 2 - 5), (8, 8)), 0.0),
            Screw(Interactable((20, display.get_height() - 20 * 2 - 5), (8, 8)), 0.0),
            Screw(Interactable((display.get_width() - 15 * 2 - 5, 15), (8, 8)), 0.0)
        ]
        self.screw_image: pygame.Surface = pygame.image.load("Assets/sprites/screw.png").convert_alpha()
        self.screw_sound: pygame.mixer.Sound = pygame.mixer.Sound("Assets/sound_effects/metal_plate.wav")
        self.screw_sound_played: bool = False
        self.screw_sound_timer: float = sys.maxsize

        self.upper_plate: Interactable = Interactable(
            (15, 10),
            (display.get_width() - 15 * 2, display.get_height() - 20 * 2)
        )

        self.electrical_box: pygame.Surface = pygame.image.load("Assets/sprites/electrical_box.png").convert_alpha()

        # the difference between the mouse position and the plates rect position
        self.mouse_plate_delta: tuple = (0, 0)

        self.cable_connector: pygame.Surface = pygame.image.load("Assets/sprites/cable_connector.png").convert_alpha()
        self.cable_connector_shadow: pygame.Surface = pygame.image.load(
            "Assets/sprites/cable_connector_shadow.png").convert_alpha()

        self.sparks_effect_timer = time.perf_counter()
        self.sparks_effect = list()
        self.spark_spawn_positions = list()

        self.sparks_sound = pygame.mixer.Sound("Assets/sound_effects/electrical_sparks.wav")

        self.cable_colors: list[tuple[int, int, int]] = [(255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 150, 255)]

        self.left_cables: list[CableConnector] = list()
        self.right_cables: list[CableConnector] = list()

        self.randomize_cables()
        self.apply_colors_to_cables()

        # these variables are for knowing what cable_connectors to connect
        self.cable_connections: list[tuple] = list()
        self.selected_cables: list = [None, None]

        self.select_sound = pygame.mixer.Sound("Assets/sound_effects/select.wav")
        self.connect_sound = pygame.mixer.Sound("Assets/sound_effects/connect.wav")

        self.saved_cable_connections: list[tuple[list[CableConnector], list[CableConnector], list[tuple]]] = list()
        self.are_cable_connections_saved: bool = False

        self.init_played: bool = False

        self.rounds_played: int = 0

    @staticmethod
    def init(tool_bar: ToolBar):
        tool_bar.tools = [
            Tool(
                pygame.image.load("Assets/sprites/grab_icon.png").convert_alpha(),
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

    def play(self, dt: float, tool_bar: ToolBar, display: pygame.Surface, mouse_pos: tuple,
             interaction_starter: bool) -> None:

        if not self.init_played:
            self.init(tool_bar)
            self.init_played = True

        # makes sure a cable inst selected after the old ones where saved
        if interaction_starter and self.are_cable_connections_saved:
            self.selected_cables = [None, None]
        else:
            self.are_cable_connections_saved = False
        if len(self.cable_connections) == 4 and self.rounds_played < 3:
            for left, right in zip(self.left_cables, self.right_cables):
                left.color = pygame.Color(left.color) - pygame.Color(125, 125, 150, 0)
                right.color = pygame.Color(right.color) - pygame.Color(125, 125, 150, 0)

            self.saved_cable_connections.append((
                self.left_cables.copy(), self.right_cables.copy(), self.cable_connections.copy()
            ))
            self.randomize_cables()
            self.apply_colors_to_cables()
            self.selected_cables = [None, None]
            self.cable_connections = list()
            self.are_cable_connections_saved = True
            self.rounds_played += 1

        self.upper_plate.update(mouse_pos, interaction_starter)

        display.fill((90, 90, 90))

        # electrical box drawing
        display.blit(self.electrical_box, (15, 10))

        # drawing of the saved cable connections
        for scc in self.saved_cable_connections:
            for left, right in zip(scc[0], scc[1]):
                display.blit(self.cable_connector_shadow, (left.inter.rect.x, left.inter.rect.y + 1))
                display.blit(
                    pygame.transform.flip(self.cable_connector_shadow, True, False),
                    (right.inter.rect.x, right.inter.rect.y + 1)
                )

                display.blit(left.spr, (left.inter.rect.x, left.inter.rect.y))
                display.blit(right.spr, (right.inter.rect.x, right.inter.rect.y))

            for connection in scc[2]:
                pygame.draw.line(
                    display, (0, 0, 0),
                    (scc[0][connection[0]].inter.rect.x + 9,
                     scc[0][connection[0]].inter.rect.y + 4),
                    (scc[1][connection[1]].inter.rect.x + 3,
                     scc[0][connection[1]].inter.rect.y + 4),
                    8
                )

                pygame.draw.line(
                    display, scc[0][connection[0]].color,
                    (scc[0][connection[0]].inter.rect.x + 9,
                     scc[0][connection[0]].inter.rect.y + 3),
                    (scc[1][connection[1]].inter.rect.x + 3,
                     scc[1][connection[1]].inter.rect.y + 3),
                    8
                )
                pygame.draw.line(
                    display, pygame.Color(scc[0][connection[0]].color) - pygame.Color(50, 50, 50, 0),
                    (scc[0][connection[0]].inter.rect.x + 9,
                     scc[0][connection[0]].inter.rect.y + 7),
                    (scc[1][connection[1]].inter.rect.x + 3,
                     scc[1][connection[1]].inter.rect.y + 7),
                )

        for i, s in sorted(enumerate(self.sparks_effect), reverse=True):
            s[0][0] += s[1][0] * dt
            s[0][1] += s[1][1] * dt
            s[1][1] += 0.1 * dt
            s[2] -= 0.05 * dt
            pygame.draw.circle(display, (255, 255, 0), s[0], s[2])
            if s[2] <= 0:
                self.sparks_effect.pop(i)

        # drawing all the cable connectors
        for i, (left, right) in enumerate(zip(self.left_cables, self.right_cables)):
            left.inter.update(mouse_pos, interaction_starter)
            right.inter.update(mouse_pos, interaction_starter)
            if left.inter.is_clicked and not self.upper_plate.is_held and tool_bar.current_tool.name == "cable":
                self.selected_cables[0] = i
                self.select_sound.play(0)
            if right.inter.is_clicked and not self.upper_plate.is_held and tool_bar.current_tool.name == "cable":
                self.selected_cables[1] = i
                self.select_sound.play(0)

            if time.perf_counter() - self.sparks_effect_timer > 2 and self.rounds_played < 4:
                # timing the spawning of the sparks
                if not self.upper_plate.rect.colliderect(left.inter.rect) and not self.upper_plate.rect.colliderect(
                        right.inter.rect):
                    indexes = [i for i in range(4)]
                    left_indexes = [left for left, right in self.cable_connections]
                    right_indexes = [right for left, right in self.cable_connections]
                    missing_indexes = []

                    for index in indexes:
                        if index not in left_indexes:
                            missing_indexes.append((index, True))

                        if index not in right_indexes:
                            missing_indexes.append((index, False))

                    # spawning the sparks
                    self.spark_spawn_positions = [
                        (37 if side else 162, (30 + index * 20) + 4) for index, side in missing_indexes
                    ]
                    spark_pos: tuple = rnd.choice(self.spark_spawn_positions)

                    self.sparks_sound.play(0)

                    for j in range(10):
                        spark_angle = math.radians(rnd.randint(-90, 90) if spark_pos[0] == 37 else rnd.randint(90, 270))
                        self.sparks_effect.append([
                            list(spark_pos),
                            [
                                math.cos(spark_angle) * rnd.randint(50, 100) / 100,
                                -math.sin(spark_angle) * rnd.randint(50, 100) / 100
                            ],
                            rnd.randint(2, 4)
                        ])
                self.sparks_effect_timer = time.perf_counter()

            display.blit(self.cable_connector_shadow, (left.inter.rect.x, left.inter.rect.y + 1))
            display.blit(
                pygame.transform.flip(self.cable_connector_shadow, True, False),
                (right.inter.rect.x, right.inter.rect.y + 1)
            )

            display.blit(left.spr, (left.inter.rect.x, left.inter.rect.y))
            display.blit(right.spr, (right.inter.rect.x, right.inter.rect.y))

        # creating the cable connections
        if self.selected_cables[0] is not None and self.selected_cables[1] is not None:
            self.connect_sound.play(0)

            if self.left_cables[self.selected_cables[0]].color == self.right_cables[self.selected_cables[1]].color:
                self.cable_connections.append(tuple(self.selected_cables))
                self.cable_connections = delete_duplicate(self.cable_connections)
                self.selected_cables = [None, None]

        # drawing the cable connections
        for cable_connection in self.cable_connections:
            pygame.draw.line(
                display, (0, 0, 0),
                (self.left_cables[cable_connection[0]].inter.rect.x + 9,
                 self.left_cables[cable_connection[0]].inter.rect.y + 4),
                (self.right_cables[cable_connection[1]].inter.rect.x + 3,
                 self.right_cables[cable_connection[1]].inter.rect.y + 4),
                8
            )

            pygame.draw.line(
                display, self.left_cables[cable_connection[0]].color,
                (self.left_cables[cable_connection[0]].inter.rect.x + 9,
                 self.left_cables[cable_connection[0]].inter.rect.y + 3),
                (self.right_cables[cable_connection[1]].inter.rect.x + 3,
                 self.right_cables[cable_connection[1]].inter.rect.y + 3),
                8
            )
            pygame.draw.line(
                display, pygame.Color(self.left_cables[cable_connection[0]].color) - pygame.Color(50, 50, 50, 0),
                (self.left_cables[cable_connection[0]].inter.rect.x + 9,
                 self.left_cables[cable_connection[0]].inter.rect.y + 7),
                (self.right_cables[cable_connection[1]].inter.rect.x + 3,
                 self.right_cables[cable_connection[1]].inter.rect.y + 7),
            )

        # upper plate logic and drawing
        if not len(self.screws) and self.upper_plate.is_held and tool_bar.current_tool.name == "grab":
            if self.upper_plate.is_clicked:
                self.mouse_plate_delta = mouse_pos[0] - self.upper_plate.rect.x, mouse_pos[1] - self.upper_plate.rect.y

            self.upper_plate.rect.x = mouse_pos[0] - self.mouse_plate_delta[0]
            self.upper_plate.rect.y = mouse_pos[1] - self.mouse_plate_delta[1]

        # drawing the selection of what cable connectors to connect
        if self.selected_cables[0] is not None:
            pygame.draw.circle(display, (255, 255, 255), (
                self.left_cables[self.selected_cables[0]].inter.rect.x + 6,
                self.left_cables[self.selected_cables[0]].inter.rect.y + 4
            ), 7, 1)

        if self.selected_cables[1] is not None:
            pygame.draw.circle(display, (255, 255, 255), (
                self.right_cables[self.selected_cables[1]].inter.rect.x + 6,
                self.right_cables[self.selected_cables[1]].inter.rect.y + 4
            ), 7, 1)

        pygame.draw.rect(display, (80, 80, 90), self.upper_plate.rect)

        # screws logic and drawing
        for i, screw in enumerate(self.screws):
            screw.inter.update(mouse_pos, interaction_starter)
            if tool_bar.current_tool.name == "screw_driver" and screw.inter.is_held:
                if not self.screw_sound_played:
                    self.screw_sound.play(0)
                    self.screw_sound_timer = time.perf_counter()
                    self.screw_sound_played = True
                screw.rotation_angle += 5 * dt
                if screw.rotation_angle > 360:
                    self.screws.pop(i)
            rotated_screw = pygame.transform.rotate(self.screw_image, screw.rotation_angle)

            shadow = pygame.Surface((8, 8))
            shadow.set_colorkey((0, 0, 0))
            shadow.fill((0, 0, 1))
            shadow = pygame.transform.rotate(shadow, screw.rotation_angle)

            display.blit(
                shadow,
                (
                    screw.inter.rect.x - rotated_screw.get_width() / 2 + self.screw_image.get_width() / 2 + 1,
                    screw.inter.rect.y - rotated_screw.get_height() / 2 + self.screw_image.get_height() / 2 + 1
                )
            )

            display.blit(
                rotated_screw,
                (
                    screw.inter.rect.x - rotated_screw.get_width() / 2 + self.screw_image.get_width() / 2,
                    screw.inter.rect.y - rotated_screw.get_height() / 2 + self.screw_image.get_height() / 2
                )
            )
        if time.perf_counter() - self.screw_sound_timer > self.screw_sound.get_length():
            self.screw_sound_played = False

        # checking for winning
        if len(self.cable_connections) == 4 and self.rounds_played == 3:
            self.won = True
            self.rounds_played += 1

        if self.won:
            if self.text_pos.y < display.get_height()/2-20:
                self.text_pos.y += 3 * dt
            else:
                self.won_timer = time.perf_counter()
                self.won = False
                self.complete_sound.play(0)

        display.blit(
            self.font.render("Level Complete", False, (255, 255, 255)),
            self.text_pos
        )

        if time.perf_counter() - self.won_timer > 2:
            self.end_won = True

    def randomize_cables(self):
        chosable_colors: list[tuple[int, int, int]] = self.cable_colors.copy()
        self.left_cables: list[CableConnector] = list()

        for i in range(4):
            choice = rnd.randint(0, len(chosable_colors) - 1)
            self.left_cables.append(CableConnector(
                pygame.Surface((0, 0)),
                Interactable((0, 0), (0, 0)),
                chosable_colors[choice]
            ))
            chosable_colors.pop(choice)

        chosable_colors: list[tuple[int, int, int]] = self.cable_colors.copy()
        self.right_cables: list[CableConnector] = list()

        for i in range(4):
            choice = rnd.randint(0, len(chosable_colors) - 1)
            self.right_cables.append(CableConnector(
                pygame.Surface((0, 0)),
                Interactable((0, 0), (0, 0)),
                chosable_colors[choice]
            ))
            chosable_colors.pop(choice)

    def apply_colors_to_cables(self):
        for i, cable_connector in enumerate(self.left_cables):
            spr_copy = self.cable_connector.copy()
            for y in range(spr_copy.get_height()):
                for x in range(spr_copy.get_width()):
                    match tuple(spr_copy.get_at((x, y))):
                        case (255, 255, 255, 255):
                            spr_copy.set_at((x, y), cable_connector.color)
                        case (12, 230, 242, 255):
                            spr_copy.set_at(
                                (x, y), pygame.Color(cable_connector.color) - pygame.Color(50, 50, 50, 0)
                            )

            self.left_cables[i] = CableConnector(
                spr_copy, Interactable((25, 30 + i * 20), (12, 8)), cable_connector.color
            )

        for i, cable_connector in enumerate(self.right_cables):
            spr_copy = pygame.transform.flip(self.cable_connector.copy(), True, False)
            for y in range(spr_copy.get_height()):
                for x in range(spr_copy.get_width()):
                    match tuple(spr_copy.get_at((x, y))):
                        case (255, 255, 255, 255):
                            spr_copy.set_at((x, y), cable_connector.color)
                        case (12, 230, 242, 255):
                            spr_copy.set_at(
                                (x, y), pygame.Color(cable_connector.color) - pygame.Color(50, 50, 50, 0)
                            )
            self.right_cables[i] = CableConnector(
                spr_copy, Interactable((162, 30 + i * 20), (12, 8)), cable_connector.color
            )
