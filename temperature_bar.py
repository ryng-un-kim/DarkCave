from pico2d import *
import main_state


class PlayerTemperature:
    image = None
    def __init__(self, x, y):
        self.x = x + 280
        self.y = y
        self.frame = 0
        self.renew_temp_gauge = main_state.temp_gauge * 128 / 20
        self.start_timer = get_time()
        if PlayerTemperature.image == None:
            PlayerTemperature.image = load_image('resource\Temperature.png')

    def damage_temp(self):
        main_state.end_timer = get_time()
        main_state.elapsed_timer = main_state.end_timer - main_state.start_timer

    def recovery(self):
        self.end_timer = get_time()
        self.elapsed_timer = self.end_timer - self.start_timer
        if main_state.temp_gauge < 20 and self.elapsed_timer > 2:
            main_state.temp_gauge += 1
            self.start_timer = get_time()

    def update(self):
        self.renew_temp_gauge = main_state.temp_gauge * 128 / 20
        self.end_timer = get_time()
        self.elapsed_timer = self.end_timer - self.start_timer
        if self.elapsed_timer > 4 and main_state.temp_gauge != 0:
            main_state.temp_gauge -= 1
            self.start_timer = get_time()
        if self.renew_temp_gauge == 0:
            self.damage_temp()
            if main_state.elapsed_timer > 6:
                main_state.player_health.damage_temp()

    def draw(self):
        self.image.clip_draw(self.frame, 0, int(self.renew_temp_gauge), 16, self.x - (128 - int(self.renew_temp_gauge))/2, self.y)