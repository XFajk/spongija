import pygame

from utils import Interactable
from utils import ToolBar, Tool
from dataclasses import dataclass


class StartCutscene:
    def __init__(self, display: pygame.Surface):
        
        self.frames: list[pygame.Surface] = [
            pygame.image.load("Assets/cutscenes/research_institute.png").convert_alpha(),
            pygame.image.load("Assets/cutscenes/folder.png").convert_alpha(),
            pygame.transform.scale(pygame.image.load("Assets/cutscenes/notepad.png").convert_alpha(), (200, 150)),
            pygame.transform.scale(pygame.image.load("Assets/cutscenes/meteorite.png").convert_alpha(), (200, 150)),
            pygame.transform.scale(pygame.image.load("Assets/cutscenes/rocket.png").convert_alpha(), (200, 150))
        ]

        self.dialog_box = pygame.image.load("Assets/sprites/dialog_box.png").convert_alpha()

        self.font = pygame.font.Font("Assets/fonts/Pixeboy.ttf", 16)

        self.current_frame = 0

        self.button: Interactable = Interactable((0, 0), (200, 150))
        self.waiting = False

        self.text = 0
        
        self.text_0 = "You're a worker at NASA,   "
        self.text_0_char = False
        self.text_0_timer = 0

        self.text_1 = "glenn Research Cener.   "
        self.text_1_char = False
        self.text_1_timer = 0
        self.text_1_begun = False
        
        self.initial_timer = False
        self.initial_timer_done = False

    def draw(self, dt: float, display: pygame.Surface) -> None:
        
        display.fill((0, 0, 0))
        display.blit(self.frames[self.current_frame], (0, 0))

    def play(self, dt: float, tool_bar: ToolBar, display: pygame.Surface, mouse_pos: tuple,
             interaction_starter: bool) -> None:
        
        self.ticks = pygame.time.get_ticks()
        self.button.update(mouse_pos, interaction_starter)

        self.draw(dt, display)

        if self.initial_timer == False:
            self.initial_timer = pygame.time.get_ticks()

        if self.current_frame == 0 and self.ticks - self.initial_timer > 2200 and not self.initial_timer_done and self.text == 0:
            self.text_0_char = 0
            self.text_0_timer = self.ticks
            self.initial_timer_done = True

        if self.text_0_char >= 0 and self.ticks - self.text_0_timer > 100 and self.initial_timer_done and self.text == 0 or self.current_frame == 1:
            self.text_0_char += 1
            self.text_0_timer = self.ticks

        if self.text_0_char >= 0 and self.initial_timer_done and self.text == 0 or self.current_frame == 1:
            display.blit(self.dialog_box, (0, 0))
            display.blit(pygame.font.Font.render(self.font, self.text_0[0:self.text_0_char], False, (255, 255, 255)), (3, 120))
            if self.text_0_char == len(self.text_0):
                self.text = 1

        #text 1

        if self.text == 1 and not self.text_1_begun:
            self.text_1_char = 0
            self.text_1_timer = self.ticks
            self.text_1_begun = True

        if self.text_1_char >= 0 and self.ticks - self.text_1_timer > 100 and self.text_1_begun and self.text == 1:
            self.text_1_char += 1
            self.text_1_timer = self.ticks

        if self.text_1_char >= 0 and self.text_1_begun and self.text == 1:
            display.blit(self.dialog_box, (0, 0))
            display.blit(pygame.font.Font.render(self.font, self.text_1[0:self.text_1_char], False, (255, 255, 255)), (3, 137))
            if self.text_1_char == len(self.text_1):
                self.text = 2