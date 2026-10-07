import random
import arcade
import math
from typing import Tuple, List


class PacgumList:
    def __init__(self):
        self.pacgum_list: list[Pacgum] = []

    def generate_sample(self, maze: list[list[int]], nb_pacgum: int) -> List[tuple[int, int]]:
        maze = maze[::-1]
        y = 0
        x = 0
        valid_cell: list[tuple[int, int]] = []
        for row in maze:
            for cell in row:
                if cell != 15:
                    valid_cell.append((y, x))
                x += 1
            y += 1
            x = 0

        sample = random.sample(valid_cell, nb_pacgum)
        return sample

    def init_pacgum(self, maze: list[list[int]], nb_pacgum: int,
                    tile_size: int, offset_y: int, offset_x: int):
        sample = self.generate_sample(maze, nb_pacgum)
        for coord in sample:
            self.pacgum_list.append(Pacgum(coord, tile_size, offset_y, offset_x))

    def show_pacgum(self):
        sprite_list = arcade.SpriteList()
        for pacgum in self.pacgum_list:
            if not pacgum.eated:
                sprite_list.append(pacgum.sprite)
        return sprite_list

    def pacgum_eated(self, player_size: int, player_y: int, player_x: int):
        for pacgum in self.pacgum_list:
            if not pacgum.eated:
                pacgum_coord = [pacgum.coord_y, pacgum.coord_x]
                player_coord = [player_y, player_x]
                print(pacgum_coord, player_coord)
                if math.dist(pacgum_coord, player_coord) < (pacgum.sprite.width + player_size) / 2:
                    pacgum.eated = True
                    print("eated")


class Pacgum:
    def __init__(self, coord: tuple, tile_size: int, offset_y: int, offset_x: int):
        y, x = coord
        self.y = y
        self.x = x
    
        self.eated = False
        self.sprite = arcade.Sprite("assets/pacman_sprites/pacman_down_closed.png")

        self.sprite.center_x = x * tile_size + (tile_size // 2) + offset_x
        self.sprite.center_y = y * tile_size + (tile_size // 2) + offset_y

        self.coord_y = y * tile_size + (tile_size // 2)
        self.coord_x = x * tile_size + (tile_size // 2)
        self.sprite.scale = (tile_size / self.sprite.width) * 0.4
