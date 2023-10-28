import pygame
from pygame import Vector2
from icecream import ic


class Interactable:
    def __init__(self, pos: tuple, size: tuple):
        self.rect: pygame.Rect = pygame.Rect(pos, size)

        self.is_hovering_over: bool = False

        self.is_clicked: bool = False
        self._was_clicked: bool = False

        self.is_held: bool = False

        self.is_released: bool = True

    def update(self, mouse_pos: tuple, interaction_starter: bool) -> None:
        if self.rect.collidepoint(mouse_pos):
            self.is_hovering_over = True
            if interaction_starter:

                self.is_clicked = True if not self.is_clicked and not self._was_clicked else False

                if self.is_clicked and not self._was_clicked:
                    self._was_clicked = True

                self.is_held = True
                self.is_released = False
            else:
                self._was_clicked = False
                self.is_released = True
                self.is_held = False
        else:
            self.is_hovering_over = False
            self.is_clicked = False
            self._was_clicked = False
            self.is_held = False
            self.is_released = True

    def debug_draw(self, display: pygame.Surface, debug_color: tuple) -> None:
        pygame.draw.rect(display, debug_color, self.rect, 1)
