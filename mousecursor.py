from pico2d import *
import game_framework

VIEW_WIDTH = 1024
VIEW_HEIGHT = 768
class MouseCursor:
    image = None

    def __init__(self, x=0, y=0):
        hide_cursor()
        self.x = x
        self.y = y
        if MouseCursor.image == None:
            MouseCursor.image = load_image("resource\mouse3.png")


    def position(self, x=0, y=0):
        self.x = x
        self.y = y

    def get_hitbox(self):
        return self.x - 8, self.y, self.x, self.y + 8


    def update(self):
        self.image.x = self.x
        self.image.y = self.y

    def draw(self):
        self.image.draw(self.image.x, self.image.y)







