import pygame

class Screen:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.screen = 0

    def display(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.x, self.y))

        pygame.display.set_caption("Maze Solver")

        icon = pygame.image.load('maze.png')
        pygame.display.set_icon(icon)

        self.screen.fill((0, 0, 0))
        pygame.display.flip()

        # Game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(self.screen, (100, 100, 100), (pygame.mouse.get_pos()[0],
                                                                pygame.mouse.get_pos()[1], 10, 10))
            pygame.display.flip()


screen = Screen(800, 600)
screen.display()
