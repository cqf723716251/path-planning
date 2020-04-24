import random
from math import hypot,inf
import numpy
import pygame as pg
import time

WIDTH = 0
HEIGHT = 0
MAX_SEARCH = 10000
THRESHOLD = 30
node_list = []
EDGE_COLOR = (0,100,255) # lake blue
PATH_COLOR = (255,100,0) # orange
NODE_COLOR = (100,0,255) # purple
BACKGROUND = (255,255,255) # white
NODE_RADIUS = 3

pg.init()

class Node:
	def __init__(self, pos, parent):
		self.pos = pos
		self.parent = parent

def run(main_screen, map_surf, path_surf, start, end):
	global node_list
	print("Finding path by RRT...")
	running = True
	success = True
	path = []
	i = 1
	# initialize start and end node
	start_node = Node((start[0],start[1]), None)
	end_node = Node((end[0],end[1]), None)
	# print("start: ",start_node.pos,". end: ",end_node.pos)
	path_surf.image.fill(BACKGROUND)
	WIDTH = map_surf.image.get_width()
	HEIGHT = map_surf.image.get_height()
	# print("WIDTH: ", WIDTH, ", HEIGHT: ", HEIGHT)
	# add start point to node_list and start rrt
	node_list.append(start_node)

	while running:
		# time.sleep(0.1)
		# quit path searching when user press ESC
		for e in pg.event.get():
			if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
				print("Path searching terminated!")
				node_list = []
				return None
		# generate a random node on map
		rand_node = (int(random.random()*WIDTH), int(random.random()*HEIGHT))
		nearest_node = findNearestNode(rand_node)
		next_node = getNextNode(rand_node, nearest_node)
		# next_node = Node(rand_node, nearest_node)
		# print("======")
		# print("rand node", rand_node)
		# print("nearest node", nearest_node.pos)
		# print("next node", next_node.pos)

		# check collision
		test_line = pg.draw.line(path_surf.image, EDGE_COLOR, next_node.pos, nearest_node.pos)
		collision = pg.sprite.collide_mask(path_surf, map_surf)
		# print(collision)
		# abandon this attempt if test line collides with obstacle
		if collision != None:
			# remove the test line if it collides with obstacle
			path_surf.image.fill(BACKGROUND, test_line)
			continue
		else:
			# add new node to list
			node_list.append(next_node)
			# draw new node and edge
			pg.draw.circle(path_surf.image, NODE_COLOR, next_node.pos, NODE_RADIUS)
			line = pg.draw.line(main_screen, EDGE_COLOR, next_node.pos, nearest_node.pos)
			circle = pg.draw.circle(main_screen, NODE_COLOR, next_node.pos, NODE_RADIUS)
			pg.display.update([line,circle])

		# stop searching if the end node is reachable
		if getDistance(next_node.pos, end_node.pos) <= THRESHOLD:
			# check collision
			test_line = pg.draw.line(path_surf.image, EDGE_COLOR, next_node.pos, end_node.pos)
			collision = pg.sprite.collide_mask(path_surf, map_surf)
			# abandon this attempt if test line collides with obstacle
			if collision != None:
				# remove the test line if it collides with obstacle
				path_surf.image.fill(BACKGROUND, test_line)
			else:
				# draw edge and node
				pg.draw.circle(path_surf.image, NODE_COLOR, end_node.pos, NODE_RADIUS)
				line = pg.draw.line(main_screen, EDGE_COLOR, next_node.pos, end_node.pos)
				circle = pg.draw.circle(main_screen, NODE_COLOR, next_node.pos, NODE_RADIUS)
				pg.display.update([line,circle])

				end_node.parent = next_node
				node_list.append(end_node)
				break
		# increase i after each attempt
		if i >= MAX_SEARCH:
			print("Max search number reached! Failed to find a path using RRT")
			running = False
			success = False
		else:
			i = i + 1

	if success == True:
		print("Path found in ",i," attempts.")
		path = findPath(main_screen, path_surf, node_list)

		# end of path searching
		running = True
		while running:
			for e in pg.event.get():
				# press ESC or click X to quit
				if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
					running = False
				elif e.type == pg.QUIT:
					running = False

	node_list = []
	return path

# find the nearest node to the random node
def findNearestNode(rand_node):
	global node_list
	# find the nearest node to the random node
	nearest_dist = inf
	for node in node_list:
		current_dist = getDistance(node.pos, rand_node)
		if current_dist < nearest_dist:
			nearest_node = node
			nearest_dist = current_dist
	return nearest_node

# extend the tree toward the direction of random node
def getNextNode(rand_pos, nearest_node):
	if getDistance(rand_pos, nearest_node.pos) <= THRESHOLD:
		next_node = Node(rand_pos, nearest_node)
		return next_node
	else:
		try:
			# use absolute value of theta
			theta = abs(numpy.arctan((rand_pos[0] - nearest_node.pos[0])/(rand_pos[1] - nearest_node.pos[1])))
			if rand_pos[0] < nearest_node.pos[0]:
				next_x = int(round(nearest_node.pos[0] - THRESHOLD*numpy.sin(theta)))
			else:
				next_x = int(round(nearest_node.pos[0] + THRESHOLD*numpy.sin(theta)))
			if rand_pos[1] < nearest_node.pos[1]:
				next_y = int(round(nearest_node.pos[1] - THRESHOLD*numpy.cos(theta)))
			else:
				next_y = int(round(nearest_node.pos[1] + THRESHOLD*numpy.cos(theta)))
			# print("Next X: ",next_node.pos[0],"; Next Y: ",next_node.pos[1])
			next_node = Node((next_x,next_y), nearest_node)
			return next_node
		except:
			# when rand_node.pos[1] = nearest_node.pos[1]
			if rand_pos[0] < nearest_node.pos[0]:
				next_x = nearest_node.pos[0] - THRESHOLD
			else:
				next_x = nearest_node.pos[0] + THRESHOLD
			next_y = nearest_node.pos[1]
			next_node = Node((next_x,next_y), nearest_node)
			return next_node

# find the list of nodes that the robot will go through
def findPath(main_screen, path_surf, node_list):
	path = []
	next_node = node_list[-1]
	# path.append((last_node.pos[0],last_node.pos[1]))
	while next_node.parent is not None:
		# append last node to path
		path.append(next_node.pos)
		# paint path
		pg.draw.line(path_surf.image, PATH_COLOR, next_node.pos, next_node.parent.pos)
		# move to next node
		next_node = next_node.parent
	# add last node (start node) to path
	path.append(next_node.pos)
	main_screen.blit(path_surf.image, (0,0))
	pg.display.flip()
	path = path[::-1]
	# print("Path found by RRT: ",path)
	print("Path found by RRT!")
	lenth = getPathLength(path)
	print("length: ",lenth)
	print("==================================================================")
	return path

# calculate the length of path
def getPathLength(path):
	length = 0
	index = 0
	while index+1 < len(path):
		length += getDistance(path[index],path[index+1])
		index += 1
	return length

# get distance between two nodes
def getDistance(pos_1, pos_2):
	return hypot(pos_2[0]-pos_1[0], pos_2[1]-pos_1[1])