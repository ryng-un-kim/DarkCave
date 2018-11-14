from pico2d import *
import game_framework
import game_world
import main

TIME_PER_ACTION = 2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4


class Skeleton:
    image = None

    def __init__(self, x=400, y=400):
        self.x = x
        self.y = y
        self.frame = 0
        self.hp = 0.1 * 100
        if Skeleton.image == None:
            Skeleton.image = load_image("resource\Monsters_skele.png") # 611X564

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_Time)%FRAMES_PER_ACTION
    def die(self):
        pass

    def get_hitbox(self):
        return self.x - 12, self.y - 32, self.x + 12, self.y + 32


    def draw(self):
        self.image.clip_draw(int(self.frame) * 96, 768-96, 96, 64, self.x, self.y)
        draw_rectangle(*self.get_hitbox())
