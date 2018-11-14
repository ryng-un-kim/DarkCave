from pico2d import *
import main


class Map:
    image = None

    def __init__(self):
        self.x = main.VIEW_WIDTH/2
        self.y = main.VIEW_HEIGHT/2
        if Map.image == None:
            Map.image = load_image('resource\map.png')

    def update(self):
        pass

    def get_hitbox(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)