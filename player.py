import game_framework
from pico2d import*
import game_world
import random
import main
from effect import Effect
from weapon import Weapon

PIXEL_PER_METER = (10.0/0.3)  # 10 pixel 30cm
RUN_SPEED_KMPH = 15.0  # km/hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000/60)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_ACTION = 2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

# Player Event
RIGHT_DOWN, LEFT_DOWN, UP_DOWN, DOWN_DOWN, RIGHT_UP, LEFT_UP, UP_UP, \
DOWN_UP, LMOUSE_DOWN, LMOUSE_UP, RMOUSE_DOWN, RMOUSE_UP, IdleState = range(13)

key_event_table = {
    (SDL_MOUSEBUTTONDOWN, None, SDL_BUTTON_LEFT): LMOUSE_DOWN,
    (SDL_MOUSEBUTTONUP, None, SDL_BUTTON_LEFT): LMOUSE_UP,
    (SDL_KEYDOWN, SDLK_s, None): DOWN_DOWN,
    (SDL_KEYDOWN, SDLK_w, None): UP_DOWN,
    (SDL_KEYDOWN, SDLK_a, None): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_d, None): RIGHT_DOWN,
    (SDL_KEYUP, SDLK_s, None): DOWN_UP,
    (SDL_KEYUP, SDLK_w, None): UP_UP,
    (SDL_KEYUP, SDLK_a, None): LEFT_UP,
    (SDL_KEYUP, SDLK_d, None): RIGHT_UP
}
weapon = None

class IdleState:
    @staticmethod
    def enter(player, event):

        if event == LEFT_DOWN:
            player.x_velocity -= RUN_SPEED_PPS
        elif event == RIGHT_DOWN:
            player.x_velocity += RUN_SPEED_PPS
        elif event == UP_DOWN:
            player.y_velocity += RUN_SPEED_PPS
        elif event == DOWN_DOWN:
            player.y_velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            player.x_velocity += RUN_SPEED_PPS
        elif event == RIGHT_UP:
            player.x_velocity -= RUN_SPEED_PPS
        elif event == UP_UP:
            player.y_velocity -= RUN_SPEED_PPS
        elif event == DOWN_UP:
            player.y_velocity += RUN_SPEED_PPS


    @staticmethod
    def exit(player, event):
        if event == LMOUSE_DOWN:
            player.throw_weapon()

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_Time) % 4

    @staticmethod
    def draw(player):
        if main.see_right:
            player.unit.clip_draw(int(player.frame) * player.size, 128, 64, 64, player.x, player.y)
        else:
            player.unit.clip_draw(int(player.frame) * player.size, 196, 64, 64, player.x, player.y)


class MoveState:
    @staticmethod
    def enter(player, event):
        if event == LEFT_DOWN:
            player.x_velocity -= RUN_SPEED_PPS
        elif event == RIGHT_DOWN:
            player.x_velocity += RUN_SPEED_PPS
        elif event == UP_DOWN:
            player.y_velocity += RUN_SPEED_PPS
        elif event == DOWN_DOWN:
            player.y_velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            player.x_velocity += RUN_SPEED_PPS
        elif event == RIGHT_UP:
            player.x_velocity -= RUN_SPEED_PPS
        elif event == UP_UP:
            player.y_velocity -= RUN_SPEED_PPS
        elif event == DOWN_UP:
            player.y_velocity += RUN_SPEED_PPS

        player.start_timer = get_time()
    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        if main.mousecursor.x > player.x:
            main.see_right = True
        elif main.mousecursor.x < player.x:
            main.see_right = False
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_Time) % 4
        player.x += player.x_velocity * game_framework.frame_Time
        player.y += player.y_velocity * game_framework.frame_Time
        if player.x_velocity == 0 and player.y_velocity == 0:
            player.end_timer = get_time()
            player.elapsed_timer = player.end_timer - player.start_timer
            if player.elapsed_timer > 0.1:
                player.add_event(IdleState)
        # print(player.start_timer, player.end_timer)

    @staticmethod
    def draw(player):
        if main.see_right:
            player.unit.clip_draw(int(player.frame) * player.size, 0, 64, 64, player.x, player.y)
        else:
            player.unit.clip_draw(int(player.frame) * player.size, 64, 64, 64, player.x, player.y)




