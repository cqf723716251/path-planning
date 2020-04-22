import random
import cv2
import os
import numpy as np
import sys
import pygame as pg

from planner import astar,rrt

pg.init()

image_path = "map.png"
HEIGHT = 0
WIDTH = 0
START = (90,80)
END = (150, 120)
BACKGROUND = (255,255,255)
START_COLOR = (0,255,0) # GREEN
END_COLOR = (255,0,0) # RED

# point block
class Block(pg.sprite.Sprite):
	def __init__(self, color, pos):
		super().__init__()
		radius = 10
		self.image = pg.surface.Surface((2*radius,2*radius))
		self.rect = self.image.get_rect(topleft=pos)
		self.image.fill(color)
		# self.image.fill(BACKGROUND)
		self.image.set_colorkey(BACKGROUND)
		# pg.draw.circle(self.image, color, pos, radius)

# obstacle surface
class Surf(pg.sprite.Sprite):
	global HEIGHT,WIDTH
	def __init__(self):
		super().__init__()
		self.image = pg.surface.Surface((WIDTH, HEIGHT))
		self.rect = self.image.get_rect()
		self.image.set_colorkey(BACKGROUND)
		self.image.fill(BACKGROUND)

# get the size of map image
def get_map_size(image_path):
	map = cv2.imread(image_path)
	HEIGHT = map.shape[0]
	WIDTH = map.shape[1]
	print("HEIGHT: ", HEIGHT, ", WIDTH: ", WIDTH)
	return HEIGHT,WIDTH

def load_map(surf, path):
	try:
		surf.image = pg.image.load(image_path).convert()
	except:
		print("failed to locate 'map.png'")
		return
	else:
		print('Map loaded.')
		surf.image.set_colorkey(BACKGROUND)
		return surf

def main():
	global HEIGHT,WIDTH,START,END
	# fit the window to the size of map
	HEIGHT,WIDTH = get_map_size(image_path)
	main_screen = pg.display.set_mode((WIDTH, HEIGHT))
	# initailize and load map
	map_surf = Surf()
	load_map(map_surf, image_path)
	# initailize start and end point
	start_point = Block(START_COLOR, START)
	end_point = Block(END_COLOR, END)
	# set up sprite group
	sprites = pg.sprite.Group(start_point, end_point,map_surf)
	path_surf = Surf()

	drag = ""
	running = True
	while running:
		for e in pg.event.get():
			# quit only when the window is closed
			if e.type == pg.QUIT:
				running = False 

			elif e.type == pg.KEYDOWN:
				START = start_point.rect.center
				END = end_point.rect.center
				if e.key ==pg.K_1:
					# run astar
					astar_path = astar.run(main_screen, map_surf, path_surf, START, END)
				elif e.key == pg.K_2:
					# Run rrt planner
					rrt_path = rrt.run(main_screen, map_surf, path_surf, START, END)

			elif e.type == pg.MOUSEBUTTONDOWN:
				# drag point
				if e.button == 1: # left mouse button
					if start_point.rect.collidepoint(e.pos):
						drag = "START"
						print("Draging START point...")
					elif end_point.rect.collidepoint(e.pos):
						drag = "END"
						print("Draging END point...")

			elif e.type == pg.MOUSEBUTTONUP:
				# new point location set
				if e.button == 1 and drag != "": # left mouse button
					print("New", drag, "loction: ", e.pos)
					drag = ""

			elif e.type == pg.MOUSEMOTION:
				# dragging point
				if drag == "START":
					start_point.rect.center = e.pos
				elif drag == "END":
					end_point.rect.center = e.pos

		# refresh screen
		main_screen.fill(BACKGROUND)
		# main_screen.blit(map_surf, (0,0))
		sprites.draw(main_screen)
		pg.display.flip()
	# # load map and transfer it to 2d array
	# map = image2array(image_path, HEIGHT, WIDTH)
	# # set start and end point
	# # start = (1, 1)
	# # end = (170, 85)
	# # end = (10,10)
	# print("Start point: ", START)
	# print("End point: ", END)
	# print("==================================================")
	# # analyse path by astar algorithm
	# path_1 = astar.run(map, START, END)
	# print("Number of nodes in A-Star path:", len(path_1))
	# print("A-Star path: ", path_1)
	# print("==================================================")
	# path_2 = rrt.run(map, START, END)
	# if path_2 is not None:
	# 	print("Number of nodes in RRT path:", len(path_2))
	# 	print("RRT path: ", path_2)

if __name__ == '__main__':
	main()

def image2array(path, HEIGHT, WIDTH):
	image = cv2.imread(path,0)
	array = cv2.resize(image,(HEIGHT,WIDTH))
	# array_out = cv2.imwrite("map_out.png", array)
	for i in range(len(array)):
		for j in range(len(array[i])):
			if array[i][j] > 128:
				array[i][j] = 0
			else:
				array[i][j] = 1
	np.savetxt('map.txt',array,delimiter=',',fmt='%d')
	# print(array)
	return array
