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
START = (1,1)
END = (170, 85)
BACKGROUND = (255,255,255)

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

def get_map_size(image_path):
	map = cv2.imread(image_path)
	HEIGHT = map.shape[0]
	WIDTH = map.shape[1]
	print("HEIGHT: ", HEIGHT, ", WIDTH: ", WIDTH)
	return HEIGHT,WIDTH

def load_map(path):
	try:
		surf = pg.image.load(image_path).convert()
	except:
		print("'map.png' file was not found in the same directory.")
		return
	else:
		print('Map loaded.')
		surf.set_colorkey(BACKGROUND)
		return surf

def main():
	global HEIGHT,WIDTH
	HEIGHT,WIDTH = get_map_size(image_path)
	main_screen = pg.display.set_mode((WIDTH, HEIGHT))
	# map_surf = pg.surface.Surface((WIDTH, HEIGHT))
	# load_map(map_surf, image_path)
	map_surf = load_map(image_path)

	done = False
	while not done:

		for e in pg.event.get():
			# If the user clicks the window's 'x', closes the app.
			if e.type == pg.QUIT:
				done = True 

		main_screen.fill(BACKGROUND)
		main_screen.blit(map_surf, (0,0))
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