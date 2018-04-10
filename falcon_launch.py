from vpython import *
import random
import time

miller_planet = sphere(pos=vector(0,20,0),color=color.orange,radius=0.2,make_trail=True)
earth = sphere(pos=vector(0,-21,-1),color=color.cyan,radius=0.95,make_trail=True)
falcon = arrow(pos=vector(0,-20,-1),axis=vector(0,1,0),color=color.white,shaftwidth=0.4,visible=True)

#smoke_fire = pyramid(pos=vector(0,-20,-1),axis=vector(0,1,-2),color=color.orange,length=0.2,height=0.1,width=0)
#eject1 = sphere(pos=vector(0,12,0),color=color.magenta,radius=0.2)

def rocket_launch():

	miller_planet.radius += 1
	time.sleep(5)

	i = -20
	while i <= 25:
		rate(20)
		falcon.pos.y = i
		time.sleep(0.1)
		i += 0.4

	i = 25
	while i >= 21.2:
		rate(20)
		falcon.pos.y = i
		time.sleep(0.1)
		i -= 0.4

rocket_launch()
