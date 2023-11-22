import pygame


class Simulator:
    simulation_steps_count: int = 0

    def __init__(self):
        pass

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((1280, 720))
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill("purple")

            # RENDER YOUR GAME HERE

            pygame.display.flip()

            clock.tick(60)

            self.simulation_steps_count += 1

        pygame.quit()
