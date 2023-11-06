import pygame

from utils import Interactable
from utils import ToolBar, Tool
from dataclasses import dataclass


class EndCutscene:
    def __init__(self, display: pygame.Surface):
        
        self.frames: list[pygame.Surface] = [
            pygame.transform.scale(pygame.image.load("Assets/cutscenes/rocket_done.png").convert_alpha(), (200, 150)),
            pygame.image.load("Assets/cutscenes/rocket_inside.png").convert_alpha(),
            pygame.image.load("Assets/cutscenes/choice.png").convert_alpha()
        ]

        self.backgrounds: list[pygame.Surface] = [
            pygame.image.load("Assets/cutscenes/earth.png").convert_alpha(),
            pygame.image.load("Assets/cutscenes/space.png").convert_alpha(),
            pygame.image.load("Assets/cutscenes/meteorite_front.png").convert_alpha()
        ]

        self.dialog_box = pygame.image.load("Assets/sprites/dialog_box.png").convert_alpha()

        self.font = pygame.font.Font("Assets/fonts/LcdSolid.ttf", 12)

        self.current_frame = 0

        self.button: Interactable = Interactable((0, 0), (200, 150))
        self.waiting = False
        self.choice = False

        self.text = 0

        self.text_0 = "...and DONE! Just in time.   "
        self.text_0_char = False
        self.text_0_timer = 0
        self.text_0_complete = False

        self.text_1 = "Now I just need to  "
        self.text_1_char = False
        self.text_1_timer = 0
        self.text_1_begun = False
        self.text_1_complete = False
        
        self.initial_timer = False
        self.initial_timer_done = False

    def draw(self, dt: float, display: pygame.Surface) -> None:
        
        display.fill((0, 0, 0))
        if self.current_frame == 1:
            display.blit(self.frames[2], (0, 0))
        display.blit(self.frames[self.current_frame], (0, 0))
        if self.choice:
            display.blit(self.frames[2], (0, 0))

    def play(self, dt: float, tool_bar: ToolBar, display: pygame.Surface, mouse_pos: tuple,
             interaction_starter: bool) -> None:
        
        self.ticks = pygame.time.get_ticks()
        
        if not self.choice:
            self.button.update(mouse_pos, interaction_starter)
        else:
            pass

        self.draw(dt, display)

        if self.initial_timer == False:
            self.initial_timer = pygame.time.get_ticks()

        if self.waiting:
            if self.button.is_clicked:
                self.waiting = False

        if self.current_frame == 0 and self.ticks - self.initial_timer > 2200 and not self.initial_timer_done and self.text == 0:
            self.text_0_char = 0
            self.text_0_timer = self.ticks
            self.initial_timer_done = True

        if self.text_0_char >= 0 and self.ticks - self.text_0_timer > 100 and self.initial_timer_done and self.text == 0 or self.text == 1:
            self.text_0_char += 1
            self.text_0_timer = self.ticks

        if self.text_0_char >= 0 and self.initial_timer_done and self.text == 0 or self.text == 1:
            display.blit(self.dialog_box, (0, 0))
            display.blit(pygame.font.Font.render(self.font, self.text_0[0:self.text_0_char], False, (255, 255, 255)), (3, 120))
            if self.text_0_char == len(self.text_0):
                self.waiting = True
                self.text_0_complete = True
        if self.text == 0 and not self.waiting and self.text_0_complete:
            self.text = 1
            self.text_0_timer = self.ticks
        
        #text 1

        if self.text == 3 and not self.text_3_begun:
            self.text_3_char = 0
            self.text_3_timer = self.ticks
            self.text_3_begun = True

        if self.text_3_char >= 0 and self.ticks - self.text_3_timer > 100 and self.text_3_begun and self.text == 3 and not self.waiting:
            self.text_3_char += 1
            self.text_3_timer = self.ticks

        if self.text_3_char >= 0 and self.text_3_begun and self.text == 3:
            display.blit(pygame.font.Font.render(self.font, self.text_3[0:self.text_3_char], False, (255, 255, 255)),
                         (3, 137))
            if self.text_3_char == len(self.text_3):
                self.waiting = True
                self.text_3_complete = True

        if self.text == 3 and not self.waiting and self.text_3_complete:
            self.text = 4