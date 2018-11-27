from pico2d import *


class Light:
    image = None
    def __init__(self, x, y):
        self.x = x
        self.y = y
        if Light.image == None:
            Light.image = load_image('resource\light.png')

    def set_background(self, bg):
        self.bg = bg

    def get_hitbox(self):
        return self.x - 120 - self.bg.window_left, self.y - 120 - self.bg.window_bottom, \
               self.x + 120 - self.bg.window_left, self.y + 120 - self.bg.window_bottom


    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 300, 300, self.x- self.bg.window_left, self.y- self.bg.window_bottom)
        draw_rectangle(*self.get_hitbox())

