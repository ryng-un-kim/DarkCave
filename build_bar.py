from pico2d import *


class Build:
    image = None
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        if Build.image == None:
            Build.image = load_image('resource\Build_bar.png')

    def set_background(self, bg):
        self.bg = bg

    def set_player(self, player):
        self.player = player

    def update(self):
        self.x = self.player.x - self.bg.window_left
        self.y = self.player.y - self.bg.window_bottom

    def draw(self):
        self.image.clip_draw(0,0,self.frame,4,self.x, self.y - 16)