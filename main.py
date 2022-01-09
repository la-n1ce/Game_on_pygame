import pygame
from class_board import Board


def main():
    pygame.init()
    size = 300, 400
    screen = pygame.display.set_mode(size)
    board = Board(666, 66)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('black')
        pygame.display.flip()
    pygame.quit()


main()