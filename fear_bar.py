from pico2d import *
import main_state
import random


class PlayerFear:
    image = None

    def __init__(self, x, y):
        self.x = x + 140
        self.y = y
        self.frame = 0
        self.start_timer = get_time()
        self.font = load_font('ENCR10B.TTF', 18)
        self.renew_fear_gauge = main_state.fear_gauge * 128 / 20
        if PlayerFear.image == None:
            PlayerFear.image = load_image('resource\Fear.png')

    def skeleton_collision(self):
        self.end_timer = get_time()
        self.elapsed_timer = self.end_timer - self.start_timer
        if self.elapsed_timer > 2 and main_state.fear_gauge != 0:
            main_state.fear_gauge -= 1
            self.start_timer = get_time()

    def set_background(self, bg):
        self.bg = bg

    def set_position(self, player):
        self.player = player

    def get_hitbox(self):
        return self.player.x - 128 - self.bg.window_left, \
                self.player.y - 128 - self.bg.window_bottom, \
                self.player.x + 128 - self.bg.window_left, \
                self.player.y + 128 - self.bg.window_bottom

    def damage_fear(self):
        main_state.end_timer = get_time()
        main_state.elapsed_timer = main_state.end_timer - main_state.start_timer

    def recovery(self):
        self.end_timer = get_time()
        self.elapsed_timer = self.end_timer - self.start_timer
        if main_state.fear_gauge < 20 and self.elapsed_timer > 1.5:
            main_state.fear_gauge += 1
            self.start_timer = get_time()


    def update(self):
        self.renew_fear_gauge = main_state.fear_gauge * 128 / 20
        if self.renew_fear_gauge == 0:
            self.damage_fear()
            if main_state.elapsed_timer > 5:
                main_state.player_health.damage_fear()

    def draw(self):
        for skeleton in main_state.skeletons:
            if main_state.collision(self, skeleton):
                self.font.draw(self.player.x - 20 - self.bg.window_left,
                           self.player.y - self.bg.window_bottom + random.randint(40, 45), 'Fear', (255, 0, 0))

        if self.renew_fear_gauge == 0:
            self.font.draw(self.player.x - 20 - self.bg.window_left,
                           self.player.y - self.bg.window_bottom + random.randint(40, 43), 'Fear', (160, 0, 255))

        self.image.clip_draw(self.frame, 0, int(self.renew_fear_gauge), 16, self.x - (128 - int(self.renew_fear_gauge))/2, self.y)
        draw_rectangle(*self.get_hitbox())
