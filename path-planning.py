import cv2
import numpy as np
from planner import astar

image_path = "map.png"
HEIGHT = 512
WIDTH = 512
START = (1,1)
END = (238,39)
map = []

def convertMap(path):
	image = cv2.imread(path, 0)
	image = cv2.resize(image, (HEIGHT, WIDTH))
	image_out = cv2.imwrite("map_converted.png", 255*image)
	for i in range(len(image)):
		for j in range(len(image[i])):
			if image[i][j] < 128:
				image[i][j] = 1
			else:
				image[i][j] = 0
	# save map to txt
	np.savetxt("map.txt", image, fmt="%d")
	return image

if __name__ == '__main__':
	map = convertMap(image_path)
	# path_astar = astar.run(map, START, END)
	# print(path_astar)
	# print("This is my own program.")