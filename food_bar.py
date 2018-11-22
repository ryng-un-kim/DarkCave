from pico2d import *


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

    def update(self):
        self.renew_food_gauge = self.food_gauge * 128 / 20
        self.end_timer = get_time()
        self.elapsed_timer = self.end_timer - self.start_timer
        if self.elapsed_timer > 10:
            self.food_gauge -= 1
            self.start_timer = get_time()

    def draw(self):
        self.image.clip_draw(self.frame, 0, int(self.renew_food_gauge), 16, self.x - (128 - int(self.renew_food_gauge))/2, self.y)