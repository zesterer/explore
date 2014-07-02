from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

width = 640
height = 480

def Draw():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()

	Refresh2D(width, height)

	glColor3f(0.9, 0.9, 0.0)
	DrawRectangle(10, 10, 200, 100)

	glutSwapBuffers()

def DrawRectangle(x, y, w, h):
	glBegin(GL_QUADS)
	glVertex2f(x, y)
	glVertex2f(x + w, y)
	glVertex2f(x + w, y + h)
	glVertex2f(x, y + h)
	glEnd()

def Refresh2D(width, height):
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)

window = glutCreateWindow("Test Window!")

glutDisplayFunc(Draw)
glutIdleFunc(Draw)
glutMainLoop()