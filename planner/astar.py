import pygame as pg

WIDTH = 0
HEIGHT = 0
EDGE_COLOR = (0,100,255) # lake blue
PATH_COLOR = (255,100,0) # orange
NODE_COLOR = (100,0,255) # purple
BACKGROUND = (255,255,255) # white
NODE_RADIUS = 3
RANGE = 1

pg.init()

class Node():
	def __init__(self, pos, parent):
		self.pos = pos
		self.parent = parent

		self.g = 0
		self.h = 0
		self.f = 0

	def __eq__(self, other):
		return self.pos == other.pos

class Surf(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.surface.Surface((WIDTH, HEIGHT))
		self.rect = self.image.get_rect()
		self.image.set_colorkey(BACKGROUND)
		self.image.fill(BACKGROUND)


def run(main_screen, map_surf, path_surf, start, end):
	global WIDTH,HEIGHT
	print("Finding path by A*...")
	# Initializing start_node and end_node
	start_node = Node(start, None)
	start_node.g = start_node.h = start_node.f = 0
	end_node = Node(end, None)
	end_node.g = end_node.h = end_node.f = 0
	path_surf.image.fill(BACKGROUND)
	WIDTH = map_surf.image.get_width()
	HEIGHT = map_surf.image.get_height()
	# Initialize open and closed list
	open_list = []
	closed_list = []

	# Add the start node to open lise
	open_list.append(start_node)

	# Loop until you find the end
	while len(open_list) > 0:

		# Get the current node
		current_node = open_list[0]
		current_index = 0
		# find the node with lowest f in open list
		for index, item in enumerate(open_list):
			if item.f < current_node.f:
				current_node = item
				current_index = index

		# Move the current_node to closed list
		open_list.pop(current_index)
		closed_list.append(current_node)

		# print(current_node.pos)
		# Found the goal
		# End seaching until end_node is reached
		if current_node == end_node:
			path = findPath(main_screen, path_surf, current_node)

			running = True
			while running:
				for e in pg.event.get():
					if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
						running = False
					elif e.type == pg.QUIT:
						running = False
			return path

		# Generate neighbours, searching for a path
		neighbours = []
		# Searchign neighbourhoods
		for new_position in [(0, -RANGE), (0, RANGE), (-RANGE, 0), (RANGE, 0), (-RANGE, -RANGE), (-RANGE, RANGE), (RANGE, -RANGE), (RANGE, RANGE)]:

			# Get neignbour node position
			node_position = (current_node.pos[0] + new_position[0], current_node.pos[1] + new_position[1])

			# Check the node is in the board
			if node_position[0] > (WIDTH-1) or node_position[0] < 0 or node_position[1] > (HEIGHT-1) or node_position[1] < 0:
				# print("OUT OF BOUND!")
				continue

			# Check the node is not a obstacle
			# create test_surf for collision detection
			test_surf = Surf()
			test_rect = pg.draw.rect(test_surf.image, NODE_COLOR, (node_position[0], node_position[1], 1, 1))
			collision = pg.sprite.collide_mask(test_surf, map_surf)
			# reset test_surf
			test_surf.image.fill(BACKGROUND, test_rect)
			if collision != None:
				# print("OBSTACLE HIT!")
				continue

			# Create new node
			new_node = Node(node_position, current_node)

			# Append
			neighbours.append(new_node)

			# draw new node
			# print(new_node.pos)
			pg.draw.line(path_surf.image, EDGE_COLOR, new_node.pos, current_node.pos)
			pg.draw.circle(path_surf.image, NODE_COLOR, new_node.pos, NODE_RADIUS)
			line = pg.draw.line(main_screen, EDGE_COLOR, new_node.pos, current_node.pos)
			circle = pg.draw.circle(main_screen, NODE_COLOR, new_node.pos, NODE_RADIUS)
			pg.display.update([line,circle])

		# Retreive neighbours
		for neighbour in neighbours:

			# If neighbour is in the closed list then ignore it
			# for closed_neighbour in closed_list:
			#    if neighbour == closed_neighbour:
			#       continue
			if neighbour in closed_list:
				continue

			# Calculate the f, g, and h values
			neighbour.g = current_node.g + 1 # distance between parent to neighbour
			neighbour.h = ((neighbour.pos[0] - end_node.pos[0]) ** 2) + ((neighbour.pos[1] - end_node.pos[1]) ** 2) # Pythagorean Theorem
			neighbour.f = neighbour.g + neighbour.h # f=g+h

			# If neighbour is not in the open list
			# and the path is better
			# then add the neighbour to open list
			for open_node in open_list:
				if neighbour == open_node and neighbour.f > open_node.f:
					continue
			open_list.append(neighbour)


def findPath(main_screen, path_surf, current_node):
	path = []
	# add nodes to path
	while current_node.parent is not None:
		path.append(current_node.pos)
		pg.draw.line(path_surf.image, PATH_COLOR, current_node.pos, current_node.parent.pos)
		current_node = current_node.parent
	# start node is the last node
	path.append(current_node)
	main_screen.blit(path_surf.image, (0,0))
	pg.display.flip()
	print("Path found by A*!")
	# Return reversed path
	return path[::-1]