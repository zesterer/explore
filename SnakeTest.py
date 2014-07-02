from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from random import randint

width, height = 640, 480
fwidth, fheight = 40, 30
interval = 150
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

def Update(value):
	global tick, dead_time, snake, snake_dir

	if dead_time == 0:
		snake.insert(0, AddVectors(snake[0], snake_dir))
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
		if snake[0] == part and dead_time == 0:
			dead_time = 10

	(hx, hy) = snake[0]
	for x, y in food:
		if hx == x and hy == y:
			snake.append((x, y))
			x, y = randint(1, fwidth - 1), randint(1, fheight - 1)
			food[0] = (x, y)

	tick += 1
	if dead_time > 0:
		dead_time -= 1
		if dead_time == 0:
			snake = [(19, 15), (18, 15), (17, 15), (16, 15)]
			snake_dir = (1, 0)

	glutTimerFunc(interval, Update, 0)

def AddVectors(v1, v2):
	return (v1[0] + v2[0], v1[1] + v2[1])

def Keyboard(*args):
	global snake_dir

	old = snake_dir

	if dead_time == 0:
		if args[0] == b"w":
			snake_dir = (0, 1)
		if args[0] == b"s":
			snake_dir = (0, -1)
		if args[0] == b"a":
			snake_dir = (-1, 0)
		if args[0] == b"d":
			snake_dir = (1, 0)

	if abs(snake_dir[0] - old[0]) == 2 or abs(snake_dir[1] - old[1]) == 2:
		snake_dir = old

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)

window = glutCreateWindow("Snake Game")

snake = [(19, 15), (18, 15), (17, 15), (16, 15)]
snake_dir = (1, 0)
dead_time = 0

food = []
x, y = randint(0, fwidth), randint(0, fheight)
food.append((x, y))

glutDisplayFunc(Draw)
glutIdleFunc(Draw)
glutTimerFunc(interval, Update, 0)
glutKeyboardFunc(Keyboard)

glutMainLoop()