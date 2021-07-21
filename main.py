import pygame, sys

from pygame.locals import *
from collections import deque

pygame.init()

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
PURPLE = (128,0,128)
BLUE = (0,0,255)
YELLOW = (255,255,0)
RED = (255,0,0)

WIDTH = 900

width_of_one_cell = 18

total_rows = WIDTH // width_of_one_cell
total_cols = WIDTH // width_of_one_cell

WINDOW = pygame.display.set_mode((WIDTH, WIDTH))

pygame.display.set_caption('Path Finding Visualisation')

#WINDOW.fill(WHITE)

class Cell:
	def __init__(self, row, col, width):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.adjacent = []
		self.color = WHITE
		self.width = width

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		self.color == RED

	def is_in_openset(self):
		return self.color == GREEN

	def is_obstacle(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == BLUE

	def is_end(self):
		return self.color == YELLOW

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = BLUE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = YELLOW

	def make_path(self):
		self.color = PURPLE

	def draw(self, WINDOW): #basically colors all the cells in a grid (initially all are colored white)
		pygame.draw.rect(WINDOW, self.color, (self.x, self.y, self.width, self.width))


def draw_lines(WINDOW, WIDTH): #function to display lines
	no_of_cells = WIDTH // width_of_one_cell

	starting_pos_ver = width_of_one_cell

	while starting_pos_ver < WIDTH:
		pygame.draw.line(WINDOW, BLACK, (starting_pos_ver,0), (starting_pos_ver, WIDTH))
		starting_pos_ver += width_of_one_cell
	#pygame.display.update()

	starting_pos_hor = width_of_one_cell

	while starting_pos_hor < WIDTH:
		pygame.draw.line(WINDOW, BLACK, (0,starting_pos_hor), (WIDTH,starting_pos_hor))
		starting_pos_hor += width_of_one_cell
	pygame.display.update()

def make_cells_grid(): #collecting all rows,cols in twodimensional array spots
	spots = []
	rows = WIDTH // width_of_one_cell

	for i in range(rows):
		spots.append([])
		for j in range(rows):
			new_spot = Cell(i, j, width_of_one_cell)
			spots[i].append(new_spot)

	return spots

def draw_all_spots(WINDOW, spots, width_of_one_cell): #just drawing all the lines and cells
	WINDOW.fill(WHITE)
	for row in spots:
		for cell in row:
			cell.draw(WINDOW)
	
	#pygame.display.update()
	draw_lines(WINDOW, WIDTH)

def get_spot_pos(pos, width_of_one_cell): #function for finding in which cell we have clicked
	y, x = pos

	row = y // width_of_one_cell
	col = x // width_of_one_cell

	return row, col

def bfs(start_cell, end_cell, spots):
	q = deque()
	q.append(start_cell)
	visited = []
	came_from = {}
	while len(q) > 0:
		cur_cell = q.popleft()
		visited.append(cur_cell)
		if cur_cell == end_cell:
			end_cell.make_end()
			while came_from[cur_cell] != start_cell:
				if cur_cell != end_cell:
					cur_cell.make_path()
				cur_cell = came_from[cur_cell] 
			cur_cell.make_path()
			return
		cur_x, cur_y = cur_cell.get_pos()
		if cur_x < total_rows - 1 and not spots[cur_x + 1][cur_y].is_obstacle():
			if spots[cur_x + 1][cur_y] not in visited:
				spots[cur_x + 1][cur_y].make_open()
				came_from[spots[cur_x + 1][cur_y]] = cur_cell
				pygame.display.update()
				q.append(spots[cur_x + 1][cur_y])
				visited.append(spots[cur_x + 1][cur_y])
		if cur_x > 0 and not spots[cur_x - 1][cur_y].is_obstacle():
			if spots[cur_x - 1][cur_y] not in visited:
				spots[cur_x - 1][cur_y].make_open()
				came_from[spots[cur_x - 1][cur_y]] = cur_cell
				pygame.display.update()
				q.append(spots[cur_x - 1][cur_y])
				visited.append(spots[cur_x - 1][cur_y])
		if cur_y > 0 and not spots[cur_x][cur_y - 1].is_obstacle():
			if spots[cur_x][cur_y - 1] not in visited:
				spots[cur_x][cur_y - 1].make_open()
				came_from[spots[cur_x][cur_y - 1]] = cur_cell
				pygame.display.update()
				q.append(spots[cur_x][cur_y - 1])
				visited.append(spots[cur_x][cur_y - 1])
		if cur_y < total_cols - 1 and not spots[cur_x][cur_y + 1].is_obstacle():
			if spots[cur_x][cur_y + 1] not in visited:
				spots[cur_x][cur_y + 1].make_open()
				came_from[spots[cur_x][cur_y + 1]] = cur_cell
				pygame.display.update()
				q.append(spots[cur_x][cur_y + 1])
				visited.append(spots[cur_x][cur_y + 1])
		
def main():
	spots = make_cells_grid()

	start_cell = None
	end_cell = None
	started = False
	end = False

	while True: # main game loop
		draw_all_spots(WINDOW, spots, width_of_one_cell)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if pygame.mouse.get_pressed()[0]: #LEFT MOUSE BUTTON
				pos_of_mouse = pygame.mouse.get_pos()
				row, col = get_spot_pos(pos_of_mouse, width_of_one_cell)
				spot = spots[row][col]
				if not started and spot != end_cell:
					start_cell = spot
					start_cell.make_start()
					started = True				
				elif not end and spot != start_cell:
					end_cell = spot
					end_cell.make_end()
					end = True
				elif spot != start_cell and spot != end_cell:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: #RIGHT MOUSE BUTTON
				pos_of_mouse = pygame.mouse.get_pos()
				row, col = get_spot_pos(pos_of_mouse, width_of_one_cell)
				spot = spots[row][col]
				if spot == start_cell:
					started = False
				elif spot == end_cell:
					end = False
				spot.reset()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					bfs(start_cell, end_cell, spots)


#pygame.display.update()
main()




