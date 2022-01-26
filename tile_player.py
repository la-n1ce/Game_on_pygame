import pygame
from load_image import load_image


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
sky_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

tile_images = {
    'sky': load_image('Sky_Block.jpg'),
    'dirt': load_image('Dirt_Block.png'),
    'tree': load_image('Tree_BLock.png')
}
player_image = load_image('pers1.png')

tile_width = tile_height = 16


class Sky(pygame.sprite.Sprite):
    # блоки/клетки неба
    def __init__(self, tile_type, pos_x, pos_y, step_x=0):
        super().__init__(sky_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + step_x, tile_height * pos_y)  # в пикселях


class Tile(pygame.sprite.Sprite):
    # блоки/клетки
    def __init__(self, tile_type, pos_x, pos_y, step_x=0):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + step_x, tile_height * pos_y)  # в пикселях


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y - 16)