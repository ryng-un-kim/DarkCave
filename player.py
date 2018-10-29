from pico2d import *
import settings

import time
import threading
import main
# Player Event
RIGHT_DOWN, LEFT_DOWN, UP_DOWN, DOWN_DOWN, RIGHT_UP, LEFT_UP, UP_UP, DOWN_UP, LMOUSE_DOWN, LMOUSE_UP, RMOUSE_DOWN, RMOUSE_UP = range(12)

key_event_table = {
    (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT): LMOUSE_DOWN,
    (SDL_KEYDOWN, SDLK_s): DOWN_DOWN,
    (SDL_KEYDOWN, SDLK_w): UP_DOWN,
    (SDL_KEYDOWN, SDLK_a): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_d): RIGHT_DOWN
}

class IdleState:
    @staticmethod
    def enter(player, event):
        if event == LEFT_DOWN:
            player.velocityX -= 1
            main.way = True
        elif event == RIGHT_DOWN:
            player.velocityX += 1
            main.way = False
        elif event == UP_DOWN:
            player.velocityY += 1
            if main.way:
                main.way = True
            elif not main.way:
                main.way = False
        elif event == DOWN_DOWN:
            player.velocityY -= 1

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 4
        player.x += player.velocityX
        player.y += player.velocityY
        if main.way:
            player.frame2 = 64
        else:
            player.frame2 = 0

    @staticmethod
    def draw(player):
        player.unit.clip_draw(player.frame * player.SIZE, player.frame2, 64, 64, player.x, player.y)


class MoveState:
    @staticmethod
    def enter(player, event):
        if event == LEFT_DOWN:
            player.velocityX -= 1
            main.way = True
        elif event == RIGHT_DOWN:
            player.velocityX += 1
            main.way = False
        elif event == UP_DOWN:
            player.velocityY += 1
            if main.way:
                main.way = True
            elif not main.way:
                main.way = False
        elif event == DOWN_DOWN:
            player.velocityY -= 1

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 4
        player.x += player.velocityX
        player.y += player.velocityY
        if main.way:
            player.frame2 = 64
        else:
            player.frame2 = 0

    @staticmethod
    def draw(player):
        player.unit.clip_draw(player.frame * player.SIZE, player.frame2, 64, 64, player.x, player.y)


class AttackState:
    @staticmethod
    def enter(player, event):
        pass

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        player.timer -= 1

    @staticmethod
    def draw(player):
        pass

next_state_table = {
    IdleState: {LMOUSE_DOWN: AttackState, RIGHT_DOWN: MoveState, LEFT_DOWN: MoveState, RIGHT_UP: IdleState,
                LEFT_UP: IdleState, UP_DOWN: MoveState, DOWN_DOWN: MoveState, UP_UP: IdleState, DOWN_UP: IdleState},
    MoveState: {RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState, RIGHT_UP: IdleState, LEFT_UP: IdleState,
                UP_DOWN: IdleState, DOWN_DOWN: IdleState, UP_UP: IdleState, DOWN_UP: IdleState}


}

class Player:
    unit = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocityX = 0
        self.velocityY = 0
        self.frame2 = 0
        self.SIZE = 64
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        if Player.unit == None:
            Player.unit = load_image('player_idle2.png')

    def add_event(self, event):
        self.event_que.insert(0, event)

    def idle_update(self):
        self.frame = (self.frame + 1) % 4

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)


"""class Player:
    unit = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame2 = 0
        self.SIZE = 64
        self.frame = 0
        if Player.unit == None:
            Player.unit = load_image('player_idle2.png')

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

    def hit_by(self):
        pass

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
        self.unit.clip_draw(self.frame * self.SIZE, self.frame2, 64, 64, self.unit.x, self.unit.y)"""

"""def handle_events():
    global running
    global way
    global click
    global x, y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            mouse.move(dx=event.x, dy=VIEW_HEIGHT-1-event.y)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                print("click : ", event.x, event.y)
                click = True
        elif event.type == SDL_MOUSEBUTTONUP:
            if event.button == SDL_BUTTON_LEFT:
                print("click : ", event.x, event.y)
                click = False
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
                running = False"""