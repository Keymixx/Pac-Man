N, E, S, W = 1, 2, 4, 8


class Ghost:
    def __init__(self, start_col, start_row, tile_size, maze: list[list[int]]):
        self.tile_size = tile_size
        self.center_x = start_col * tile_size + (tile_size // 2)
        self.center_y = start_row * tile_size + (tile_size // 2)
        self.speed = tile_size * 0.04
        self.maze = maze[::-1]
        self.direction = (0, 0)
        self.next_direction = (0, 0)

    def row_col(self) -> tuple:
        row = int(self.center_y // self.tile_size)
        col = int(self.center_x // self.tile_size)
        return row, col

    def axis_center(self, row, col):
        cy = row * self.tile_size + (self.tile_size // 2)
        cx = col * self.tile_size + (self.tile_size // 2)
        return cy, cx

    def get_neighbours(self, coord: tuple[int, int]) -> list[tuple[int, int]]:
        y, x = coord
        cell = self.maze[y][x]
        neighbours = []

        if not cell & N:
            neighbours.append((y + 1, x))
        if not cell & S:
            neighbours.append((y - 1, x))
        if not cell & E:
            neighbours.append((y, x + 1))
        if not cell & W:
            neighbours.append((y, x - 1))

        return neighbours

    def bfs(self, target: tuple[int, int]):
        start = self.row_col()
        visited = set(start)
        queue = [start]
        history = {}

        while queue:
            cell = queue.pop(0)
            neighbours = self.get_neighbours(cell)

            if cell == target:
                return history

            for neighbour in neighbours:
                if neighbour not in visited:
                    visited.add(neighbour)
                    history[neighbour] = cell
                    queue.append(neighbour)

    def get_path(self, history: dict, target: tuple[int, int]):
        current = target
        path = []
        start = self.row_col()
        while current != start:
            path.append(current)
            current = history[current]
        path.reverse()
        return path

    def get_direction(self, target_pos: tuple[int, int]) -> tuple[int, int]:
        cy, cx = self.row_col()
        ty, tx = target_pos
        if ty > cy:
            return (1, 0)
        elif ty < cy:
            return (-1, 0)
        elif tx > cx:
            return (0, 1)
        else:
            return (0, -1)

    def get_next_direction(self, player_pos: tuple[int, int]):
        history = self.bfs(player_pos)
        path = self.get_path(history, player_pos)
        self.next_direction = self.get_direction(path[0])
        print(self.next_direction)

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

    def update_position(self):
        row, col = self.row_col()
        cy, cx = self.axis_center(row, col)
        dy, dx = self.direction

        if self.will_cross_axis() or self.direction == (0, 0):
            self.center_y = cy 
            self.center_x = cx 
            self.update_direction()

        self.move()
