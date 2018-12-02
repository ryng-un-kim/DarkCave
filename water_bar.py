from pico2d import *
import main_state

class PlayerWater:
    image = None

    def __init__(self, x, y):
        self.x = x + 560
        self.y = y
        self.frame = 0
        self.renew_water_gauge = 0
        self.start_timer = get_time()
        if PlayerWater.image == None:
            PlayerWater.image = load_image('resource\Water.png')

    def damage_water(self):
        main_state.end_timer = get_time()
        main_state.elapsed_timer = main_state.end_timer - main_state.start_timer

    def update(self):
        self.renew_water_gauge = main_state.water_gauge * 128 / 20
        self.end_timer = get_time()
        self.elapsed_timer = self.end_timer - self.start_timer
        if self.elapsed_timer > 13 and main_state.water_gauge != 0:
            main_state.water_gauge -= 1
            self.start_timer = get_time()
        self.renew_water_gauge = main_state.water_gauge * 128 / 20
        if self.renew_water_gauge == 0:
            self.damage_water()
            if main_state.elapsed_timer > 6:
                main_state.player_health.damage_water()


    def draw(self):
        self.image.clip_draw(self.frame, 0, int(self.renew_water_gauge), 16, self.x - (128 -int(self.renew_water_gauge))/2, self.y)