class AttackState:
    @staticmethod
    def enter(player, event):

        if event == LMOUSE_DOWN:
            if player.attack_elapsed_timer > 0.3:
                player.effect_act()
                player.throw_weapon()
                player.attack_start_timer = get_time()




    @staticmethod
    def exit(player, event):
        pass
    @staticmethod
    def do(player):

        if main.mousecursor.x > player.x:
            main.see_right = True
        elif main.mousecursor.x < player.x:
            main.see_right = False
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_Time) % 4
        player.x += player.x_velocity * game_framework.frame_Time
        player.y += player.y_velocity * game_framework.frame_Time
        player.attack_end_timer = get_time()
        player.attack_elapsed_timer = player.attack_end_timer - player.attack_start_timer


        # print(player.attack_start_timer, player.attack_end_timer)



    @staticmethod
    def draw(player):
        if main.see_right:
            player.unit.clip_draw(int(player.frame) * player.size, 0, 64, 64, player.x, player.y)
        else:
            player.unit.clip_draw(int(player.frame) * player.size, 64, 64, 64, player.x, player.y)


next_state_table = {
    IdleState: {LMOUSE_DOWN: AttackState, LMOUSE_UP: IdleState, RIGHT_DOWN: MoveState, LEFT_DOWN: MoveState, RIGHT_UP: MoveState,
                LEFT_UP: MoveState, UP_DOWN: MoveState, DOWN_DOWN: MoveState, UP_UP: MoveState, DOWN_UP: MoveState,
                IdleState: IdleState},
    MoveState: {LMOUSE_DOWN: AttackState, LMOUSE_UP: MoveState, RIGHT_DOWN: MoveState, LEFT_DOWN: MoveState, RIGHT_UP: MoveState, LEFT_UP: MoveState,
                IdleState: IdleState, UP_DOWN: MoveState, DOWN_DOWN: MoveState, UP_UP: MoveState, DOWN_UP: MoveState,
                },
    AttackState: {LMOUSE_DOWN: AttackState, LMOUSE_UP: AttackState, RIGHT_DOWN: MoveState, LEFT_DOWN: MoveState, RIGHT_UP: MoveState, LEFT_UP: MoveState,
                  IdleState: IdleState, UP_DOWN: MoveState, DOWN_DOWN: MoveState, UP_UP: MoveState, DOWN_UP: MoveState

    }

}

class Player:
    unit = None
    weapons = []
    def __init__(self, x, y, x_velocity=0, y_velocity= 0):
        self.x = x
        self.y = y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.size = 64
        self.hitbox_size = 30
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.start_timer = 0
        self.end_timer = 0
        self.elapsed_timer = 0
        self.attack_start_timer = 0
        self.attack_end_timer = 0
        self.attack_elapsed_timer = 0
        self.cur_state.enter(self, None)
        if Player.unit == None:
            Player.unit = load_image('resource\player_animation.png')

    def effect_act(self):
        effect = Effect(self.x, self.y, self.x_velocity, self.y_velocity)
        game_world.add_object(effect, 1)

    def get_hitbox(self):
        return (self.x - self.hitbox_size / 2), (self.y - self.hitbox_size / 2), (self.x + self.hitbox_size / 2), (self.y + self.hitbox_size / 2)

    def throw_weapon(self):
        Player.weapons = [Weapon(self.x, self.y, self.x_velocity, self.y_velocity) for i in range(1)]
        # weapon.set_force(random.randint(3, 4), 3)
        game_world.add_objects(Player.weapons, 1)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def stop(self):
        print('Hit!')

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)



    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_hitbox())

    def handle_event(self, event):
        if (event.type, event.key, event.button) in key_event_table:
            key_event = key_event_table[(event.type, event.key, event.button)]
            self.add_event(key_event)







