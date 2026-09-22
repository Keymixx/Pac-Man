import arcade


class Player:
    def __init__(self, start_col, start_row, tile_size, maze: list[list[int]]):
        self.tile_size = tile_size
        self.center_x = start_col * tile_size + (tile_size // 2)
        self.center_y = start_row * tile_size + (tile_size // 2)
        self.speed = 50
        self.direction = (1, 0)
        self.next_direction = (0, 0)
        self.maze = maze

    def row_col(self)-> tuple:
        row = int(self.center_y // self.title_size)
        col = int(self.center_x // self.title_size)
        return row, col

    def axis_center(self, row, col):
        cy = row * self.tile_size + (self.tile_size // 2)
        cx = col * self.tile_size + (self.tile_size // 2)
        return cy, cx

    def on_axis(self):
        row, col = self.row_col()
        cy, cx = self.axis_center(row, col)
        if self.center_y == cy and self.center_x == cx:
            return True
        else:
            return False

    def move(self):
        y, x = self.direction
        if x != 0:
            self.center_x += self.speed * x
        if y != 0:
            self.center_y += self.speed * y
        return 0

    def update_direction(self):
        row, col = self.row_col()
        cell = self.maze[row][col]
        y, x = self.next_direction
        if y > 0 and  cell & 1 > 0:
            self.direction = (1,0)
        elif y < 0 and  cell & 4 > 0:
            self.direction = (-1,0)
        elif x > 0 and  cell & 2 > 0:
            self.direction = (0,1)
        elif x < 0 and  cell & 8 > 0:
            self.direction = (0,-1)
        else:
            self.direction = (0,0)

    def update_position(self):

        if self.on_axis() and self.direction != (0, 0):
            if self.direction == self.next_direction:
                self.move()
            else:
                return 0


