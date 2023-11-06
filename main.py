import pygame

import time

import utils


# noinspection PyTypeChecker
def main():
    pygame.init()
    pygame.mixer.init()

    WS = [800, 600]
    ZOOM = 4

    window = pygame.display.set_mode(WS, vsync=1)
    display = pygame.Surface((WS[0] / ZOOM, WS[1] / ZOOM))

    clock = pygame.time.Clock()

    tool_bar = utils.ToolBar((display.get_width() - 28, display.get_height() - 28))

    scenes = [utils.scenes.MainMenu(display), utils.scenes.StartCutscene(display), utils.scenes.CableScene(display), utils.scenes.FuelScene(display), utils.scenes.ConveyorBeltScene(display), utils.scenes.WeldingScene(tool_bar, display), utils.scenes.EndCutscene(display)]

    last_frame_time = time.perf_counter()

    current_scene = 0

    done = False
    while not done:

        current_frame_time = time.perf_counter()
        dt = (current_frame_time - last_frame_time) * 60
        last_frame_time = current_frame_time

        keys = pygame.key.get_pressed()

        mouse_input = pygame.mouse.get_pressed()
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        mouse_pos /= ZOOM

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        if scenes[current_scene].end_won:
            current_scene += 1
            scenes[current_scene].end_won = False

        # draw here
        scenes[current_scene].play(dt, tool_bar, display, mouse_pos, mouse_input[0])

        if current_scene >= 2 and current_scene <6:
            tool_bar.update(dt, mouse_pos, mouse_input[0])
            tool_bar.draw(dt, display)

        surf = pygame.transform.scale(display, WS)
        window.blit(surf, [0, 0])
        pygame.display.update()

        pygame.display.set_caption(f"Departure FPS: {round(clock.get_fps(), 2)}")

        clock.tick(60)

    pygame.mixer.quit()
    pygame.quit()


if __name__ == "__main__":
    main()
