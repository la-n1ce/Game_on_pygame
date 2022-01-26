import pygame
from class_Board import Board
from start_screen import terminate, start_screen
from load_level import load_level
from generate_level import generate_level
from settings import WIDTH, HEIGHT
from tile_player import all_sprites, player_group, tiles_group, sky_group
from load_image import load_image
from tile_player import Tile, Sky
from end_screen import end_screen


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w - WIDTH // 2) - 16
        # self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


def main():
    # для передвижения игрока
    RIGHT = "to the right"
    LEFT = "to the left"
    STOP = "stop"
    motion = STOP
    step_x = 0
    step_x_for_board = 0

    # для прыжка игрока
    is_jump = False
    jump_count = 11

    player = None

    pygame.init()
    size = WIDTH, HEIGHT = 800, 560
    screen = pygame.display.set_mode(size)
    start_screen(screen)

    # курсор
    cursor = pygame.sprite.Sprite()
    cursor.image = load_image('arrow.png')
    cursor.rect = cursor.image.get_rect()
    cursor_sprites = pygame.sprite.Group()
    cursor_sprites.add(cursor)
    pygame.mouse.set_visible(False)
    was_mouse_motion = False

    player, level_x, level_y = generate_level(load_level('level.txt'), 1)
    camera = Camera()

    board = Board(50, 35)
    for i in range(len(board.board)):
        for j in range(len(board.board[i])):
            if board.board[i][j] == '@':
                board.board[i][j] = 0
            else:
                board.board[i][j] = int(board.board[i][j])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            #нажатие мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # копание
                    if round(step_x_for_board) % 16 != 0:
                        plus = 1
                    else:
                        plus = 0

                    board.get_click(event.pos, round(step_x_for_board) // 16 + plus)
                    x_in_board, y_in_board = board.get_cell(event.pos, round(step_x_for_board) // 16 + plus)
                    print(x_in_board, y_in_board)
                    for sprite in tiles_group:
                        if sprite.rect.x == (x_in_board - 30) * 16 and sprite.rect.y == y_in_board * 16:
                            sprite.kill()
                    if board.board[y_in_board][x_in_board] == 0:
                        step2 = (round(step_x_for_board) // 16 + plus)
                        plus2 = x_in_board - (53 + (step_x_for_board // 16))
                        Sky('sky', 53 + plus2 - 30 + (step_x_for_board // 16), y_in_board, (800 - step_x_for_board) % 16 - step2 * 16)
                elif event.button == 3:
                    # строительство
                    if round(step_x_for_board) % 16 != 0:
                        plus = 1
                    else:
                        plus = 0
                    board.get_click(event.pos, round(step_x_for_board) // 16 + plus)
                    x_in_board, y_in_board = board.get_cell(event.pos, round(step_x_for_board) // 16 + plus)
                    for sprite in sky_group:
                        if sprite.rect.x == (x_in_board - 30) * 16 and sprite.rect.y == y_in_board * 16:
                            sprite.kill()
                    if board.board[y_in_board][x_in_board] == 2:
                        step2 = (round(step_x_for_board) // 16 + plus)
                        plus2 = x_in_board - (53 + (step_x_for_board // 16))
                        Tile('tree', 53 + plus2 - 30 + (step_x_for_board // 16), y_in_board, (800 - step_x_for_board) % 16 - step2 * 16)

            # курсор
            if event.type == pygame.MOUSEMOTION:
                was_mouse_motion = True
                cursor.rect.x = event.pos[0]
                cursor.rect.y = event.pos[1]

            # клавиатура
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    motion = LEFT
                elif event.key == pygame.K_RIGHT:
                    motion = RIGHT
                elif event.key == pygame.K_SPACE:
                    is_jump = True
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    motion = STOP
                    step_x = 0

        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        sky_group.draw(screen)
        player_group.draw(screen)
        # курсор
        if was_mouse_motion and pygame.mouse.get_focused():
            cursor_sprites.draw(screen)
        pygame.display.flip()

        if motion == LEFT:
            if not is_jump:
                step_x -= 1.5
            else:
                step_x -= 1

            if abs(int(step_x)) > 0:
                player.rect.x += int(step_x)  # step_x - в пикселях
                step_x_for_board += int(step_x)
                '''
                for sprite in tiles_group:
                    if player.rect.x + step_x_for_board == sprite.rect.x:
                        if player.rect.y + player.rect.height < sprite.rect.y:
                            player.rect.y = sprite.rect.y - player.rect.height
                if player.rect.y + player.rect.height >= HEIGHT:
                    terminate()
                    end_screen(screen)
                '''
                step_x = 0
        elif motion == RIGHT:
            if not is_jump:
                step_x += 1.5
            else:
                step_x += 1

            if abs(int(step_x)) > 0:
                player.rect.x += int(step_x)
                step_x_for_board += int(step_x)
                step_x = 0

        if is_jump:
            if jump_count >= -11:
                if jump_count < 0:
                    player.rect.y += int((jump_count ** 2) / 20)
                else:
                    player.rect.y -= int((jump_count ** 2) / 20)
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 11


if __name__ == '__main__':
    main()