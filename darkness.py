from pico2d import *


class Darkness:
    image = None

    def __init__(self):
        self.x = 0
        self.y = 0
        if Darkness.image == None:
            Darkness.image = load_image('resource\darkness.png')

    def set_background(self, bg):
        self.bg = bg
        self.x = bg.w / 2
        self.y = bg.h / 2

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0,0,self.bg.w,self.bg.h, self.x, self.y)
