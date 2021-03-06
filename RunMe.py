import pyglet
from pyglet.gl import *
import PyGM3
from PyGM3 import instance, sound, sprite


class GameSettings:
    delta_timed = True
    batch = pyglet.graphics.Batch()
    def __init__(self):
        pass


class Goblin(instance.Entity):
    def event_create(self):
        self.name = 'test'
        self.sounder = sound.load('beep1.wav')
        self.scale=1
        print(self.name)
        self.name = 10
        self.sprite = sprite.add('annoyed.png', img_number=34, xorg=16, yorg=32, batch=GameSettings.batch)
        self.sprite.scale = self.scale

    def event_step(self):
        #self.x+=1
        pass

    def play_sound(self):
        sound.play(self.sounder)
        #self.sprite.scale = self.scale
        self.scale += 1
        if instance.number(Goblin)<300:
            instance.create(Goblin, x=self.x, y=self.y)
            self.x+=16
            if self.x>640:
                self.x = 16
                self.y+=32
            self.alarm["play_sound"] = 1
            print(instance.number(Goblin))

#create window
window = pyglet.window.Window(800, 600, "OpenGL")
window.set_location(100, 100)


#create an instance with an alarm
instance.create(Goblin,y=100).alarm["play_sound"] = 10

#create an instance
instance.create(Goblin, x=100, y=100)

#create an instance with a special value
bob = instance.create(Goblin, x=100, y=200)

fps_display = pyglet.clock.ClockDisplay()
@window.event
def on_draw():
    window.clear()
    fps_display.draw()
    GameSettings.batch.draw()
    for entity in instance._InstanceController.entity.values():
        entity.event_draw()


if GameSettings.delta_timed is True:
    pyglet.clock.schedule(PyGM3.core.step_controller.delta_update)
else:
    pyglet.clock.schedule(PyGM3.core.step_controller.update)

pyglet.app.run()
