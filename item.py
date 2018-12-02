from pico2d import*
import game_framework
import game_world
import random
import main_state


class Item:
    image = None

    def __init__(self):
        self.size = 30
        self.x = random.randint(100, 1500)
        self.y = random.randint(200, 950)
        self.r = 0
        if Item.image == None:
            Item.image = load_image("resource\Item.png")

    def set_background(self, bg):
        self.bg = bg


    def get_hitbox(self):
        return self.x - self.bg.window_left - self.size / 2, self.y - self.bg.window_bottom  - self.size / 2, \
               self.x - self.bg.window_left + self.size / 2, self.y - self.bg.window_bottom + self.size / 2

    def update(self):
        self.y = self.y + math.sin(self.r)/5
        self.r += game_framework.frame_Time * 10
        # 맵 바뀔 때 아이템 제거

    def hit(self):
        game_world.remove_object(self)

    def draw(self):
        self.image.clip_draw(0, 0, 50, 50, self.x - self.bg.window_left , self.y - self.bg.window_bottom )
        # draw_rectangle(*self.get_hitbox())


class WaterItem:
    image = None

    def __init__(self):
        self.size = 30
        self.x = random.randint(100, 1500)
        self.y = random.randint(200, 950)
        self.r = 0
        if WaterItem.image == None:
            WaterItem.image = load_image("resource\water_item.png")

    def set_background(self, bg):
        self.bg = bg


    def get_hitbox(self):
        return self.x - self.bg.window_left - self.size / 2, self.y - self.bg.window_bottom  - self.size / 2, \
               self.x - self.bg.window_left + self.size / 2, self.y - self.bg.window_bottom + self.size / 2

    def update(self):
        self.y = self.y + math.sin(self.r)/5
        self.r += game_framework.frame_Time * 10


    def hit(self):
        game_world.remove_object(self)

    def draw(self):
        self.image.clip_draw(0, 0, 32, 32, self.x - self.bg.window_left , self.y - self.bg.window_bottom )
        # draw_rectangle(*self.get_hitbox())