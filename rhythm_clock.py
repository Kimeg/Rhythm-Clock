import pygame as pg
import numpy as np
import random
import math 

class Clock:
	def __init__(self):
		self.running = True
		self.ticks = [Tick(i, (150,200, i*10)) for i in range(3, N+1)]
		return

	def update(self):
		[tick.update() for tick in self.ticks]
		return

	def render(self):
		while self.running:
			for event in pg.event.get():
				if event.type==pg.QUIT:
					self.running = False
					break

			window.fill((0,0,0))

			self.update()

			#[pg.draw.circle(window, (100,100,100), (tick.pos.x+OFFSET, tick.pos.y+OFFSET), 3) for tick in self.ticks]
			[tick.render() for tick in self.ticks]

			pg.display.update()
		pg.quit()
		return

class Tick:
	def __init__(self, n, color):
		self.nVertices = n 
		self.radius = n*20
		self.angle = 0
		self.center = (WIDTH/2, HEIGHT/2)

		#self.vertices = [(math.cos(np.pi*2*i/n+(np.pi/2))*self.radius+(WIDTH/2), math.sin(np.pi*2*i/n+(np.pi/2))*self.radius+(HEIGHT/2)) for i in range(n)]
		self.vertices = [(math.cos(np.pi*2*i/n)*self.radius+(WIDTH/2), math.sin(np.pi*2*i/n)*self.radius+(HEIGHT/2)) for i in range(n)]
		self.hits = [0 for _ in range(len(self.vertices))]

		self.index = 0
		self.cur = self.vertices[self.index]
		self.next = self.vertices[(self.index+1)%len(self.vertices)]
		self.pos = self.cur

		self.at_vertex = True
		self.color = color
		return

	def update(self):
		self.angle += A_SPEED
		if self.angle > 360:
			self.angle = 0

		if self.at_vertex:
			#self.dx = (self.next[0]-self.cur[0])/500
			#self.dy = (self.next[1]-self.cur[1])/500
			self.at_vertex = False

		#self.pos = (self.pos[0]+self.dx, self.pos[1]+self.dy)

		self.v = np.array([self.center[0]+math.cos(self.angle*np.pi/180)*5000, self.center[1]+math.sin(self.angle*np.pi/180)*5000])

		x1, x2, x3, x4 = self.center[0], self.v[0], self.cur[0], self.next[0]
		y1, y2, y3, y4 = self.center[1], self.v[1], self.cur[1], self.next[1]

		self.xi = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
		self.yi = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))

		self.vi = np.array([self.xi-self.center[0], self.yi-self.center[1]])

		self.radius = np.sqrt(np.sum(i**2 for i in self.vi))
		#print(self.pos)

		#if abs(self.pos[0]-self.next[0])<0.5 and abs(self.pos[1]-self.next[1])<0.5:
		self.dx = abs(self.xi-self.next[0])
		self.dy = abs(self.yi-self.next[1])
		if self.dx<0.5 and self.dy<0.5:
			self.at_vertex = True

			if self.hits[self.index]==1:
				self.hits[self.index] = 0 
			else:
				self.hits[self.index] = 1 

			self.index = (self.index+1)%len(self.vertices)

			self.cur = self.vertices[self.index]
			self.next = self.vertices[(self.index+1)%len(self.vertices)]
			self.pos = self.cur

			#random.choice(sounds).play()
			random.choice(CHORDS[int(self.angle)//45]).play()

		return

	def render(self):
		for i in range(len(self.vertices)):
			v1 = self.vertices[i]
			v2 = self.vertices[(i+1)%len(self.vertices)]

			pg.draw.line(window, (100, 100, 100), v1, v2)

		for i in range(len(self.vertices)):
			if self.hits[i]==1:
				pg.draw.circle(window, (i*10,self.angle*0.7,200), (self.vertices[(i+1)%len(self.vertices)][0], self.vertices[(i+1)%len(self.vertices)][1]), 8)

		#pg.draw.circle(window, (200,200,200), (self.pos[0], self.pos[1]), 3)
		r = max(int(self.color[0]-self.dx), 0)
		g = max(int(self.color[1]-self.dy), 0)
		b = max(int(self.color[2]-self.dx), 0)
		pg.draw.circle(window, (r, g, b), (self.center[0]+math.cos(self.angle*np.pi/180)*self.radius, self.center[1]+math.sin(self.angle*np.pi/180)*self.radius), 5)
		pg.draw.circle(window, (255, 255, 255), (self.center[0]+math.cos(self.angle*np.pi/180)*self.radius, self.center[1]+math.sin(self.angle*np.pi/180)*self.radius), 5, 1)
		return

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		return

	def update(self, angle, radius):
		self.x = int(math.cos(angle*np.pi/180)*radius)
		self.y = int(math.sin(angle*np.pi/180)*radius)
		return

def main():
	clock = Clock()
	clock.render()
	return

if __name__=="__main__":
	WIDTH, HEIGHT = 800, 800
	OFFSET = int(WIDTH/2)
	A_SPEED = 0.015
	N = 10

	pg.init()
	pg.mixer.init()

	sounds = [
			#pg.mixer.Sound("piano/A3.mp3"),
			#pg.mixer.Sound("piano/B3.mp3"),
			pg.mixer.Sound("piano/C3.mp3"),
			#pg.mixer.Sound("piano/D3.mp3"),
			pg.mixer.Sound("piano/Eb3.mp3"),
			#pg.mixer.Sound("piano/F3.mp3"),
			pg.mixer.Sound("piano/G3.mp3"),
			#pg.mixer.Sound("piano/Bb3.mp3"),
			pg.mixer.Sound("piano/D4.mp3"),
	]

	CHORDS = [
		[
			pg.mixer.Sound("piano/Eb4.mp3"),
			pg.mixer.Sound("piano/Gb4.mp3"),
			pg.mixer.Sound("piano/Bb3.mp3"),
			pg.mixer.Sound("piano/Db5.mp3"),
		],
		[
			pg.mixer.Sound("piano/Gb3.mp3"),
			pg.mixer.Sound("piano/Bb3.mp3"),
			pg.mixer.Sound("piano/Db3.mp3"),
			pg.mixer.Sound("piano/E4.mp3"),
		],
		[
			pg.mixer.Sound("piano/B3.mp3"),
			pg.mixer.Sound("piano/Eb4.mp3"),
			pg.mixer.Sound("piano/Gb3.mp3"),
			pg.mixer.Sound("piano/A4.mp3"),
			pg.mixer.Sound("piano/Db5.mp3"),
		],
		[
			pg.mixer.Sound("piano/Gb3.mp3"),
			pg.mixer.Sound("piano/A3.mp3"),
			pg.mixer.Sound("piano/Db3.mp3"),
			pg.mixer.Sound("piano/F4.mp3"),
		],
		[
			pg.mixer.Sound("piano/C4.mp3"),
			pg.mixer.Sound("piano/E4.mp3"),
			pg.mixer.Sound("piano/Gb4.mp3"),
			pg.mixer.Sound("piano/Bb4.mp3"),
		],
		[
			pg.mixer.Sound("piano/B3.mp3"),
			pg.mixer.Sound("piano/E4.mp3"),
			pg.mixer.Sound("piano/Gb4.mp3"),
			pg.mixer.Sound("piano/Bb4.mp3"),
		],
		[
			pg.mixer.Sound("piano/Ab3.mp3"),
			pg.mixer.Sound("piano/C4.mp3"),
			pg.mixer.Sound("piano/Eb3.mp3"),
			pg.mixer.Sound("piano/Gb4.mp3"),
			pg.mixer.Sound("piano/Bb4.mp3"),
			pg.mixer.Sound("piano/Db5.mp3"),
			pg.mixer.Sound("piano/E5.mp3"),
		],
		[
			pg.mixer.Sound("piano/Eb4.mp3"),
			pg.mixer.Sound("piano/Gb4.mp3"),
			pg.mixer.Sound("piano/Bb3.mp3"),
			pg.mixer.Sound("piano/Db5.mp3"),
		],
	]

	window = pg.display.set_mode((WIDTH, HEIGHT))
	pg.display.set_caption("Rhythm Clock")

	main()
