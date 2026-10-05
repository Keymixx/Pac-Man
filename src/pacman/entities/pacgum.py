import random
import arcade
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

    def init_pacgum(self, maze: list[list[int]], nb_pacgum: int):
        sample = self.generate_sample(maze, nb_pacgum)
        for coord in sample:
            self.pacgum_list.append(Pacgum(coord))

    def show_pacgum(self):
        sprite_list = arcade.SpriteList()
        for pacgum in self.pacgum_list:
            if not pacgum.eated:
                sprite_list.append(pacgum.sprite)
        return sprite_list


class Pacgum:
    def __init__(self, coord: tuple):
        y, x = coord
        self.eated = False
        self.sprite = arcade.Sprite("assets/pacman_sprites/pacman_down_closed.png")

        ############# magic number a modifier #####################
        self.sprite.center_x = x * 23 + (32 // 2)
        self.sprite.center_y = y * 23 + (62 // 2)
        self.sprite.scale = 0.4
