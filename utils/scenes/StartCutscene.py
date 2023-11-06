import pygame

import time

from utils import Interactable
from utils import ToolBar, Tool
from dataclasses import dataclass


class StartCutscene:
    def __init__(self, display: pygame.Surface):
        self.end_won: bool = False

        self.frames: list[pygame.Surface] = [
            pygame.image.load("Assets/cutscenes/research_institute.png").convert_alpha(),
            pygame.image.load("Assets/cutscenes/folder.png").convert_alpha(),
            pygame.transform.scale(pygame.image.load("Assets/cutscenes/notepad.png").convert_alpha(), (200, 150)),
            pygame.transform.scale(pygame.image.load("Assets/cutscenes/meteorite.png").convert_alpha(), (200, 150)),
            pygame.transform.scale(pygame.image.load("Assets/cutscenes/rocket.png").convert_alpha(), (200, 150))
        ]

        self.dialog_box = pygame.image.load("Assets/sprites/dialog_box.png").convert_alpha()

        self.select_sound = pygame.mixer.Sound("Assets/sound_effects/select.wav")

        self.font = pygame.font.Font("Assets/fonts/LcdSolid.ttf", 12)

        self.current_frame = 0

        self.button: Interactable = Interactable((0, 0), (200, 150))
        self.waiting = False

        self.text = 0

        self.text_0 = "You're a worker at NASA,   "
        self.text_0_char = False
        self.text_0_timer = 0

        self.text_1 = "Glenn Research Center.   "
        self.text_1_char = False
        self.text_1_timer = 0
        self.text_1_begun = False
        self.text_1_complete = False

        self.text_2 = "Your team calculated, that  "
        self.text_2_char = False
        self.text_2_timer = 0
        self.text_2_begun = False

        self.text_3 = "Earth will get hit by a...   "
        self.text_3_char = False
        self.text_3_timer = 0
        self.text_3_begun = False
        self.text_3_complete = False

        self.text_4 = "...meteorite in the next 10  "
        self.text_4_char = False
        self.text_4_timer = 0
        self.text_4_begun = False

        self.text_5 = "years.       "
        self.text_5_char = False
        self.text_5_timer = 0
        self.text_5_begun = False
        self.text_5_complete = False

        self.text_6 = "To keep chaos at minimum,"
        self.text_6_char = False
        self.text_6_timer = 0
        self.text_6_begun = False

        self.text_7 = "the goverment decided to...       "
        self.text_7_char = False
        self.text_7_timer = 0
        self.text_7_begun = False
        self.text_7_complete = False

        self.text_8 = "...keep this information "
        self.text_8_char = False
        self.text_8_timer = 0
        self.text_8_begun = False

        self.text_9 = "private.       "
        self.text_9_char = False
        self.text_9_timer = 0
        self.text_9_begun = False
        self.text_9_complete = False

        self.text_10 = "It's late at work and  "
        self.text_10_char = False
        self.text_10_timer = 0
        self.text_10_begun = False

        self.text_11 = "everyone has already left.       "
        self.text_11_char = False
        self.text_11_timer = 0
        self.text_11_begun = False
        self.text_11_complete = False

        self.text_12 = "You go over the calcula-"
        self.text_12_char = False
        self.text_12_timer = 0
        self.text_12_begun = False

        self.text_13 = "tions and realise...    "
        self.text_13_char = False
        self.text_13_timer = 0
        self.text_13_begun = False
        self.text_13_complete = False

        self.text_14 = "T... T... This cant be"
        self.text_14_char = False
        self.text_14_timer = 0
        self.text_14_begun = False

        self.text_15 = "right!   "
        self.text_15_char = False
        self.text_15_timer = 0
        self.text_15_begun = False
        self.text_15_complete = False

        self.text_16 = "Your team was wrong"
        self.text_16_char = False
        self.text_16_timer = 0
        self.text_16_begun = False

        self.text_17 = "this entire time.   "
        self.text_17_char = False
        self.text_17_timer = 0
        self.text_17_begun = False
        self.text_17_complete = False

        self.text_18 = "The impact will actually"
        self.text_18_char = False
        self.text_18_timer = 0
        self.text_18_begun = False

        self.text_19 = "happen in <24 hours.   "
        self.text_19_char = False
        self.text_19_timer = 0
        self.text_19_begun = False
        self.text_19_complete = False

        self.text_20 = "I have to do something!    "
        self.text_20_char = False
        self.text_20_timer = 0
        self.text_20_begun = False

        self.text_21 = "What if i...   "
        self.text_21_char = False
        self.text_21_timer = 0
        self.text_21_begun = False
        self.text_21_complete = False

        self.text_22 = "You decide to use the new"
        self.text_22_char = False
        self.text_22_timer = 0
        self.text_22_begun = False

        self.text_23 = "but unfinished rocket.   "
        self.text_23_char = False
        self.text_23_timer = 0
        self.text_23_begun = False
        self.text_23_complete = False

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

        if self.waiting:
            if self.button.is_clicked:
                self.waiting = False
                self.select_sound.play(0)

        if self.current_frame == 0 and self.ticks - self.initial_timer > 2200 and not self.initial_timer_done and self.text == 0:
            self.text_0_char = 0
            self.text_0_timer = self.ticks
            self.initial_timer_done = True

        if self.text_0_char >= 0 and self.ticks - self.text_0_timer > 100 and self.initial_timer_done and self.text == 0 or self.text == 1:
            self.text_0_char += 1
            self.text_0_timer = self.ticks

        if self.text_0_char >= 0 and self.initial_timer_done and self.text == 0 or self.text == 1:
            display.blit(self.dialog_box, (0, 0))
            display.blit(pygame.font.Font.render(self.font, self.text_0[0:self.text_0_char], False, (255, 255, 255)),
                         (3, 120))
            if self.text_0_char == len(self.text_0):
                self.text = 1

        # text 1

        if self.text == 1 and not self.text_1_begun:
            self.text_1_char = 0
            self.text_1_timer = self.ticks
            self.text_1_begun = True

        if self.text_1_char >= 0 and self.ticks - self.text_1_timer > 100 and self.text_1_begun and self.text == 1 and not self.waiting:
            self.text_1_char += 1
            self.text_1_timer = self.ticks

        if self.text_1_char >= 0 and self.text_1_begun and self.text == 1:
            display.blit(pygame.font.Font.render(self.font, self.text_1[0:self.text_1_char], False, (255, 255, 255)),
                         (3, 137))
            if self.text_1_char == len(self.text_1):
                self.waiting = True
                self.text_1_complete = True

        if self.text == 1 and not self.waiting and self.text_1_complete:
            self.text = 2

        # text 2

        if self.text == 2 and not self.text_2_begun and not self.waiting:
            self.current_frame = 1
            self.text_2_char = 0
            self.text_2_timer = self.ticks
            self.text_2_begun = True

        if self.text_2_char >= 0 and self.ticks - self.text_2_timer > 100 and self.text_2_begun and self.text == 2:
            self.text_2_char += 1
            self.text_2_timer = self.ticks

        if self.text_2_char >= 0 and self.text_2_begun and self.text == 2 or self.text == 3:
            display.blit(self.dialog_box, (0, 0))
            display.blit(pygame.font.Font.render(self.font, self.text_2[0:self.text_2_char], False, (255, 255, 255)),
                         (3, 120))
            if self.text_2_char == len(self.text_2):
                self.text = 3

        # text 3

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

        # text 4

        if self.text == 4 and not self.text_4_begun and not self.waiting:
            self.current_frame = 1
            self.text_4_char = 0
            self.text_4_timer = self.ticks
            self.text_4_begun = True

        if self.text_4_char >= 0 and self.ticks - self.text_4_timer > 100 and self.text_4_begun and self.text == 4:
            self.text_4_char += 1
            self.text_4_timer = self.ticks

        if self.text_4_char >= 0 and self.text_4_begun and self.text == 4 or self.text == 5:
            display.blit(self.dialog_box, (0, 0))
            display.blit(pygame.font.Font.render(self.font, self.text_4[0:self.text_4_char], False, (255, 255, 255)),
                         (3, 120))
            if self.text_4_char == len(self.text_4):
                self.text = 5

        # text 5

        if self.text == 5 and not self.text_5_begun:
            self.text_5_char = 0
            self.text_5_timer = self.ticks
            self.text_5_begun = True

        if self.text_5_char >= 0 and self.ticks - self.text_5_timer > 100 and self.text_5_begun and self.text == 5 and not self.waiting:
            self.text_5_char += 1
            self.text_5_timer = self.ticks

        if self.text_5_char >= 0 and self.text_5_begun and self.text == 5:
            display.blit(pygame.font.Font.render(self.font, self.text_5[0:self.text_5_char], False, (255, 255, 255)),
                         (3, 137))
            if self.text_5_char == len(self.text_5):
                self.waiting = True
                self.text_5_complete = True

        if self.text == 5 and not self.waiting and self.text_5_complete:
            self.text = 6

        # text 6

        if self.text == 6 and not self.text_6_begun and not self.waiting:
            self.current_frame = 1
            self.text_6_char = 0
            self.text_6_timer = self.ticks
            self.text_6_begun = True

        if self.text_6_char >= 0 and self.ticks - self.text_6_timer > 100 and self.text_6_begun and self.text == 6:
            self.text_6_char += 1
            self.text_6_timer = self.ticks

        if self.text_6_char >= 0 and self.text_6_begun and self.text == 6 or self.text == 7:
            display.blit(self.dialog_box, (0, 0))
            display.blit(pygame.font.Font.render(self.font, self.text_6[0:self.text_6_char], False, (255, 255, 255)),
                         (3, 120))
            if self.text_6_char == len(self.text_6):
                self.text = 7

        # text 7

        if self.text == 7 and not self.text_7_begun:
            self.text_7_char = 0
            self.text_7_timer = self.ticks
            self.text_7_begun = True

        if self.text_7_char >= 0 and self.ticks - self.text_7_timer > 100 and self.text_7_begun and self.text == 7 and not self.waiting:
            self.text_7_char += 1
            self.text_7_timer = self.ticks

        if self.text_7_char >= 0 and self.text_7_begun and self.text == 7:
            display.blit(pygame.font.Font.render(self.font, self.text_7[0:self.text_7_char], False, (255, 255, 255)),
                         (3, 137))
            if self.text_7_char == len(self.text_7):
                self.waiting = True
                self.text_7_complete = True

        if self.text == 7 and not self.waiting and self.text_7_complete:
            self.text = 8

        # text 8

        if self.text == 8 and not self.text_8_begun and not self.waiting:
            self.current_frame = 1
            self.text_8_char = 0
            self.text_8_timer = self.ticks
            self.text_8_begun = True

        if self.text_8_char >= 0 and self.ticks - self.text_8_timer > 100 and self.text_8_begun and self.text == 8:
            self.text_8_char += 1
            self.text_8_timer = self.ticks

        if self.text_8_char >= 0 and self.text_8_begun and self.text == 8 or self.text == 9:
            display.blit(self.dialog_box, (0, 0))
            display.blit(pygame.font.Font.render(self.font, self.text_8[0:self.text_8_char], False, (255, 255, 255)),
                         (3, 120))
            if self.text_8_char == len(self.text_8):
                self.text = 9

        # text 9

        if self.text == 9 and not self.text_9_begun:
            self.text_9_char = 0
            self.text_9_timer = self.ticks
            self.text_9_begun = True

        if self.text_9_char >= 0 and self.ticks - self.text_9_timer > 100 and self.text_9_begun and self.text == 9 and not self.waiting:
            self.text_9_char += 1
            self.text_9_timer = self.ticks

        if self.text_9_char >= 0 and self.text_9_begun and self.text == 9:
            display.blit(pygame.font.Font.render(self.font, self.text_9[0:self.text_9_char], False, (255, 255, 255)),
                         (3, 137))
            if self.text_9_char == len(self.text_9):
                self.waiting = True
                self.text_9_complete = True

        if self.text == 9 and not self.waiting and self.text_9_complete:
            self.text = 10

        # text 10

        if self.text == 10 and not self.text_10_begun and not self.waiting:
            self.current_frame = 2
            self.text_10_char = 0
            self.text_10_timer = self.ticks
            self.text_10_begun = True

        if self.text_10_char >= 0 and self.ticks - self.text_10_timer > 100 and self.text_10_begun and self.text == 10:
            self.text_10_char += 1
            self.text_10_timer = self.ticks

        if self.text_10_char >= 0 and self.text_10_begun and self.text == 10 or self.text == 11:
            display.blit(self.dialog_box, (0, 0))
            display.blit(pygame.font.Font.render(self.font, self.text_10[0:self.text_10_char], False, (255, 255, 255)),
                         (3, 120))
            if self.text_10_char == len(self.text_10):
                self.text = 11

        # text 11

        if self.text == 11 and not self.text_11_begun:
            self.text_11_char = 0
            self.text_11_timer = self.ticks
            self.text_11_begun = True

        if self.text_11_char >= 0 and self.ticks - self.text_11_timer > 100 and self.text_11_begun and self.text == 11 and not self.waiting:
            self.text_11_char += 1
            self.text_11_timer = self.ticks

        if self.text_11_char >= 0 and self.text_11_begun and self.text == 11:
            display.blit(pygame.font.Font.render(self.font, self.text_11[0:self.text_11_char], False, (255, 255, 255)),
                         (3, 137))
            if self.text_11_char == len(self.text_11):
                self.waiting = True
                self.text_11_complete = True

        if self.text == 11 and not self.waiting and self.text_11_complete:
            self.text = 12

        # text 12

        if self.text == 12 and not self.text_12_begun and not self.waiting:
            self.current_frame = 2
            self.text_12_char = 0
            self.text_12_timer = self.ticks
            self.text_12_begun = True

        if self.text_12_char >= 0 and self.ticks - self.text_12_timer > 100 and self.text_12_begun and self.text == 12:
            self.text_12_char += 1
            self.text_12_timer = self.ticks

        if self.text_12_char >= 0 and self.text_12_begun and self.text == 12 or self.text == 13:
            display.blit(self.dialog_box, (0, 0))
            display.blit(pygame.font.Font.render(self.font, self.text_12[0:self.text_12_char], False, (255, 255, 255)),
                         (3, 120))
            if self.text_12_char == len(self.text_12):
                self.text = 13

        # text 13

        if self.text == 13 and not self.text_13_begun:
            self.text_13_char = 0
            self.text_13_timer = self.ticks
            self.text_13_begun = True

        if self.text_13_char >= 0 and self.ticks - self.text_13_timer > 100 and self.text_13_begun and self.text == 13 and not self.waiting:
            self.text_13_char += 1
            self.text_13_timer = self.ticks

        if self.text_13_char >= 0 and self.text_13_begun and self.text == 13:
            display.blit(pygame.font.Font.render(self.font, self.text_13[0:self.text_13_char], False, (255, 255, 255)),
                         (3, 137))
            if self.text_13_char == len(self.text_13):
                self.waiting = True
                self.text_13_complete = True

        if self.text == 13 and not self.waiting and self.text_13_complete:
            self.text = 14

        # text 14

        if self.text == 14 and not self.text_14_begun and not self.waiting:
            self.current_frame = 2
            self.text_14_char = 0
            self.text_14_timer = self.ticks
            self.text_14_begun = True

        if self.text_14_char >= 0 and self.ticks - self.text_14_timer > 100 and self.text_14_begun and self.text == 14:
            self.text_14_char += 1
            self.text_14_timer = self.ticks

        if self.text_14_char >= 0 and self.text_14_begun and self.text == 14 or self.text == 15:
            display.blit(self.dialog_box, (0, 0))
            display.blit(pygame.font.Font.render(self.font, self.text_14[0:self.text_14_char], False, (255, 255, 255)),
                         (3, 120))
            if self.text_14_char == len(self.text_14):
                self.text = 15

        # text 15

        if self.text == 15 and not self.text_15_begun:
            self.text_15_char = 0
            self.text_15_timer = self.ticks
            self.text_15_begun = True

        if self.text_15_char >= 0 and self.ticks - self.text_15_timer > 100 and self.text_15_begun and self.text == 15 and not self.waiting:
            self.text_15_char += 1
            self.text_15_timer = self.ticks

        if self.text_15_char >= 0 and self.text_15_begun and self.text == 15:
            display.blit(pygame.font.Font.render(self.font, self.text_15[0:self.text_15_char], False, (255, 255, 255)),
                         (3, 137))
            if self.text_15_char == len(self.text_15):
                self.waiting = True
                self.text_15_complete = True

        if self.text == 15 and not self.waiting and self.text_15_complete:
            self.text = 16

        # text 16

        if self.text == 16 and not self.text_16_begun and not self.waiting:
            self.current_frame = 3
            self.text_16_char = 0
            self.text_16_timer = self.ticks
            self.text_16_begun = True

        if self.text_16_char >= 0 and self.ticks - self.text_16_timer > 100 and self.text_16_begun and self.text == 16:
            self.text_16_char += 1
            self.text_16_timer = self.ticks

        if self.text_16_char >= 0 and self.text_16_begun and self.text == 16 or self.text == 17:
            display.blit(self.dialog_box, (0, 0))
            display.blit(pygame.font.Font.render(self.font, self.text_16[0:self.text_16_char], False, (255, 255, 255)),
                         (3, 120))
            if self.text_16_char == len(self.text_16):
                self.text = 17

        # text 17

        if self.text == 17 and not self.text_17_begun:
            self.text_17_char = 0
            self.text_17_timer = self.ticks
            self.text_17_begun = True

        if self.text_17_char >= 0 and self.ticks - self.text_17_timer > 100 and self.text_17_begun and self.text == 17 and not self.waiting:
            self.text_17_char += 1
            self.text_17_timer = self.ticks

        if self.text_17_char >= 0 and self.text_17_begun and self.text == 17:
            display.blit(pygame.font.Font.render(self.font, self.text_17[0:self.text_17_char], False, (255, 255, 255)),
                         (3, 137))
            if self.text_17_char == len(self.text_17):
                self.waiting = True
                self.text_17_complete = True

        if self.text == 17 and not self.waiting and self.text_17_complete:
            self.text = 18

        # text 18

        if self.text == 18 and not self.text_18_begun and not self.waiting:
            self.current_frame = 3
            self.text_18_char = 0
            self.text_18_timer = self.ticks
            self.text_18_begun = True

        if self.text_18_char >= 0 and self.ticks - self.text_18_timer > 100 and self.text_18_begun and self.text == 18:
            self.text_18_char += 1
            self.text_18_timer = self.ticks

        if self.text_18_char >= 0 and self.text_18_begun and self.text == 18 or self.text == 19:
            display.blit(self.dialog_box, (0, 0))
            display.blit(pygame.font.Font.render(self.font, self.text_18[0:self.text_18_char], False, (255, 255, 255)),
                         (3, 120))
            if self.text_18_char == len(self.text_18):
                self.text = 19

        # text 19

        if self.text == 19 and not self.text_19_begun:
            self.text_19_char = 0
            self.text_19_timer = self.ticks
            self.text_19_begun = True

        if self.text_19_char >= 0 and self.ticks - self.text_19_timer > 100 and self.text_19_begun and self.text == 19 and not self.waiting:
            self.text_19_char += 1
            self.text_19_timer = self.ticks

        if self.text_19_char >= 0 and self.text_19_begun and self.text == 19:
            display.blit(pygame.font.Font.render(self.font, self.text_19[0:self.text_19_char], False, (255, 255, 255)),
                         (3, 137))
            if self.text_19_char == len(self.text_19):
                self.waiting = True
                self.text_19_complete = True

        if self.text == 19 and not self.waiting and self.text_19_complete:
            self.text = 20

        # text 20

        if self.text == 20 and not self.text_20_begun and not self.waiting:
            self.current_frame = 2
            self.text_20_char = 0
            self.text_20_timer = self.ticks
            self.text_20_begun = True

        if self.text_20_char >= 0 and self.ticks - self.text_20_timer > 100 and self.text_20_begun and self.text == 20:
            self.text_20_char += 1
            self.text_20_timer = self.ticks

        if self.text_20_char >= 0 and self.text_20_begun and self.text == 20 or self.text == 21:
            display.blit(self.dialog_box, (0, 0))
            display.blit(pygame.font.Font.render(self.font, self.text_20[0:self.text_20_char], False, (255, 255, 255)),
                         (3, 120))
            if self.text_20_char == len(self.text_20):
                self.text = 21

        # text 21

        if self.text == 21 and not self.text_21_begun:
            self.text_21_char = 0
            self.text_21_timer = self.ticks
            self.text_21_begun = True

        if self.text_21_char >= 0 and self.ticks - self.text_21_timer > 100 and self.text_21_begun and self.text == 21 and not self.waiting:
            self.text_21_char += 1
            self.text_21_timer = self.ticks

        if self.text_21_char >= 0 and self.text_21_begun and self.text == 21:
            display.blit(pygame.font.Font.render(self.font, self.text_21[0:self.text_21_char], False, (255, 255, 255)),
                         (3, 137))
            if self.text_21_char == len(self.text_21):
                self.waiting = True
                self.text_21_complete = True

        if self.text == 21 and not self.waiting and self.text_21_complete:
            self.text = 22

        # text 22

        if self.text == 22 and not self.text_22_begun and not self.waiting:
            self.current_frame = 4
            self.text_22_char = 0
            self.text_22_timer = self.ticks
            self.text_22_begun = True

        if self.text_22_char >= 0 and self.ticks - self.text_22_timer > 100 and self.text_22_begun and self.text == 22:
            self.text_22_char += 1
            self.text_22_timer = self.ticks

        if self.text_22_char >= 0 and self.text_22_begun and self.text == 22 or self.text == 23:
            display.blit(self.dialog_box, (0, 0))
            display.blit(pygame.font.Font.render(self.font, self.text_22[0:self.text_22_char], False, (255, 255, 255)),
                         (3, 120))
            if self.text_22_char == len(self.text_22):
                self.text = 23

        # text 23

        if self.text == 23 and not self.text_23_begun:
            self.text_23_char = 0
            self.text_23_timer = self.ticks
            self.text_23_begun = True

        if self.text_23_char >= 0 and self.ticks - self.text_23_timer > 100 and self.text_23_begun and self.text == 23 and not self.waiting:
            self.text_23_char += 1
            self.text_23_timer = self.ticks

        if self.text_23_char >= 0 and self.text_23_begun and self.text == 23:
            display.blit(pygame.font.Font.render(self.font, self.text_23[0:self.text_23_char], False, (255, 255, 255)),
                         (3, 137))
            if self.text_23_char == len(self.text_23):
                self.waiting = True
                self.text_23_complete = True

        if self.text == 23 and not self.waiting and self.text_23_complete:
            self.end_won = True