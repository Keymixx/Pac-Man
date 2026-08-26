import arcade
from typing import Tuple

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


def build_maze(maze: list[list[int]], width: int, height: int):
    tiles_sprites = {i:f"assets/wall_sprites/wall_{i}.png" for i in range(16)}
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

            tile.center_x = (tile_w * x) + (tile_w // 2) + PAD_X1
            tile.center_y = ((maze_height - 1 - y) * tile_h) + (tile_h / 2) + PAD_Y1

            tiles_list.append(tile)

    return tiles_list, tile_w, tile_h






# def draw_maze(maze: list[list[int]], width: int, height: int):
#     tile_x = width // len(maze[0])
#     tile_y = height // len(maze)
#     for y, row in enumerate(maze):
#         for x, v in enumerate(row):
#             x0 = (x * tile_x) + tile_x // 2
#             y0 = height - ((y + 1) * tile_y) - tile_y // 2
#             print
#             if v & 1: 
#                 arcade.draw_line(x0, y0+tile_y, x0+tile_x, y0+tile_y, arcade.color.BLUE, 5)
#             if v & 2: 
#                 arcade.draw_line(x0+tile_x, y0, x0+tile_x, y0+tile_y, arcade.color.BLUE, 5)
#             if v & 4:
#                 arcade.draw_line(x0, y0, x0+tile_x, y0, arcade.color.BLUE, 5)
#             if v & 8:
#                 arcade.draw_line(x0, y0, x0, y0+tile_y, arcade.color.BLUE, 5)


# def maze_builder(maze: List[List[int]]) -> arcade.SpriteList:
#     wall_sprites = {i: arcade.Sprite(f"assets/Wall_sprites/wall_{i}.png") for i in range(15)}
#     wall_list = arcade.SpriteList()
#     wall_list.append()
#     center_y = 16
#     for y in enumerate(maze):
#         center_x = 16
#         for x in enumerate(maze[y]):
#             title = choose_title(maze[y][x])
#             wall = wall_sprites[title]
#             wall.center_x = center_x
#             wall.center_y = center_y
#             wall_list.append(wall)
#             center_x += 16
#         center_y += 16
#     return wall_list



