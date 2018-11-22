from pico2d import *


class PlayerWater:
    image = None

    def __init__(self, x, y):
        self.x = x + 560
        self.y = y
        self.frame = 0
        if PlayerWater.image == None:
            PlayerWater.image = load_image('resource\Water.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.frame, 0, 128, 16, self.x, self.y)