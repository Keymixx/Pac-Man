import random

class PacgumList:
	def __init__(self):
		self.pacgum_list = list[Pacgum]

	def generate_sample (self, maze:list[list[int]], nb_pacgum: int) -> list[tuple]:
		maze = maze[::-1]
		y = 0
		x = 0
		valid_cell = list[tuple(int, int)]
		for row in maze:
			for cell in row:
				if cell != 15:
					valid_cell.append(y, x)
				x += 1
			y += 1

		sample = random.sample(cell, nb_pacgum)
		return sample

	def init_pacgum(self, maze:list[list[int]], nb_pacgum: int):
		sample = self.generate_sample(maze, nb_pacgum)
		for coord in sample:
			self.pacgum_list.append(Pacgum(coord))

class Pacgum:
	def __init__(self, coord: tuple):
		y, x = coord
		self.eated = False

	