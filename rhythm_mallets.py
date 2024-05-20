from playsound import playsound
import pygame as pg
import numpy as np
import threading
import random
import math
import time
import os


class System:
	def __init__(self):
		self.mallets = [Mallet(i, (i+1)*5, (120-i*2,5*i,150+i*2), 10/5000) for i in range(5, N)]
		#self.mallets = [Mallet(i, (i+1)*int(N/10), (int(N*2.5)-i*2,int(N/10)*i,int(N*3)+i*2), 10/100000) for i in range(5, N)]
		self.running = True
		return

	def render(self):
		t0 = time.time()
		hit_t = time.time()
		hit_color = (150, 150, 150)
		while self.running:
			for event in pg.event.get():
				if event.type==pg.QUIT:
					self.running = False

			window.fill((0,0,0))

			pg.draw.circle(window, (255,255,255), CENTER, 300, 2)

			if time.time()-hit_t<DELAY:
				bar_color = hit_color
			else:
				bar_color = (150, 150, 150)

			pg.draw.line(window, bar_color, CENTER, (CENTER[0], CENTER[1]-(HEIGHT/2)), 2)

			for mallet in self.mallets:
				hit = mallet.update(t0)

				if not hit==None:
					hit_t = time.time()
					hit_color = hit

			[mallet.render() for mallet in self.mallets]

			pg.display.update()

		pg.quit()
		return

class Mallet:
	def __init__(self, index, radius, color, speed):
		self.index = index
		#self.t_start = random.random()*5
		self.t_start = radius*0.01
		self.radius = radius
		self.color = color 
		self.speed = math.log(radius/10)*0.0001
		self.direction = -1
		#self.direction = random.choice([-1,1])
		self.offset = math.acos((2*(self.radius**2)-SIZE**2)/(2*(self.radius**2)))
		#print(self.offset*180/np.pi)
		self.angle = (np.pi/2)+self.direction*self.offset if self.direction==1 else (np.pi*5/2)+self.direction*self.offset
		return

	def update(self, t):
		if time.time()-t<self.t_start:
			return

		prev_angle = self.angle

		self.angle += self.direction*self.speed

		#if self.index==5:
		#	print(self.angle*180/np.pi, abs(self.angle-(np.pi/2)), self.offset, self.offset*180/np.pi)

		if self.angle-(np.pi/2)<self.offset or self.angle-(np.pi*5/2)>-self.offset:
			self.direction *= -1
			self.angle = prev_angle 
			#playsound(audio_files[self.index])
			audio = threading.Thread(target=play_audio, args=(audio_files[self.index],))
			audio.start()
			return self.color
		return None

	def render(self):
		pos = (CENTER[0]+math.cos(self.angle)*self.radius, CENTER[1]-math.sin(self.angle)*self.radius)
		pg.draw.line(window, self.color, CENTER, pos)
		pg.draw.circle(window, self.color, pos, SIZE)
		pg.draw.circle(window, (255,255,255), pos, SIZE, 1)
		return 

def play_audio(audio_file):
	playsound(audio_file)
	return

def main():
	system = System()
	system.render()
	return

if __name__=="__main__":
	WIDTH, HEIGHT = 800, 800
	CENTER = (WIDTH/2, HEIGHT/2)
	SIZE = 10
	A_SPEED = 0.005
	N = 50
	DELAY = 0.08

	pg.init()
	pg.mixer.init()

	window = pg.display.set_mode((WIDTH, HEIGHT))
	pg.display.set_caption("Rhythm Mallets")

	audio_files = sorted(os.listdir('./piano'), key=lambda x: x[-1])
	main()	