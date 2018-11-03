from pico2d import *
import settings
import game_framework
import player
import main

TIME_PER_ACTION = 0.2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Effect:
    image = None

    def __init__(self, x = 0, y = 0, velx = 1, vely = 1):
        self.x, self.y= x, y
        self.frame2 = 120
        self.frame = 0
        self.SIZE = 96
        self.timer = 5
        self.velx, self.vely = velx, vely
        if Effect.image == None:
            self.image = load_image('Attack.png')

    def draw(self):
        if main.way:
            self.image.clip_draw(int(self.frame) * self.SIZE, self.frame2, 96, 120, self.x + 40, self.y - 10)
        else:
            self.image.clip_draw(int(self.frame) * self.SIZE, self.frame2, 96, 120, self.x - 40, self.y - 10)

    def update(self):
        self.x += self.velx * game_framework.frame_Time
        self.y += self.vely * game_framework.frame_Time
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_Time) % 5

        if self.frame > 4:
            settings.remove_object(self)
        if main.way:
            self.frame2 = 240
        else:
            self.frame2 = 0

