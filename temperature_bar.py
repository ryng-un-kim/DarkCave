from pico2d import *


class PlayerTemperature:
    image = None

    def __init__(self, x, y):
        self.x = x+ 280
        self.y = y
        self.frame = 0
        if PlayerTemperature.image == None:
            PlayerTemperature.image = load_image('resource\Temperature.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.frame, 0, 128, 16, self.x, self.y)