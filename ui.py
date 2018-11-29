from pico2d import *
import game_framework
import main_state
import loading_state
import pickle


TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5


class UI:
    image = None
    def __init__(self):
        self.x = 900
        self.y = 100
        self.frame = 1
        self.day_count = 1
        self.font = load_font('ENCR10B.TTF', 16)
        self.jua_font = load_font('ENCR11B.TTF', 32)
        if UI.image == None:
            UI.image = load_image('resource\Bonfire_off.png')

    def get_hitbox(self):
        return self.x - 15, self.y - 35, self.x + 20, self.y + 25

    def set_stone_counter(self):
        main_state.stone += 1

    def set_wood_counter(self):
        main_state.wood += 1



    def update(self):
        self.day_count = self.day_count
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_Time) % 5
        self.frame = clamp(1,self.frame,5)


    def draw(self):
        self.font.draw(900, 200, 'Wood:%3d' % main_state.wood, (255, 255, 255))
        self.font.draw(800, 200, 'Stone:%3d' % main_state.stone, (255, 255, 255))
        if main_state.wood < 2 or main_state.stone < 2:
            self.image.clip_draw(0, 0, 50, 80, self.x, self.y)
        elif main_state.wood >= 2 and main_state.stone >= 2:
            self.image.clip_draw(int(self.frame) * 50, 0, 50, 80, self.x, self.y)
        self.jua_font.draw(50, 700, 'Day %2.0f' % loading_state.day_count, (255, 255, 255))
        draw_rectangle(*self.get_hitbox())

class MouseClickImage:
    image = None
    def __init__(self, x, y):
        self.x, self.y = x, y
        if MouseClickImage.image == None:
            MouseClickImage.image = load_image('resource\mouse_right_click.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)


