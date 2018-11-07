from pico2d import*
import settings
import game_framework

import math
import random

from player import Player


class Map:
    image = None

    def __init__(self):
        self.x = VIEW_WIDTH/2
        self.y = VIEW_HEIGHT/2
        if Map.image == None:
            Map.image = load_image('map.png')

    def update(self):
        pass

    def get_hitbox(self):
        return self.x - VIEW_WIDTH/2 + 32, self.y - VIEW_HEIGHT/2 + 192, self.x + VIEW_WIDTH/2 - 32, self.y + VIEW_HEIGHT/2 - 32

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_hitbox())



class Items:
    image = None

    def __init__(self):
        self.size = 40
        self.randx = [n for n in range(500 + self.size, VIEW_WIDTH - 64 - self.size, 64)]
        self.randy = [n for n in range(500 + self.size, VIEW_HEIGHT - 64 - self.size, 64)]
        self.x = random.choice(self.randx)
        self.y = random.choice(self.randy)
        self.r = 0
        if Items.image == None:
            Items.image = load_image("Item.png")

    def get_hitbox(self):
        return self.x - self.size / 2, self.y - self.size / 2, self.x + self.size / 2, self.y + self.size / 2

    def update(self):
        self.y = self.y + math.sin(self.r)/5
        self.r += game_framework.frame_Time * 10
        # 맵 바뀔 때 아이템 제거

    def hit(self):
        print('hit!')
        settings.remove_object(self)

    def draw(self):
        self.image.clip_draw(0, 0, 64, 64, self.x, self.y)
        draw_rectangle(*self.get_hitbox())

class Bonfire:
    image = None

    def __init__(self):
        self.x = 200
        self.y = 400
        self.frame = 0
        if Bonfire.image == None:
            Bonfire.image = load_image('bonfire.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)


class Mouse:
    image = None

    def __init__(self, x=0, y=0):
        hide_cursor()
        self.x = x
        self.y = y
        if Mouse.image == None:
            Mouse.image = load_image("mouse3.png")

    def move(self, dx=0, dy=0):
        self.x = dx
        self.y = dy

    def update(self):
        self.image.x = self.x
        self.image.y = self.y

    def draw(self):
        self.image.draw(self.image.x, self.image.y)

def collision(a, b):
    left_a, bot_a, right_a, top_a = a.get_hitbox()
    left_b, bot_b, right_b, top_b = b.get_hitbox()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bot_b: return False
    if bot_a > top_b: return False

    return True


def handle_events():
    global way
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            mouse.move(dx=event.x, dy=VIEW_HEIGHT - 1 - event.y)
            if event.x > player.x:
                way = True
            elif event.x < player.x:
                way = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            player.handle_event(event)


name = "MainState"
VIEW_WIDTH = 1024
VIEW_HEIGHT = 768

TILESIZE = 64
way = True
click = False
running = True
player = None
ground = None
mouse = None
weapon = None
items = None
bonfire = None


def enter():
    global player, ground, wall, mouse, weapon, items, bonfire
    player = Player((VIEW_WIDTH / 2), (VIEW_HEIGHT / 2))
    ground = Map()
    mouse = Mouse(100, 100)
    items = [Items() for i in range(10)]
    bonfire = Bonfire()
    settings.add_object(ground, 0)
    settings.add_object(mouse, 6)
    settings.add_objects(items, 5)
    settings.add_object(player, 6)
    # settings.add_object(bonfire, 0)

def exit():
    settings.clear()


def update():
    for game_object in settings.all_objects():
        game_object.update()
    for item in items:
        if collision(player, item):
            items.remove(item)
            settings.remove_object(item)
            print('Hit!')





def draw():
    clear_canvas()
    for game_object in settings.all_objects():
        game_object.draw()
    update_canvas()


def main():
    enter()
    while running:
        handle_events()
        update()
        draw()
    exit()


if __name__ == '__main__':
    main()
