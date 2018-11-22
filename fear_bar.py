from pico2d import *


class PlayerFear:
    image = None
    def __init__(self, x, y):
        self.x = x+ 140
        self.y = y
        self.frame = 0
        if PlayerFear.image == None:
            PlayerFear.image = load_image('resource\Fear.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.frame, 0, 128, 16, self.x, self.y)
