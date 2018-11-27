from pico2d import *
import game_framework

TIME_PER_ACTION = 2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6

class Bonfire:
    image = None
    def __init__(self):
        self.x = 400
        self.y = 400
        self.frame = 0
        if Bonfire.image == None:
            Bonfire.image = load_image('resource\Bonfire.png')

    def set_background(self, bg):
        self.bg = bg

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_Time)%6

    def draw(self):
        self.image.clip_draw(int(self.frame) * 50, 0, 50, 80, self.x - self.bg.window_left, self.y- self.bg.window_bottom)
