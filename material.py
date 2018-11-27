from pico2d import *
import random
import inventory_state

class MaterialStone:
    image = None

    def __init__(self):
        self.x = random.randint(100, 1600)
        self.y = random.randint(200, 900)
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
        draw_rectangle(*self.get_hitbox())


class IvenMaterialStone:
    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.font = load_font('ENCR10B.TTF', 16)
        self.count = 0
        if IvenMaterialStone.image == None:
            IvenMaterialStone.image = load_image('resource\stone.png')


    def get_hitbox(self):
        return self.x - 10, self.y - 10, \
               self.x + 10, self.y + 10

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 32, 32, self.x, self.y)
        draw_rectangle(*self.get_hitbox())

class MaterialWood:
    image = None

    def __init__(self):
        self.x = random.randint(100, 1600)
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
        draw_rectangle(*self.get_hitbox())


class InvenMaterialWood:
    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        if InvenMaterialWood.image == None:
            InvenMaterialWood.image = load_image('resource\wood.png')


    def get_hitbox(self):
        return self.x - 10, self.y - 10, \
               self.x + 10, self.y + 10

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 32, 32, self.x, self.y)
        draw_rectangle(*self.get_hitbox())