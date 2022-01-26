from tile_player import Tile, Player, Sky


def generate_level(level, type_generate=1):
    if type_generate == 1:
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '0':
                    Sky('sky', x, y)
                elif level[y][x] == '1':
                    Tile('dirt', x, y)
                elif level[y][x] == '@':
                    Sky('sky', x, y)
                    new_player = Player(x, y)
        # вернем игрока, а также размер поля в клетках
        return new_player, x, y