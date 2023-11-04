import pygame

from utils import Interactable
from utils import ToolBar, Tool
from dataclasses import dataclass
import random as rnd

class WeldingScene:
    def __init__(self, tool_bar: ToolBar, display: pygame.Surface):
        tool_bar.tools = [
            Tool(
                pygame.image.load("Assets/sprites/filler_image.png").convert_alpha(),
                "grab", Interactable((0, 0), (16, 16))
            ),
            Tool(
                pygame.image.load("Assets/sprites/welder_icon.png").convert_alpha(),
                "welder", Interactable((0, 0), (18, 18))
            )
        ]

        self.panel_types: list[pygame.Surface] = [
            pygame.image.load("Assets/sprites/rocket_panels/rocket_panel_0.png").convert_alpha(),
            pygame.image.load("Assets/sprites/rocket_panels/rocket_panel_1.png").convert_alpha(),
            pygame.image.load("Assets/sprites/rocket_panels/rocket_panel_2.png").convert_alpha(),
            pygame.image.load("Assets/sprites/rocket_panels/rocket_panel_3.png").convert_alpha(),
            pygame.image.load("Assets/sprites/rocket_panels/rocket_panel_4.png").convert_alpha(),
            pygame.image.load("Assets/sprites/rocket_panels/rocket_panel_5.png").convert_alpha()
        ]
        
        self.panels: list[pygame.Surface] = []

        self.horizontal_welds: list[pygame.Surface] = [
            pygame.image.load("Assets/sprites/welds/weld_0.png").convert_alpha(),
            pygame.image.load("Assets/sprites/welds/weld_1.png").convert_alpha(),
            pygame.image.load("Assets/sprites/welds/weld_2.png").convert_alpha(),
            pygame.image.load("Assets/sprites/welds/weld.png").convert_alpha()
        ]

        self.vertical_welds: list[pygame.Surface] = [
            pygame.image.load("Assets/sprites/welds/weld_down_0.png").convert_alpha(),
            pygame.image.load("Assets/sprites/welds/weld_down_1.png").convert_alpha(),
            pygame.image.load("Assets/sprites/welds/weld_down_2.png").convert_alpha(),
            pygame.image.load("Assets/sprites/welds/weld_down.png").convert_alpha()
        ]

        self.horizontal_weld_locations = [
            (0, 46),
            (0, 94),
            (66, 46),
            (66, 94),
            (133, 46),
            (133, 94)
        ]

        self.vertical_weld_locations = [
            (61, 0),
            (61, 49),
            (61, 99),
            (129, 0),
            (129, 49),
            (129, 99)
        ]

        self.horizontal_weld_size = (67, 10)
        self.vertical_weld_size = (10, 50)
        
        self.horizontal_weld_interactables: list[Interactable] = [
            Interactable(self.horizontal_weld_locations[0], self.horizontal_weld_size),
            Interactable(self.horizontal_weld_locations[1], self.horizontal_weld_size),
            Interactable(self.horizontal_weld_locations[2], self.horizontal_weld_size),
            Interactable(self.horizontal_weld_locations[3], self.horizontal_weld_size),
            Interactable(self.horizontal_weld_locations[4], self.horizontal_weld_size),
            Interactable(self.horizontal_weld_locations[5], self.horizontal_weld_size)
        ]

        self.vertical_weld_interactables: list[Interactable] = [
            Interactable(self.vertical_weld_locations[0], self.vertical_weld_size),
            Interactable(self.vertical_weld_locations[1], self.vertical_weld_size),
            Interactable(self.vertical_weld_locations[2], self.vertical_weld_size),
            Interactable(self.vertical_weld_locations[3], self.vertical_weld_size),
            Interactable(self.vertical_weld_locations[4], self.vertical_weld_size),
            Interactable(self.vertical_weld_locations[5], self.vertical_weld_size)
        ]

        self.horizontal_weld_progress = []
        self.vertical_weld_progress = []
        
        self.randomize_panels()
        self.times_played = 0
        self.timer = 0
        self.timer_running = False
          
    def draw(self, dt: float, display: pygame.Surface) -> None:
        display.fill((15, 15, 20))
        for i in range(3):
            for j in range(3):
                display.blit(self.panels[i*3+j], (j*67, i*50))
        
        for i, prog in enumerate(self.horizontal_weld_progress):
            if prog > 5:
                display.blit(self.horizontal_welds[0], self.horizontal_weld_locations[i])
            if prog > 45:
                display.blit(self.horizontal_welds[1], self.horizontal_weld_locations[i])
            if prog > 75:
                display.blit(self.horizontal_welds[2], self.horizontal_weld_locations[i])
            if prog > 99:
                display.blit(self.horizontal_welds[3], self.horizontal_weld_locations[i])

        
        for i, prog in enumerate(self.vertical_weld_progress):
            if prog > 5:
                display.blit(self.vertical_welds[0], self.vertical_weld_locations[i])
            if prog > 45:
                display.blit(self.vertical_welds[1], self.vertical_weld_locations[i])
            if prog > 75:
                display.blit(self.vertical_welds[2], self.vertical_weld_locations[i])
            if prog > 99:
                display.blit(self.vertical_welds[3], self.vertical_weld_locations[i])

    def play(self, dt: float, tool_bar: ToolBar, display: pygame.Surface, mouse_pos: tuple, interaction_starter: bool) -> None:
        self.draw(dt, display)
        
        self.ticks = pygame.time.get_ticks()
        self.completed = True

        for i in self.horizontal_weld_progress:
            if i < 99:
                self.completed = False

        for i in self.vertical_weld_progress:
            if i < 99:
                self.completed = False

        if self.completed:
            if self.times_played < 3:
                self.times_played += 1
                self.timer = self.ticks
                self.timer_running = True
            else:
                pass #Level completed

        if self.ticks - self.timer > 1000 and self.timer_running:
            self.randomize_panels()
            self.timer_running = False

        for i, weld in enumerate(self.horizontal_weld_interactables):
            weld.update(mouse_pos, interaction_starter)
            if tool_bar.current_tool.name == "welder" and weld.is_held and self.horizontal_weld_progress[i] < 100:
                self.horizontal_weld_progress[i] += dt * 0.8

        for i, weld in enumerate(self.vertical_weld_interactables):
            weld.update(mouse_pos, interaction_starter)
            if tool_bar.current_tool.name == "welder" and weld.is_held and self.vertical_weld_progress[i] < 100:
                self.vertical_weld_progress[i] += dt * 0.8

    def randomize_panels(self):
        self.panels.clear()
        self.horizontal_weld_progress.clear()
        self.vertical_weld_progress.clear()
        for i in range(9):
            self.panels.append(self.panel_types[rnd.randint(0, 5)])
        for i in range(6):
            self.horizontal_weld_progress.append(0)
        for i in range(6):
            self.vertical_weld_progress.append(0)