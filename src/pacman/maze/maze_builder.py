import arcade

N, E, S, W = 1, 2, 4, 8
PAD_X1 = 20
PAD_Y1 = 20
PAD_X2 = 20
PAD_Y2 = 20


def calcul_mask(cell: int):
    mask = 0
    mask += cell & N
    mask += cell & E
    mask += cell & S
    mask += cell & W
    return mask


def build_maze(maze: list[list[int]],
               width: int,
               height: int,
               y_offset: int = 0):
    tiles_sprites = {i: f"assets/wall_sprites/wall_{i}.png" for i in range(16)}
    tiles_list = arcade.SpriteList()

    maze_height = len(maze)
    maze_width = len(maze[0])

    tile_h = (height - (PAD_Y1 + PAD_Y2)) / maze_height
    tile_w = (width - (PAD_X1 + PAD_X2)) / maze_width
    print(tile_h)
    print(tile_w)

    for y, row in enumerate(maze):
        for x, v in enumerate(row):
            mask = calcul_mask(v)
            tile = arcade.Sprite(tiles_sprites[mask])

            tile.width = tile_w
            tile.height = tile_h

            tile.center_x = (tile_w * x) + (tile_w / 2) + PAD_X1
            tile.center_y = ((maze_height - 1 - y) * tile_h) + (tile_h / 2) + PAD_Y1 + y_offset

            tiles_list.append(tile)

    return tiles_list
