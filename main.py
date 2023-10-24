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

    tool_bar = utils.ToolBar((display.get_width()-28, display.get_height()-28))
    tool_bar.tools.append(utils.Tool(
        pygame.image.load("Assets/sprites/screw_driver_icon.png").convert_alpha(),
        "screw_driver", utils.Interactable((0, 0), (18, 18))
    ))
        
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

        display.fill((90, 90, 90))

        # draw here
        tool_bar.update(dt, mouse_pos, mouse_input[0])
        tool_bar.draw(dt, display)
            
        surf = pygame.transform.scale(display, WS)
        window.blit(surf, [0, 0])
        pygame.display.update()

        pygame.display.set_caption(f"<game name> FPS: {round(clock.get_fps(), 2)}")

        clock.tick(120)

    pygame.quit()


if __name__ == "__main__":
    main()
