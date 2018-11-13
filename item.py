from pico2d import*
import game_framework
import random
import main


class Item:
    image = None

    def __init__(self):
        self.size = 40
        self.randx = [n for n in range(500 + self.size, main.VIEW_WIDTH - 64 - self.size, 64)]
        self.randy = [n for n in range(500 + self.size, main.VIEW_HEIGHT - 64 - self.size, 64)]
        self.x = random.choice(self.randx)
        self.y = random.choice(self.randy)
        self.r = 0
        if Item.image == None:
            Item.image = load_image("Item.png")

    def get_hitbox(self):
        return self.x - self.size / 2, self.y - self.size / 2, self.x + self.size / 2, self.y + self.size / 2

    def update(self):
        self.y = self.y + math.sin(self.r)/5
        self.r += game_framework.frame_Time * 10
        # 맵 바뀔 때 아이템 제거

    def hit(self):
        print('hit!')
        game_world.remove_object(self)

    def draw(self):
        self.image.clip_draw(0, 0, 64, 64, self.x, self.y)
        draw_rectangle(*self.get_hitbox())