from pico2d import *
import main_state

class PlayerFood:
    image = None

    def __init__(self, x, y):
        self.x = x + 420
        self.y = y
        self.frame = 0
        self.food_gauge = 20
        self.renew_food_gauge = 0
        self.start_timer = get_time()
        if PlayerFood.image == None:
            PlayerFood.image = load_image('resource\Food.png')

    def damage_food(self):
        main_state.end_timer = get_time()
        main_state.elapsed_timer = main_state.end_timer - main_state.start_timer

    def update(self):
        self.renew_food_gauge = self.food_gauge * 128 / 20
        self.end_timer = get_time()
        self.elapsed_timer = self.end_timer - self.start_timer
        if self.elapsed_timer > 12 and self.food_gauge != 0:
            self.food_gauge -= 1
            self.start_timer = get_time()
        if self.renew_food_gauge == 0:
            self.damage_food()
            if main_state.elapsed_timer > 6:
                main_state.player_health.damage_food()

    def draw(self):
        self.image.clip_draw(self.frame, 0, int(self.renew_food_gauge), 16, self.x - (128 - int(self.renew_food_gauge))/2, self.y)