import pygame
import sys
import os
from load_image import load_image
WIDTH, HEIGHT = 800, 560


def terminate():
    pygame.quit()
    sys.exit()


FPS = 50
clock = pygame.time.Clock()


def end_screen(screen):
    intro_text = ['Вы умерли из-за падения в пропасть.',
                  'Попробуйте ещё раз,'
                  ' нажав на любую кнопку мыши или клавишу клавиатуры']

    fon = pygame.transform.scale(load_image('fon2.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    font = pygame.font.Font(None, 30)
    text_coord = 490
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    end_screen(screen)