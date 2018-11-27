from pico2d import *


class CaveDoor:
    image = None
    def __init__(self, x, y):
        self.x, self.y = x, y

        if CaveDoor.image == None:
            CaveDoor.image = load_image('resource\cave_door.png')

    def set_background(self, bg):
        self.bg = bg

    def get_hitbox(self):
        return self.x - 20- self.bg.window_left, \
               self.y- 20- self.bg.window_bottom, \
               self.x + 20- self.bg.window_left, \
               self.y + 20- self.bg.window_bottom

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 70, 70, self.x - self.bg.window_left, self.y- self.bg.window_bottom)
        draw_rectangle(*self.get_hitbox())

