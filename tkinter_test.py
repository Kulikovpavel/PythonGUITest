from Tkinter import *
from math import sqrt
from random import randint
from time import sleep, time


def callback(event):
    print "clicked at", event.x, event.y


class World(object):
    def __init__(self):
        self.entities = []
        self.dt = 1/60.

    def add_entity(self, entity):
        self.entities.append(entity)

    def process(self):
        for entity in self.entities:
            entity.process()


class Entity(object):
    def __init__(self, world):
        self.world = world
        world.add_entity(self)
        self.activities = []

    def add_activity(self, activity):
        self.activities.append(activity)

    def process(self):
        for activity in self.activities:
            activity.process(self)


class Bullet(Entity):
    def __init__(self, world, x, y, sprite, vx=0, vy=0):
        super(Bullet, self).__init__(world)
        self.x = x
        self.y = y
        self.velocity = Vector(vx, vy)
        self.sprite = sprite
        self.image = None


class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __rmul__(self, other):
        return Vector(self.x * other, self.y * other)

    def norm(self):
        length = sqrt(self.x**2 + self.y**2)
        return Vector(self.x/length, self.y/length)


class Gravity(object):
    def __init__(self, magnitude, direction):
        self.magnitude = magnitude
        self.direction = direction.norm()
        self.force = magnitude * direction

    def process(self, entity):
        entity.velocity += entity.world.dt * self.force


class Movement(object):
    def process(self, entity):
        entity.x += entity.world.dt * entity.velocity.x
        entity.y += entity.world.dt * entity.velocity.y


class Renderer(object):
    def __init__(self, canvas, size):
        self.size = size
        self.canvas = canvas

    def process(self, entity):
        half = self.size/2
        if entity.image is None:
            entity.image = self.canvas.create_image(entity.x-half, entity.y - half, image=entity.sprite)
        else:
            coords = self.canvas.coords(entity.image)
            self.canvas.move(entity.image,
                             entity.x - coords[0],
                             entity.y - coords[1])


master = Tk()
w = Canvas(master, width=800, height=800)
w.pack()

# w.create_line(0, 0, 200, 100)
# w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
# w.create_rectangle(50, 25, 150, 75, fill="blue")
world = World()

gravity = Gravity(10, Vector(0, 1))
movement = Movement()
renderer = Renderer(w, 10)

sprite = PhotoImage(file="bullet.gif")

for i in range(100):
    bullet = Bullet(world, 0, 400, sprite, randint(20, 200), randint(-80, -20))
    bullet.add_activity(gravity)
    bullet.add_activity(movement)
    bullet.add_activity(renderer)

w.bind("<Button-1>", callback)


fps = 30
time_delta = 1./fps
# mainloop()
while 1:
    t0 = time()
    world.process()
    t1 = time()
    current_delta = t1 - t0
    if t1-t0 < time_delta:
        sleep(current_delta)
    master.update()
