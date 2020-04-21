class Node():
	"""A node class for A* Pathfinding"""

	def __init__(self, parent=None, position=None):
		self.parent = parent
		self.position = position

		self.g = 0
		self.h = 0
		self.f = 0

	def __eq__(self, other):
		return self.position == other.position

class astar:
	def __init__(self):
		

	def run(map, start, end):
		"""Returns a list of tuples as a path from the given start to the given end in the given map"""

		# Initializing start_node and end_node
		start_node = Node(None, start)
		start_node.g = start_node.h = start_node.f = 0
		end_node = Node(None, end)
		end_node.g = end_node.h = end_node.f = 0

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

			# Found the goal
			# End seaching until end_node is reached
			if current_node == end_node:
				path = []
				current = current_node
				# add nodes to path
				while current is not None:
					path.append(current.position)
					current = current.parent
				# Return reversed path
				return path[::-1]

			# Generate children, searching for a path
			children = []
			# Searchign neighbourhoods
			for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:

				# Get neignbour node position
				node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

				# Check the node is in the board
				if node_position[0] > (len(map) - 1) or node_position[0] < 0 or node_position[1] > (len(map[len(map)-1]) -1) or node_position[1] < 0:
					continue

				# Check the node is not a obstacle
				if map[node_position[0]][node_position[1]] != 0:
					continue

				# Create new node
				new_node = Node(current_node, node_position)

				# Append
				children.append(new_node)

			# Retreive children
			for child in children:

				# If child is in the closed list then ignore it
				# for closed_child in closed_list:
				#    if child == closed_child:
				#       continue
				if child in closed_list:
					continue

				# Calculate the f, g, and h values
				child.g = current_node.g + 1 # distance between parent to child
				child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2) # Pythagorean Theorem
				child.f = child.g + child.h # f=g+h

				# If child is not in the open list
				# and the path is better
				# then add the child to open list
				for open_node in open_list:
					if child == open_node and child.f > open_node.f:
						continue
				open_list.append(child)