from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from random import randint
import math

width, height = 640, 480
fwidth, fheight = 40, 30
sinterval = 80
interval = sinterval
tick = 0

def Refresh2D(width, height, fwidth, fheight):
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0.0, fwidth, 0.0, fheight, 0.0, 1.0)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

def DrawRect(x, y, width, height):
	glBegin(GL_QUADS)
	glVertex2f(x, y)
	glVertex2f(x + width, y)
	glVertex2f(x + width, y + height)
	glVertex2f(x, y + height)
	glEnd()

def Draw():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	Refresh2D(width, height, fwidth, fheight)

	DrawSnake()
	DrawFood()

	glutSwapBuffers()

def DrawSnake():
	if dead_time % 2 == 1:
		glColor3f(0.1, 0.1, 0.1)
	else:
		glColor3f(1.0, 0.2, 0.2)
	for x, y in snake:
		DrawRect(x, y, 1, 1)

def DrawFood():
	glColor3f(1.0, 1.0, 0.0)
	for x, y in food:
		DrawRect(x, y, 1, 1)

def PointRectIntersect(x1, y1, x, y, w, h):
	if x1 > x and y1 > y and x1 < x + w and y1 < y + h:
		return True
	return False

def Update(value):
	global tick, dead_time, snake, snake_dir, angle, keys, length, interval

	if dead_time == 0:
		snake.insert(0, AddVectors(snake[0], snake_dir))
		if len(snake) > length:
			snake.pop()

	if snake[0][0] >= fwidth:
		snake[0] = (0, snake[0][1])
	if snake[0][1] >= fheight:
		snake[0] = (snake[0][0], 0)
	if snake[0][0] < 0:
		snake[0] = (fwidth, snake[0][1])
	if snake[0][1] < 0:
		snake[0] = (snake[0][0], fheight)

	for part in snake[2:]:
		if PointRectIntersect(snake[0][0], snake[0][1], part[0], part[1], 1, 1):
			if dead_time == 0:
				dead_time = 10

	(hx, hy) = snake[0]
	for x, y in food:
		if PointRectIntersect(hx, hy, x - 1, y - 1, 2, 2):
			length += 4
			interval -= 1
			x, y = randint(1, fwidth - 1), randint(1, fheight - 1)
			food[0] = (x, y)

	if keys["a"] == True:
		angle -= 20
	if keys["d"]:
		angle += 20

	snake_dir = (math.sin(angle * math.pi / 180), math.cos(angle * math.pi / 180))

	tick += 1
	if dead_time > 0:
		dead_time -= 1
		if dead_time == 0:
			snake = [(20, 15)]
			length = 4
			angle = 90
			interval = sinterval
			snake_dir = (1, 0)

	glutTimerFunc(interval, Update, 0)

def Resize(w, h):
	global width, height
	width = w
	height = h

def AddVectors(v1, v2):
	return (v1[0] + v2[0], v1[1] + v2[1])

def KeyUp(key, x, y):
	global keys
	if key == b"a":
		keys["a"] = False
	if key == b"d":
		keys["d"] = False

def KeyDown(key, x, y):
	global keys
	if key == b"a":
		keys["a"] = True
	if key == b"d":
		keys["d"] = True

	snake_dir = (math.sin(angle * math.pi / 180), math.cos(angle * math.pi / 180))

	#if abs(snake_dir[0] - old[0]) == 2 or abs(snake_dir[1] - old[1]) == 2:
		#snake_dir = old

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)

window = glutCreateWindow("Snake Game")

snake = [(20, 15)]
snake_dir = (1, 0)
length = 4
angle = 90
dead_time = 0

keys = dict()
keys["a"] = False
keys["d"] = False
keys["w"] = False
keys["s"] = False

food = []
x, y = randint(0, fwidth), randint(0, fheight)
food.append((x, y))

glutDisplayFunc(Draw)
glutIdleFunc(Draw)
glutTimerFunc(interval, Update, 0)
glutReshapeFunc(Resize)
glutKeyboardFunc(KeyDown)
glutKeyboardUpFunc(KeyUp)
glutIgnoreKeyRepeat(True)

glutMainLoop()