import pygame
from pygame.locals import *
from math import pi

pygame.init()
screen = pygame.display.set_mode((512,512))# 设置窗口的大小，单位为像素
pygame.display.set_caption('Path planning')# 设置窗口的标题

# 定义几个颜色
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# 绘制白色作为背景
# screen.fill(BLACK)
map_surf = pygame.surface.Surface((512,512))
try:
	map_surf = pygame.image.load('map.png').convert()
except Exception as e:
	print("File was not found in the same directory.")
	print(e)
else:
	print('Obstacles map loaded.')
	map_surf.set_colorkey(BLACK)

# 绘制一条线
pygame.draw.line(screen, GREEN, [0, 0], [50,30], 5)
# # # 绘制一条抗锯齿的线
# pygame.draw.aaline(screen, GREEN, [0, 50],[50, 80],True)
# # # 绘制一条折线
# pygame.draw.lines(screen, BLACK, False,[[0, 80], [50, 90], [200, 80], [220, 30]], 5)
# # # 绘制一个空心矩形
# pygame.draw.rect(screen, BLACK, [75, 10, 50, 20], 2)
# # # 绘制一个矩形
# pygame.draw.rect(screen, BLACK, [150, 10, 50, 20])
# # # 绘制一个圆
# pygame.draw.circle(screen, BLUE, [60, 250], 40)

running = True
# 主循环！
while running:
	pygame.display.flip()
	# for 循环遍历事件队列
	for event in pygame.event.get():
		# 检测 KEYDOWN 事件: KEYDOWN 是 pygame.locals 中定义的常量，pygame.locals文件开始已经导入
		if event.type == KEYDOWN:
			# 如果按下 Esc 那么主循环终止
			if event.key == K_ESCAPE:
				running = False
		# 检测 QUIT : 如果 QUIT, 终止主循环
		elif event.type == QUIT:
			running = False