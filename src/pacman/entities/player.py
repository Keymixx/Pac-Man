# import arcade
# from ..game import PADS

# PAD_X1, PAD_Y1, PAD_X2, PAD_Y2 = PADS
# class Player:
#     def __init__(self, start_col, start_row, tile_size):
#         self.title_size = tile_size
#         self.center_x = start_col * tile_size + (tile_size // 2 + PAD_X1)
#         self.center_y = start_row * tile_size + (tile_size // 2 + PAD_Y1)
#         self.speed = 50
#         self.direction = (1, 0)
#         self.next_direction = (0, 0)

#     def row_col(self)-> tuple:
#         row = int(self.center_y // self.title_size)
#         col = int(self.center_x // self.title_size)
#         return row, col

#     def axis_center(self, row, col):
#         cy = row * self.tile_size + (self.tile_size // 2 + PAD_Y1)
#         cx = row * self.tile_size + (self.tile_size // 2 + PAD_Y1)
#         return cy, cx

#     def on_axis(self):
#         row, col = self.row_col()
#         cy, cx = self.axis_center(row, col)
#         if self.center_y == cy and self.center_x == cx:
#             return True
#         else:
#             return False

#     def move(self):
#         y, x = self.next_direction
#         if x != 0:
#             self.center_x += self.speed * x
#         if y != 0:
#             self.center_y += self.speed * y

#     def update_position(self):

#         if self.on_axis() and self.next_direction != (0, 0):
#             self.move()


