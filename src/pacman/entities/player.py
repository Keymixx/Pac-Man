import arcade

N, E, S, W = 1, 2, 4, 8


class Player:
    def __init__(self, start_col, start_row, tile_size, maze: list[list[int]]):
        self.tile_size = tile_size
        self.center_x = start_col * tile_size + (tile_size // 2)
        self.center_y = start_row * tile_size + (tile_size // 2)
        self.speed = 0.5
        self.direction = (1, 0)
        self.next_direction = (0, 0)
        self.maze = maze

    def row_col(self) -> tuple:
        row = int(self.center_y // self.tile_size)
        col = int(self.center_x // self.tile_size)
        return row, col

    def axis_center(self, row, col):
        cy = row * self.tile_size + (self.tile_size // 2)
        cx = col * self.tile_size + (self.tile_size // 2)
        return cy, cx

    def will_cross_axis(self):
        row, col = self.row_col()
        cy, cx = self.axis_center(row, col)
        dy, dx = self.direction

        if dy == 0 and dx == 0:
            return False

        if dy != 0:
            distance = (cy - self.center_y) * dy
            return 0 <= distance <= self.speed

        if dx != 0:
            distance = (cx - self.center_x) * dx
            return 0 <= distance <= self.speed

    def move(self):
        y, x = self.direction
        if x != 0:
            self.center_x += self.speed * x
        if y != 0:
            self.center_y += self.speed * y

    def update_direction(self):
        row, col = self.row_col()
        print(row, col)
        cell = self.maze[row][col]
        dy, dx = self.next_direction

        if (dy > 0 and cell & N) or \
            (dy < 0 and cell & S) or \
                (dx > 0 and cell & E) or \
                (dx < 0 and cell & W):

            self.direction = self.next_direction

    def update_position(self):
        row, col = self.row_col()
        cy, cx = self.axis_center(row, col)
        dy, dx = self.direction

        if self.will_cross_axis():
            self.center_y = cy + dy
            self.center_x = cx + dx
            self.update_direction()

        self.move()
