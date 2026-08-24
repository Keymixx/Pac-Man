from typing import List
import arcade

def draw_maze(maze: list[list[int]], width: int, height: int):
    tile_x = width // len(maze[0])
    tile_y = height // len(maze)
    for y, row in enumerate(maze):
        for x, v in enumerate(row):
            x0 = (x * tile_x) + tile_x // 2
            y0 = height - ((y + 1) * tile_y) - tile_y // 2
            print
            if v & 1: 
                arcade.draw_line(x0, y0+tile_y, x0+tile_x, y0+tile_y, arcade.color.BLUE, 5)
            if v & 2: 
                arcade.draw_line(x0+tile_x, y0, x0+tile_x, y0+tile_y, arcade.color.BLUE, 5)
            if v & 4:
                arcade.draw_line(x0, y0, x0+tile_x, y0, arcade.color.BLUE, 5)
            if v & 8:
                arcade.draw_line(x0, y0, x0, y0+tile_y, arcade.color.BLUE, 5)


# def choose_title(cell: int):
#     title += cell & 1
#     title += cell & 2
#     title += cell & 4
#     title += cell & 8
#     return cell

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



