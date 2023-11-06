import pygame

from utils import Interactable
from utils import ToolBar, Tool
from dataclasses import dataclass


class EndCutscene:
    def __init__(self, display: pygame.Surface):
        
        self.init_was_played: bool = False
        
        self.end_won = False
        
        self.select_sound = pygame.mixer.Sound("Assets/sound_effects/select.wav")
        
        self.frames: list[pygame.Surface] = [
            pygame.transform.scale(pygame.image.load("Assets/cutscenes/rocket_done.png").convert_alpha(), (200, 150)),
            pygame.image.load("Assets/cutscenes/rocket_inside.png").convert_alpha(),
            pygame.image.load("Assets/cutscenes/choice.png").convert_alpha(),
            pygame.image.load("Assets/cutscenes/blank.png").convert_alpha()
        ]

        self.backgrounds: list[pygame.Surface] = [
            pygame.image.load("Assets/cutscenes/earth.png").convert_alpha(),
            pygame.image.load("Assets/cutscenes/space.png").convert_alpha(),
            pygame.image.load("Assets/cutscenes/meteorite_front.png").convert_alpha()
        ]

        self.meteorite: list[pygame.Surface] = [
            pygame.image.load("Assets/cutscenes/meteorite_front_0.png").convert_alpha(),
            pygame.image.load("Assets/cutscenes/meteorite_front_1.png").convert_alpha(),
            pygame.image.load("Assets/cutscenes/meteorite_front.png").convert_alpha()
        ]

        self.dialog_box = pygame.image.load("Assets/sprites/dialog_box.png").convert_alpha()

        self.font = pygame.font.Font("Assets/fonts/LcdSolid.ttf", 12)

        self.current_frame = 0
        self.background = 0

        self.button: Interactable = Interactable((0, 0), (200, 150))
        self.button_autopilot: Interactable = Interactable((0, 0), (100, 150))
        self.button_manual: Interactable = Interactable((100, 0), (100, 150))
        self.waiting = False
        self.choice = False
        self.is_meteorite = False
        self.meteorite_stage = 0

        self.text = 0

        self.text_0 = "...and DONE! Just in time.   "
        self.text_0_char = False
        self.text_0_timer = 0
        self.text_0_complete = False
        self.text_0_begun = False

        self.text_1 = "Now I just need to  "
        self.text_1_char = False
        self.text_1_timer = 0
        self.text_1_begun = False

        self.text_2 = "choose between...   "
        self.text_2_char = False
        self.text_2_timer = 0
        self.text_2_complete = False
        self.text_2_begun = False

        self.text_3 = "...autopilot and manual"
        self.text_3_char = False
        self.text_3_timer = 0
        self.text_3_begun = False

        self.text_4 = "drive. "
        self.text_4_char = False
        self.text_4_timer = 0
        self.text_4_complete = False
        self.text_4_begun = False

        self.text_5_begun = False

        self.text_10 = "I've always trusted "
        self.text_10_char = False
        self.text_10_timer = 0
        self.text_10_begun = False

        self.text_11 = "the autopilot. "
        self.text_11_char = False
        self.text_11_timer = 0
        self.text_11_complete = False
        self.text_11_begun = False

        self.text_12_timer = 0
        self.text_12_complete = False
        self.text_12_begun = False

        self.text_13_timer = 0
        self.text_13_complete = False
        self.text_13_begun = False
        
        self.initial_timer = False
        self.initial_timer_done = False
        self.choice_timer = 0

        self.text_14 = "Wow, I hope I brought"
        self.text_14_char = False
        self.text_14_timer = 0
        self.text_14_begun = False

        self.text_15 = "enough supplies..."
        self.text_15_char = False
        self.text_15_timer = 0
        self.text_15_complete = False
        self.text_15_begun = False

        self.text_20 = "I can do this, "
        self.text_20_char = False
        self.text_20_timer = 0
        self.text_20_begun = False

        self.text_21 = "let's go! "
        self.text_21_char = False
        self.text_21_timer = 0
        self.text_21_complete = False
        self.text_21_begun = False

        self.text_22_timer = 0
        self.text_22_complete = False
        self.text_22_begun = False

        self.text_23_timer = 0
        self.text_23_complete = False
        self.text_23_begun = False

        self.text_24 = "Oh no,                     "
        self.text_24_char = False
        self.text_24_timer = 0
        self.text_24_begun = False

        self.text_25 = "MAYDAY! MAYDAY! MAYDAY!    "
        self.text_25_char = False
        self.text_25_timer = 0
        self.text_25_complete = False
        self.text_25_begun = False
        
    @staticmethod
    def init():
        pygame.mixer.music.load("Assets/music/background-MainMenu.wav")
        pygame.mixer.music.play(-1)
        
        
    def draw(self, dt: float, display: pygame.Surface) -> None:
        
        display.fill((0, 0, 0))
        if self.background == 1:
            display.blit(self.backgrounds[0], (0, 0))
        elif self.background == 2:
            display.blit(self.backgrounds[1], (0, 0))
        if self.is_meteorite:
            display.blit(self.meteorite[self.meteorite_stage], (0, 0))
        display.blit(self.frames[self.current_frame], (0, 0))
        if self.choice:
            display.blit(self.frames[2], (0, 0))

    def play(self, dt: float, tool_bar: ToolBar, display: pygame.Surface, mouse_pos: tuple,
             interaction_starter: bool) -> None:
        
        if not self.init_was_played:
            self.init()
            self.init_was_played = True
        
        self.ticks = pygame.time.get_ticks()
        
        if not self.choice:
            self.button.update(mouse_pos, interaction_starter)
        else:
            self.button_autopilot.update(mouse_pos, interaction_starter)
            self.button_manual.update(mouse_pos, interaction_starter)

        self.draw(dt, display)

        if self.initial_timer == False:
            self.initial_timer = pygame.time.get_ticks()

        if self.waiting:
            if not self.choice:
                if self.button.is_clicked:
                    self.waiting = False
                    self.select_sound.play(0)
            else:
                if self.ticks - self.choice_timer > 400:
                    if self.button_autopilot.is_clicked:
                        self.waiting = False
                        self.ending = 1
                    if self.button_manual.is_clicked:
                        self.waiting = False
                        self.ending = 2

        if self.current_frame == 0 and self.ticks - self.initial_timer > 2200 and not self.initial_timer_done and self.text == 0:
            self.text_0_char = 0
            self.text_0_timer = self.ticks
            self.initial_timer_done = True

        if self.text_0_char >= 0 and self.ticks - self.text_0_timer > 100 and self.initial_timer_done and self.text == 0 or self.text == 1:
            self.text_0_char += 1
            self.text_0_timer = self.ticks

        if self.text_0_char >= 0 and self.initial_timer_done and self.text == 0:
            display.blit(self.dialog_box, (0, 0))
            display.blit(pygame.font.Font.render(self.font, self.text_0[0:self.text_0_char], False, (255, 255, 255)), (3, 120))
            if self.text_0_char == len(self.text_0):
                self.waiting = True
                self.text_0_complete = True
        if self.text == 0 and not self.waiting and self.text_0_complete:
            self.text = 1
        
        #text 1

        if self.text == 1 and not self.text_1_begun and not self.waiting:
            self.current_frame = 1
            self.background = 1
            self.text_1_char = 0
            self.text_1_timer = self.ticks
            self.text_1_begun = True

        if self.text_1_char >= 0 and self.ticks - self.text_1_timer > 100 and self.text_1_begun and self.text == 1:
            self.text_1_char += 1
            self.text_1_timer = self.ticks

        if self.text_1_char >= 0 and self.text_1_begun and self.text == 1 or self.text == 2:
            display.blit(self.dialog_box, (0, 0))
            display.blit(pygame.font.Font.render(self.font, self.text_1[0:self.text_1_char], False, (255, 255, 255)),
                         (3, 120))
            if self.text_1_char == len(self.text_1):
                self.text = 2

        #text 2

        if self.text == 2 and not self.text_2_begun:
            self.text_2_char = 0
            self.text_2_timer = self.ticks
            self.text_2_begun = True

        if self.text_2_char >= 0 and self.ticks - self.text_2_timer > 100 and self.text_2_begun and self.text == 2 and not self.waiting:
            self.text_2_char += 1
            self.text_2_timer = self.ticks

        if self.text_2_char >= 0 and self.text_2_begun and self.text == 2:
            display.blit(pygame.font.Font.render(self.font, self.text_2[0:self.text_2_char], False, (255, 255, 255)),
                         (3, 137))
            if self.text_2_char == len(self.text_2):
                self.waiting = True
                self.text_2_complete = True

        if self.text == 2 and not self.waiting and self.text_2_complete:
            self.text = 3
        
        #text 3

        if self.text == 3 and not self.text_3_begun and not self.waiting:
            self.current_frame = 1
            self.background = 1
            self.text_3_char = 0
            self.text_3_timer = self.ticks
            self.text_3_begun = True

        if self.text_3_char >= 0 and self.ticks - self.text_3_timer > 100 and self.text_3_begun and self.text == 3:
            self.text_3_char += 1
            self.text_3_timer = self.ticks

        if self.text_3_char >= 0 and self.text_3_begun and self.text == 3 or self.text == 4:
            display.blit(self.dialog_box, (0, 0))
            display.blit(pygame.font.Font.render(self.font, self.text_3[0:self.text_3_char], False, (255, 255, 255)),
                         (3, 120))
            if self.text_3_char == len(self.text_3):
                self.text = 4

        #text 4

        if self.text == 4 and not self.text_4_begun:
            self.text_4_char = 0
            self.text_4_timer = self.ticks
            self.text_4_begun = True

        if self.text_4_char >= 0 and self.ticks - self.text_4_timer > 100 and self.text_4_begun and self.text == 4 and not self.waiting:
            self.text_4_char += 1
            self.text_4_timer = self.ticks

        if self.text_4_char >= 0 and self.text_4_begun and self.text == 4:
            display.blit(pygame.font.Font.render(self.font, self.text_4[0:self.text_4_char], False, (255, 255, 255)),
                         (3, 137))
            if self.text_4_char == len(self.text_4):
                self.waiting = True
                self.text_4_complete = True

        if self.text == 4 and not self.waiting and self.text_4_complete:
            self.text = 5

        #choice
        
        if self.text == 5 and not self.text_5_begun:
            self.choice = True
            self.text_5_begun = True
            self.waiting = True
            self.choice_timer = self.ticks
        
        if self.text == 5 and self.text_5_begun and not self.waiting:
            if self.ending == 1:
                self.choice = False
                self.text = 10
            if self.ending == 2:
                self.choice = False
                self.text = 20
        
        #ending 1

        if self.text == 10 and not self.text_10_begun and not self.waiting:
            self.current_frame = 1
            self.background = 1
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
        
        #text 11

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
        
        #text 12

        if self.text == 12 and not self.text_12_begun:
            self.current_frame = 1
            self.text_12_timer = self.ticks
            self.text_12_begun = True
        
        if self.ticks - self.text_12_timer > 1700 and self.text_12_begun and self.text == 12:
            self.current_frame = 3
            self.background = 1
            self.text = 13

        #text 13

        if self.text == 13 and not self.text_13_begun:
            self.text_13_timer = self.ticks
            self.text_13_begun = True

        if self.ticks - self.text_13_timer > 3000 and self.text_13_begun and self.text == 13:
            self.current_frame = 1
            self.background = 2
            self.text = 14
        
        #text 14

        if self.text == 14 and not self.text_14_begun and not self.waiting:
            self.current_frame = 1
            self.background = 2
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
        
        #text 15

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

        if self.text == 16:
            display.blit(pygame.image.load("Assets/cutscenes/ending_1.png").convert_alpha(), (0, 0))
        
        #ending 2

        if self.text == 20 and not self.text_20_begun and not self.waiting:
            self.current_frame = 1
            self.background = 1
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
            if self.text_20_char == len(self.text_10):
                self.text = 21
        
        #text 21

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
        
        #text 22

        if self.text == 22 and not self.text_22_begun:
            self.current_frame = 1
            self.text_22_timer = self.ticks
            self.text_22_begun = True
        
        if self.ticks - self.text_22_timer > 1700 and self.text_22_begun and self.text == 22:
            self.current_frame = 3
            self.background = 1
            self.text = 23

        #text 23

        if self.text == 23 and not self.text_23_begun:
            self.text_23_timer = self.ticks
            self.text_23_begun = True

        if self.ticks - self.text_23_timer > 3000 and self.text_23_begun and self.text == 23:
            self.current_frame = 1
            self.background = 2
            self.text = 24

        #text 24
        
        if self.text == 24 and not self.text_24_begun and not self.waiting:
            self.current_frame = 1
            self.background = 2
            self.is_meteorite = True
            self.meteorite_stage = 0
            self.text_24_char = 0
            self.text_24_timer = self.ticks
            self.text_24_begun = True

        if self.text_24_char >= 0 and self.ticks - self.text_24_timer > 100 and self.text_24_begun and self.text == 24:
            self.text_24_char += 1
            self.text_24_timer = self.ticks

        if self.text_24_char >= 0 and self.text_24_begun and self.text == 24 or self.text == 25:
            display.blit(self.dialog_box, (0, 0))
            display.blit(pygame.font.Font.render(self.font, self.text_24[0:self.text_24_char], False, (255, 255, 255)),
                         (3, 120))
            if self.text_24_char == len(self.text_24):
                self.text = 25
        
        #text 25

        if self.text == 25 and not self.text_25_begun:
            self.meteorite_stage = 1
            self.text_25_char = 0
            self.text_25_timer = self.ticks
            self.text_25_begun = True

        if self.text_25_char >= 0 and self.ticks - self.text_25_timer > 100 and self.text_25_begun and self.text == 25 and not self.waiting:
            self.text_25_char += 1
            self.text_25_timer = self.ticks

        if self.text_25_char >= 0 and self.text_25_begun and self.text == 25:
            display.blit(pygame.font.Font.render(self.font, self.text_25[0:self.text_25_char], False, (255, 255, 255)),
                         (3, 137))
            if self.text_25_char == len(self.text_25):
                self.waiting = True
                self.text_25_complete = True
                self.meteorite_stage = 2

        if self.text == 25 and not self.waiting and self.text_25_complete:
            self.meteorite_stage = 2
            self.text = 26

        if self.text == 26:
            display.blit(pygame.image.load("Assets/cutscenes/ending_2.png").convert_alpha(), (0, 0))