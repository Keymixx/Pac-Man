N, E, S, W = 1, 2, 4, 8

class Ghost:
    def __init__(self, start_col, start_row, tile_size, maze: list[list[int]]):
        self.tile_size = tile_size
        self.center_x = start_col * tile_size + (tile_size // 2)
        self.center_y = start_row * tile_size + (tile_size // 2)
        self.speed = tile_size * 0.04
        self.maze = maze[::-1]

    def get_neighbours(self, coord: tuple[int,int])-> list[tuple[int, int]]:
        y , x = coord
        cell = self.maze[y][x]
        neighbours = []

        if cell & N:
            neighbours.append(y + 1, x)
        if cell & S:
            neighbours.append(y - 1, x)
        if cell & E:
            neighbours.append(y, x + 1)
        if cell & W:
            neighbours.append(y, x - 1)

        return neighbours