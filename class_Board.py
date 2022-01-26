import pygame
from load_level import load_level


class Board:
    def __init__(self, widht, height):
        # widht, height - кол-во клеток поля
        self.width = widht
        self.height = height
        self.board = []
        for line in load_level('level.txt'):
            line = list(line)
            self.board.append(line)

        # значения поля
        self.left = 0
        self.top = 0
        self.cell_size = 16  # размер клетки

    def render(self, screen):
        colors = [pygame.Color(0, 0, 0), pygame.Color(255, 255, 255)]
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(screen, colors[1],
                                 (self.left + x * self.cell_size,
                                  self.top + y * self.cell_size,
                                  self.cell_size, self.cell_size), 1)
                pygame.draw.rect(screen, colors[self.board[y][x]],
                                 (self.left + x * self.cell_size + 1,
                                  self.top + y * self.cell_size + 1,
                                  self.cell_size - 2, self.cell_size - 2))

    def get_cell(self, mouse_pos, step_x=0):
        x = (mouse_pos[0] - self.left) // self.cell_size + 30 + step_x
        y = (mouse_pos[1] - self.top) // self.cell_size
        if 0 <= x < len(self.board[-1]) and 0 <= y < len(self.board):
            return x, y  # в клетках
        return None  # в дальнейшем None будет возвращаться, когда будет создан персонаж

    def on_click(self, cell_coords):
        y = cell_coords[0]
        x = cell_coords[1]
        # координаты наоборот, тк в списке
        # нумерация по-другому (наоборот)

        # изменяем атрибут self.board
        if self.board[x][y] in [1, 2]:
            self.board[x][y] = 0
        elif self.board[x][y] == 0:
            self.board[x][y] = 2
        '''
        self.board[cell_coords[1]][cell_coords[0]] = 1 - self.board[cell_coords[1]][cell_coords[0]]
        '''

    def get_click(self, mouse_pos, step_x=0):
        cell = self.get_cell(mouse_pos, step_x)
        if cell:
            self.on_click(cell)