import arcade

N, E, S, W = 1, 2, 4, 8


class Player:
    def __init__(self, start_col: int, start_row: int, tile_size: int,
                 maze: list[list[int]],
                 textures: dict[str, list[arcade.Texture]]):
        self.tile_size = tile_size
        self.center_y: float = start_row * tile_size + (tile_size // 2)
        self.center_x: float = start_col * tile_size + (tile_size // 2)
        self.size = tile_size * 0.7
        self.speed = tile_size * 0.08
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.maze = maze[::-1]
        self.super = False

        self.is_alive = True
        self.animation_timer = 0.0
        self.current_frame = 0
        self.textures = textures
        self.actual_texture = textures["up"][2]

    def row_col(self) -> tuple:
        row = int(self.center_y // self.tile_size)
        col = int(self.center_x // self.tile_size)
        return row, col

    def axis_center(self, row: int, col: int) -> tuple[int, int]:
        cy = row * self.tile_size + (self.tile_size // 2)
        cx = col * self.tile_size + (self.tile_size // 2)
        return cy, cx

    def will_cross_axis(self) -> bool:
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

        return False

    def move(self) -> None:
        y, x = self.direction
        if x != 0:
            self.center_x += self.speed * x
        if y != 0:
            self.center_y += self.speed * y

    def update_direction(self) -> None:
        row, col = self.row_col()
        cell = self.maze[row][col]
        ndy, ndx = self.next_direction
        dy, dx = self.direction

        if (ndy > 0 and not cell & N) or \
            (ndy < 0 and not cell & S) or \
                (ndx > 0 and not cell & E) or \
                (ndx < 0 and not cell & W):

            self.direction = self.next_direction

        elif dy == 1 and not cell & N:
            pass
        elif dy == -1 and not cell & S:
            pass
        elif dx == 1 and not cell & E:
            pass
        elif dx == -1 and not cell & W:
            pass

        else:
            self.direction = (0, 0)

    def update_position(self) -> None:
        row, col = self.row_col()
        cy, cx = self.axis_center(row, col)

        ndy, ndx = self.next_direction
        dy, dx = self.direction

        if (ndx != 0 and ndx == -dx) or (ndy != 0 and ndy == -dy):
            self.direction = self.next_direction

        if self.will_cross_axis() or self.direction == (0, 0):
            self.center_y = cy
            self.center_x = cx
            self.update_direction()

        self.move()

    def update_animation(self, delta_time: float) -> None:
        if self.direction == (0, 0) and self.is_alive:
            self.current_frame = 0

        self.animation_timer += delta_time
        if self.animation_timer >= 0.1:
            self.animation_timer = 0.0
            self.current_frame = (self.current_frame + 1) % 3

        elif self.direction == (0, 1):
            self.actual_texture = self.textures["right"][self.current_frame]
        elif self.direction == (0, -1):
            self.actual_texture = self.textures["left"][self.current_frame]
        elif self.direction == (1, 0):
            self.actual_texture = self.textures["up"][self.current_frame]
        elif self.direction == (-1, 0):
            self.actual_texture = self.textures["down"][self.current_frame]

    def death_animation(self, delta_time: float) -> None:
        self.animation_timer += delta_time
        if self.animation_timer >= 0.1:
            self.animation_timer = 0.0
            self.current_frame = (self.current_frame + 1) % 15

        self.actual_texture = self.textures["death"][self.current_frame]
