from pico2d import *
import game_framework

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5


class UI:
    image = None
    def __init__(self):
        self.x = 900
        self.y = 100
        self.stone = 0
        self.wood = 0
        self.frame = 1
        self.font = load_font('ENCR10B.TTF', 16)
        if UI.image == None:
            UI.image = load_image('resource\Bonfire_off.png')

    def get_hitbox(self):
        return self.x - 15, self.y - 35, self.x + 20, self.y + 25

    def set_stone_counter(self):
        self.stone += 1

    def set_wood_counter(self):
        self.wood += 1

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_Time) % 5
        self.frame = clamp(1,self.frame,5)
    def draw(self):
        self.font.draw(900, 200, 'Wood:%3d' % self.wood, (255, 255, 255))
        self.font.draw(800, 200, 'Stone:%3d' % self.stone, (255, 255, 255))
        if self.wood < 2 or self.stone < 2:
            self.image.clip_draw(0, 0, 50, 80, self.x, self.y)
        elif self.wood >= 2 and self.stone >= 2:
            self.image.clip_draw(int(self.frame) * 50, 0, 50, 80, self.x, self.y)

        draw_rectangle(*self.get_hitbox())
