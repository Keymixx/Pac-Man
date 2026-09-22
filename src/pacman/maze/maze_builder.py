import arcade

N, E, S, W = 1, 2, 4, 8

def build_maze(maze: list[list[int]],
               width: int,
               height: int,
               height_hud: int):

    tiles_sprites = {i: f"assets/wall_sprites/wall_{i}.png" for i in range(16)}
    tiles_list = arcade.SpriteList()

    maze_height = len(maze)
    maze_width = len(maze[0])

    tile_size = int(min((height) / maze_height, (width) / maze_width))

    for y, row in enumerate(maze):
        for x, v in enumerate(row):
            tile = arcade.Sprite(tiles_sprites[v])

            tile.width = tile_size 
            tile.height = tile_size

            offset_x = (width - (maze_width * tile_size)) / 2
            offset_y = height_hud + (height - (maze_height * tile_size)) / 2

            tile.center_x = offset_x + (tile_size * x) + (tile_size / 2)
            tile.center_y = (tile_size * (maze_height - 1 - y)) + (tile_size / 2) + offset_y

            tiles_list.append(tile)

    return tiles_list, tile_size
