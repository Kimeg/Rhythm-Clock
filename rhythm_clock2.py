import pygame as pg
import numpy as np
import math

class System:
	def __init__(self):
		self.center = (WIDTH/2, HEIGHT*3/4)
		self.running = True

		self.marbles = [Marble(i, i*20, (int(200/N)*i, 150, 20), self.center, i*0.001+0.01) for i in range(N+1)]
		return

	def render(self):

		while self.running:
			for event in pg.event.get():
				if event.type==pg.QUIT:
					self.running = False

			window.fill((0,0,0))

			pg.draw.line(window, (200,200,200), self.center, (self.center[0]+math.cos(FOV*np.pi/180)*RADIUS, self.center[1]-math.sin(FOV*np.pi/180)*RADIUS), 3)
			pg.draw.line(window, (200,200,200), self.center, (self.center[0]-math.cos(FOV*np.pi/180)*RADIUS, self.center[1]-math.sin(FOV*np.pi/180)*RADIUS), 3)

			[marble.update() for marble in self.marbles]
			[self.marbles[i].render(self.marbles[(i+1)%len(self.marbles)].pos) for i in range(len(self.marbles))]

			pg.display.update()

		pg.quit()
		return

class Marble:
	def __init__(self, index, radius, color, center, speed):
		self.index = index
		self.radius = radius
		self.color = color 
		self.center = center 
		self.angle = 45 
		self.direction = 1
		self.speed = speed
		return

	def update(self):
		self.angle += self.direction*self.speed 
		if self.angle >= 135 or self.angle<=45:
			self.direction *= -1

		self.pos = (math.cos(self.angle*np.pi/180)*self.radius, -math.sin(self.angle*np.pi/180)*self.radius)
		return

	def render(self, pos):
		if self.index<N:
			pg.draw.line(window, (200,200,200), (self.pos[0]+self.center[0], self.pos[1]+self.center[1]), (pos[0]+self.center[0], pos[1]+self.center[1]))
		pg.draw.circle(window, self.color, (self.pos[0]+self.center[0], self.pos[1]+self.center[1]), 5)
		return

def main():
	system = System()
	system.render()
	return

if __name__=="__main__":
	WIDTH, HEIGHT = 800, 800

	FOV = 45
	RADIUS = WIDTH/2
	A_SPEED = 0.1
	N = 20

	pg.init()

	pg.mixer.init()

	window = pg.display.set_mode((WIDTH, HEIGHT))

	pg.display.set_caption("Rhythm Marbles")

	main()