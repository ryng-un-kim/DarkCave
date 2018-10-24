from pico2d import*
import threading


class Map:
    def __init__(self):
        self.image = load_image('map.png')

    def draw(self):
        self.image.draw(VIEW_WIDTH/2, VIEW_HEIGHT/2)


class Wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.SIZE = 64
        self.image = load_image('wall.png')

    def update(self):
        self.image.x = self.x * TILESIZE
        self.image.y = self.y * TILESIZE

    def draw(self):
        self.image.clip_draw(0, 0, 64, 64, self.image.x, self.image.y)


class Weapon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame2 = 0
        self.SIZE = 64
        self.frame = 0
        self.unit = load_image('weapon.png')

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
            self.frame2 = 64
        else:
            self.frame2 = 0

    def draw(self):
        self.unit.clip_draw(self.frame * self.SIZE, self.frame2, 64, 64, self.unit.x, self.unit.y)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame2 = 0
        self.SIZE = 64
        self.frame = 0
        self.unit = load_image('player_idle2.png')
        self.unit2 = load_image('weapon.png')

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

    def wall(self):
        pass

    def idle_update(self):
        self.frame = (self.frame + 1) % 4
        threading.Timer(0.3, self.idle_update).start()

    def update(self):
        self.unit.x = self.x * TILESIZE
        self.unit.y = self.y * TILESIZE
        self.unit2.x = self.x * TILESIZE
        self.unit2.y = self.y * TILESIZE
        if way:
            self.frame2 = 64
        else:
            self.frame2 = 0

    def draw(self):
        self.unit.clip_draw(self.frame * self.SIZE, self.frame2, 64, 64, self.unit.x, self.unit.y)

    def weapon_draw(self):
        self.unit2.clip_draw(0, 0, 64, 64, self.unit2.x + TILESIZE/3, self.unit2.y - TILESIZE/8)


class Mouse:
    def __init__(self, x, y):
        hide_cursor()
        self.x = x
        self.y = y
        self.image = load_image("mouse.png")

    def move(self, dx=0, dy=0):
        self.x = dx
        self.y = dy

    def update(self):
        self.image.x = self.x
        self.image.y = self.y

    def draw(self):
        self.image.draw(self.image.x, self.image.y)


def handle_events():
    global running
    global way
    global x, y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            mouse.move(dx=event.x, dy=VIEW_HEIGHT-1-event.y)
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_a:
                player.move(dx=-1)
                way = True
            elif event.key == SDLK_d:
                player.move(dx=+1)
                way = False
            elif event.key == SDLK_w:
                player.move(dy=+1)
                if way:
                    way = True
                elif not way:
                    way = False
            elif event.key == SDLK_s:
                player.move(dy=-1)
            elif event.key == SDLK_ESCAPE:
                running = False


class Time:
    def __init__(self):
        pass

    def new(self):
        pass

    def update(self):
        pass


VIEW_WIDTH = 1024
VIEW_HEIGHT = 768

FPS = 60
TILESIZE = 64
open_canvas(VIEW_WIDTH, VIEW_HEIGHT)
player = Player((VIEW_WIDTH/2)/TILESIZE, (VIEW_HEIGHT/2)/TILESIZE)
way = True
running = True
dirt = Map()
wall = Wall(100, 100)
player.idle_update()
mouse = Mouse(100, 100)
weapon = Weapon((VIEW_WIDTH/2)/TILESIZE, (VIEW_HEIGHT/2)/TILESIZE)

while running:
    main()
    handle_events()
    player.update()
    mouse.update()
    wall.update()
    clear_canvas()
    dirt.draw()
    mouse.draw()
    player.draw()
    player.weapon_draw()
    wall.draw()
    update_canvas()






close_canvas()