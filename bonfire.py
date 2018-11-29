from pico2d import *
import game_framework

TIME_PER_ACTION = 2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6

class Bonfire:
    image = None
    def __init__(self, x = 400, y = 400):
        self.x = x
        self.y = y
        self.frame = 0
        self.create_sound = load_wav('resource\create_bonfire.wav')
        self.create_sound.set_volume(32)
        self.create_sound.play()
        if Bonfire.image == None:
            Bonfire.image = load_image('resource\Bonfire.png')

    def set_background(self, bg):
        self.bg = bg

    def drag(self, cursor):
        self.x = cursor.x - 8 + self.bg.window_left
        self.y = cursor.y + 8 + self.bg.window_bottom

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_Time)%6

    def draw(self):
        self.image.clip_draw(int(self.frame) * 50, 0, 50, 80, self.x - self.bg.window_left, self.y- self.bg.window_bottom)

