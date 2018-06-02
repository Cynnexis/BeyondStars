# -*-coding:UTF-8 -*
import time

from beyondstars import *
from beyondstars.Body import Body
from beyondstars.Time import Time
from beyondstars.Universe import Universe
from beyondstars.Vector import Vector

u = Universe(name="Solar System")
u.add_bodies(Body(name="Earth", mass=5.972 * pow(10, 24), diameter=12742, position=Vector(149597870700, 0, 0), velocity=Vector(30000, 0, 0), acceleration=Vector(0, 0, 0)))
u.add_bodies(Body(name="Sun", mass=1.989 * pow(10, 30), diameter=1391016, position=Vector(0, 0, 0), velocity=Vector(0, 0, 0), acceleration=Vector(0, 0, 0)))
print(u)
u.start()
time.sleep(1)  # 1s
u.stop()
print(u)

u.save_bodies_as_csv("test")

del u
