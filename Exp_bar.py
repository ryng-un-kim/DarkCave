from pico2d import *
import game_framework
import main_state
import level_up_state

class Exp:
    image = None
    def __init__(self, x, y):
        self.x , self.y = x + 700, y
        self.renew_exp_gauge = main_state.exp_gauge * 128 / 20
        if Exp.image == None:
            Exp.image = load_image('resource\exp.png')

    def level_up(self):
        game_framework.push_state(level_up_state)

    def update(self):
        self.renew_exp_gauge = main_state.exp_gauge * 128 / main_state.player_max_exp
        if main_state.exp_gauge >= main_state.player_max_exp:
            main_state.exp_gauge = 0
            main_state.player_max_exp += 6
            self.level_up()

    def draw(self):
        self.image.clip_draw(0, 0, int(self.renew_exp_gauge), 16,
                             self.x - (128 - int(self.renew_exp_gauge)) / 2, self.y)


class HealthUP:
    image = None
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        if HealthUP.image == None:
            HealthUP.image = load_image('resource\level_up_health_damage.png')

    def get_hitbox(self):
        return self.x - 30, self.y - 30, \
               self.x + 30, self.y + 30

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.frame, 64, 64, 64, self.x, self.y)


class DamageUP:
    image = None

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        if DamageUP.image == None:
            DamageUP.image = load_image('resource\level_up_health_damage.png')

    def get_hitbox(self):
        return self.x - 30, self.y - 30, \
               self.x + 30, self.y + 30

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.frame, 0, 64, 64, self.x, self.y)
