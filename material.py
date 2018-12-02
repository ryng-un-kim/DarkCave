from pico2d import *
import random

class MaterialStone:
    image = None

    def __init__(self):
        self.x = random.randint(100, 1500)
        self.y = random.randint(200, 950)
        self.font = load_font('ENCR10B.TTF', 16)
        self.count = 0
        self.stone_counter = 0
        if MaterialStone.image == None:
            MaterialStone.image = load_image('resource\stone.png')



    def set_background(self, bg):
        self.bg = bg


    def get_hitbox(self):
        return self.x - 10- self.bg.window_left, self.y - 10- self.bg.window_bottom, \
               self.x + 10- self.bg.window_left, self.y + 10- self.bg.window_bottom

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 32, 32, self.x- self.bg.window_left, self.y- self.bg.window_bottom)
        # draw_rectangle(*self.get_hitbox())






class MaterialWood:
    image = None

    def __init__(self):
        self.x = random.randint(100, 1500)
        self.y = random.randint(200, 900)
        self.font = load_font('ENCR10B.TTF', 16)
        if MaterialWood.image == None:
            MaterialWood.image = load_image('resource\wood.png')

    def set_background(self, bg):
        self.bg = bg


    def get_hitbox(self):
        return self.x - 10- self.bg.window_left, self.y - 10- self.bg.window_bottom, \
               self.x + 10- self.bg.window_left, self.y + 10- self.bg.window_bottom

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 32, 32, self.x - self.bg.window_left, self.y - self.bg.window_bottom)
        # draw_rectangle(*self.get_hitbox())


