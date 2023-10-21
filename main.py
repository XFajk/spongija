import pygame
import time


def main():
    pygame.init()

    WS = [800, 600]
    ZOOM = 4

    window = pygame.display.set_mode(WS)
    display = pygame.Surface((WS[0] / ZOOM, WS[1] / ZOOM))

    clock = pygame.time.Clock()

    done = False
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

    pygame.quit()


if __name__ == "__main__":
    main()
