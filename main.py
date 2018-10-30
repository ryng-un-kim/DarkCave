from pico2d import*
import settings
import game_framework

import math
import random

from player import Player


class Map:
    image = None

    def __init__(self):
        if Map.image == None:
            Map.image = load_image('map.png')

    def update(self):
        pass


    def draw(self):
        self.image.draw(VIEW_WIDTH/2, VIEW_HEIGHT/2)


class Items:
    image = None

    def __init__(self):
        self.randx = [n for n in range(64, 700, 64)]
        self.randy = [n for n in range(64, 700, 64)]
        self.x = random.choice(self.randx)
        self.y = random.choice(self.randy)
        self.r = 0

        if Items.image == None:
            Items.image = load_image("Item.png")

    def update(self):
        self.y = self.y + math.sin(self.r)/5
        self.r += game_framework.frame_Time * 10
        # 맵 바뀔 때 아이템 제거

    def draw(self):
        self.image.clip_draw(0, 0, 64, 64, self.x, self.y)


class Weapon:
    unit = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame2 = 0
        self.SIZE = 64
        self.frame = 0
        if Weapon.unit == None:
            Weapon.unit = load_image('weapon.png')

    def move(self, dx=0, dy=0):
        self.x += player.move(dx)
        self.y += player.move(dy)

    def idle_update(self):
        self.frame = (self.frame + 1) % 4
        threading.Timer(0.3, self.idle_update).start()

    def update(self):
        self.unit.x = self.x * TILESIZE
        self.unit.y = self.y * TILESIZE
        if way:
            self.frame2 = 0
        else:
            self.frame2 = 0

    def draw(self):
        self.unit.clip_draw(self.frame * self.SIZE, self.frame2, 64, 64, self.unit.x, self.unit.y)


class Effect:
    image = None

    def __init__(self, x = 0, y = 0):
        self.x, self.y = x, y
        self.frame2 = 120
        self.frame = 0
        self.SIZE = 96
        self.timer = 5
        if Effect.image == None:
            self.image = load_image('Attack.png')

    def update(self):
        for i in range(0, 100):
            self.frame = (self.frame + 1) % 5
            i += 1
        self.timer -= 1
        if self.timer == 0:
            pass


    def draw(self):
        if click:
            self.image.clip_draw(self.frame * self.SIZE, self.frame2, 96, 120, player.unit.x - TILESIZE, player.unit.y)


class Mouse:
    image = None

    def __init__(self, x, y):
        hide_cursor()
        self.x = x
        self.y = y
        if Mouse.image == None:
            Mouse.image = load_image("mouse.png")

    def move(self, dx=0, dy=0):
        self.x = dx
        self.y = dy

    def update(self):
        self.image.x = self.x
        self.image.y = self.y

    def draw(self):
        self.image.draw(self.image.x, self.image.y)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            mouse.move(dx=event.x, dy=VIEW_HEIGHT - 1 - event.y)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                print("click : ", event.x, event.y)
                click = True
        elif event.type == SDL_MOUSEBUTTONUP:
            if event.button == SDL_BUTTON_LEFT:
                print("click : ", event.x, event.y)
                click = False
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
dirt = None
mouse = None
weapon = None
item = None
def enter():
    global player, dirt, wall, mouse, weapon, item
    player = Player((VIEW_WIDTH / 2) / TILESIZE, (VIEW_HEIGHT / 2) / TILESIZE)
    dirt = Map()
    # player.idle_update()
    mouse = Mouse(100, 100)
    weapon = Weapon((VIEW_WIDTH / 2) / TILESIZE, (VIEW_HEIGHT / 2) / TILESIZE)
    item = Items()
    settings.add_object(dirt, 0)
    settings.add_object(weapon, 1)
    settings.add_object(mouse, 4)
    settings.add_object(item, 2)
    settings.add_object(player, 3)

def exit():
    settings.clear()


def update():
    for game_object in settings.all_objects():
        game_object.update()


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
