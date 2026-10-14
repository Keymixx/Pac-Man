import random
import arcade
import math
from typing import Tuple, List
from .player import Player


class PacgumList:
    def __init__(self, nb_pacgum: int, supergum_point: int,
                 gum_point: int, maze: list[list[int]]):
        self.nb_pacgum = nb_pacgum
        self.supergum_point = supergum_point
        self.gum_point = gum_point

        self.pacgum_list: list[Pacgum] = []
        self.pacgums = list[tuple[int, int]]
        self.super_pacgums = list[tuple[int, int]]

        self.maze = maze

        self.sprite_list = arcade.SpriteList()

    def generate_sample(self) -> List[tuple[int, int]]:
        maze = self.maze[::-1]
        valid_cell: list[tuple[int, int]] = []
        y_max = len(maze) - 1
        x_max = len(maze[0]) - 1

        corners = {(0, 0), (0, x_max), (y_max, 0), (y_max, x_max)}
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if (y, x) not in corners and cell != 15:
                    valid_cell.append((y, x))

        sample = random.sample(valid_cell, self.nb_pacgum)
        return sample

    def init_pacgum(self, tile_size: int):
        sample = self.generate_sample()
        for coord in sample:
            new_pacgum = Pacgum(coord, tile_size)
            self.pacgum_list.append(new_pacgum)
            self.sprite_list.append(new_pacgum.sprite)

        y_max = len(self.maze) - 1
        x_max = len(self.maze[0]) - 1
        corners = {(0, 0), (0, x_max), (y_max, 0), (y_max, x_max)}
        for coord in corners:
            super_pacgum = SuperPacgum(coord, tile_size)
            self.pacgum_list.append(super_pacgum)
            self.sprite_list.append(super_pacgum.sprite)

    def show_pacgum(self, offset_y: int, offset_x: int):
        for pacgum in self.pacgum_list:
            if not pacgum.eated:
                pacgum.sprite.center_y = pacgum.coord_y + offset_y
                pacgum.sprite.center_x = pacgum.coord_x + offset_x
        return self.sprite_list

    def pacgum_eated(self, player: Player):
        player_y, player_x = player.row_col()

        for pacgum in self.pacgum_list:
            if not pacgum.eated:
                pacgum_coord = [pacgum.coord_y, pacgum.coord_x]
                player_coord = [player.center_y, player.center_x]

                if math.dist(pacgum_coord, player_coord) < (pacgum.sprite.width + player.size) / 2:
                    pacgum.eated = True
                    pacgum.sprite.remove_from_sprite_lists()
                    if pacgum.super_gum:
                        player.super = True
                        return self.supergum_point
                    else:
                        return self.gum_point
        return 0


class Pacgum:
    def __init__(self, coord: tuple, tile_size: int):
        y, x = coord
        self.y = y
        self.x = x

        self.eated = False
        self.super_gum = False 
        self.sprite = arcade.Sprite("assets/pacman_sprites/pacman_down_closed.png")

        self.coord_y = y * tile_size + (tile_size // 2)
        self.coord_x = x * tile_size + (tile_size // 2)
        self.sprite.scale = tile_size * 0.004


class SuperPacgum(Pacgum):
    def __init__(self, coord, tile_size):
        super().__init__(coord, tile_size)
        self.sprite.scale = tile_size * 0.008
        self.super_gum = True
