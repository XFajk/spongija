import pygame
from icecream import ic

import time

import utils

def main():
    pygame.init()

    WS = [800, 600]
    ZOOM = 4

    window = pygame.display.set_mode(WS)
    display = pygame.Surface((WS[0] / ZOOM, WS[1] / ZOOM))

    clock = pygame.time.Clock()
    
    inter = utils.interactable.Interactable((50, 50), (30, 30))
    
    last_frame_time = time.perf_counter()
    
    done = False
    while not done:

        current_frame_time = time.perf_counter()
        dt = (current_frame_time - last_frame_time) * 60

        keys = pygame.key.get_pressed()

        mouse_input = pygame.mouse.get_pressed()
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        mouse_pos /= ZOOM


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        display.fill((255, 255, 255))

        # draw here
        inter.update(mouse_pos, mouse_input[0])
            
        surf = pygame.transform.scale(display, WS)
        window.blit(surf, [0, 0])
        pygame.display.update()

        pygame.display.set_caption(f"<game name> FPS: {round(clock.get_fps(), 2)}")

        clock.tick(120)

    pygame.quit()


if __name__ == "__main__":
    main()
