from pico2d import *


class Inventory:
    image = None
    def __init__(self):
        self.x = 200
        self.y = 90
        if Inventory.image == None:
            Inventory.image = load_image('resource\inventory.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)