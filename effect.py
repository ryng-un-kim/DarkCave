from pico2d import *
import game_world
import game_framework
import player
import main

TIME_PER_ACTION = 0.2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Effect:
    image = None

    def __init__(self, x = 0, y = 0, x_velocity = 1, y_velocity = 1):
        self.x, self.y= x, y
        self.see_right_frame = 120
        self.frame = 0
        self.SIZE = 96
        self.timer = 5
        self.x_velocity, self.y_velocity = x_velocity, y_velocity
        if Effect.image == None:
            self.image = load_image('Attack.png')

    def draw(self):
        if main.see_right:
            self.image.clip_draw(int(self.frame) * self.SIZE, self.see_right_frame, 96, 120, self.x + 40, self.y - 10)
        else:
            self.image.clip_draw(int(self.frame) * self.SIZE, self.see_right_frame, 96, 120, self.x - 40, self.y - 10)

    def update(self):
        self.x += self.x_velocity * game_framework.frame_Time
        self.y += self.y_velocity * game_framework.frame_Time
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_Time) % 5

        if self.frame > 4:
            game_world.remove_object(self)
        if main.see_right:
            self.see_right_frame = 240
        else:
            self.see_right_frame = 0

