from pico2d import *
import game_framework
import game_world
import main_state
import random
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import player
import pickle

PIXEL_PER_METER = (10.0/0.3)  # 10 pixel 30cm

RUN_SPEED_KMPH = 10.0 # km/hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000/60)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 1.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4


class Skeleton:
    image = None
    def __init__(self, speed, hp , damage):
        self.x, self.y = random.randint(300, 1600), random.randint(300, 1600)
        self.frame = 0
        self.act_frame = 768 - 96
        self.font_frame = 40
        self.timer = 1.0
        self.collision_start_timer = get_time()
        self.collision_end_timer = 0
        self.dir = random.random() * 2 * math.pi  # random moving direction
        self.speed = 0
        self.renew_speed = speed
        self.print_font = 0
        self.font = load_font('ENCR10B.TTF', 18)
        self.hp = hp
        self.damage = damage
        self.build_behavior_tree()
        if Skeleton.image == None:
            Skeleton.image = load_image("resource\Monsters_skele.png")  # 611X564

    def wander(self):
        self.speed = RUN_SPEED_PPS
        self.timer -= game_framework.frame_Time
        if self.timer < 0:
            self.timer += 1.0
            self.dir = random.random() * 2 * math.pi
        return BehaviorTree.SUCCESS

    def find_player(self):
        player = main_state.get_player()
        distance = (player.x - self.x) ** 2 + (player.y - self.y) ** 2
        if distance < (PIXEL_PER_METER * 10) ** 2:
            self.dir = math.atan2(player.y - self.y, player.x - self.x)
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.FAIL

    def move_to_player(self):
        self.speed = RUN_SPEED_PPS
        return BehaviorTree.SUCCESS

    def set_background(self, bg):
        self.bg = bg


    def build_behavior_tree(self):
        wander_node = LeafNode("Wander", self.wander)
        find_player_node = LeafNode("Find Player", self.find_player)
        move_to_player_node = LeafNode("Move to Player", self.move_to_player)
        chase_node = SequenceNode("Chase")
        chase_node.add_children(find_player_node, move_to_player_node)
        wander_chase_node = SelectorNode("WanderChase")
        wander_chase_node.add_children(chase_node, wander_node)
        self.bt = BehaviorTree(wander_chase_node)

    def update(self):
        self.act_frame = 768 - 96
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_Time)%FRAMES_PER_ACTION
        self.bt.run()
        self.x += self.speed * math.cos(self.dir)*game_framework.frame_Time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_Time
        self.x = clamp(50, self.x, self.bg.w - 50)
        self.y = clamp(200, self.y, self.bg.h - 50)
        if self.print_font == 1:
            self.font_frame = (self.font_frame + 100 * game_framework.frame_Time)
            if self.font_frame > 60:
                self.print_font = 0
                self.font_frame = 40


    def hit(self):
        if self.print_font == 0:
            self.print_font = 1


    def get_hitbox(self):
        return self.x - self.bg.window_left - 12, self.y - self.bg.window_bottom - 32, \
               self.x - self.bg.window_left + 12, self.y - self.bg.window_bottom + 32

    def attack(self):
        self.act_frame = 768 - 96 - 96 -96
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_Time) % FRAMES_PER_ACTION


    def draw(self):
        if self.print_font == 1:
            self.font.draw(self.x - 20 - self.bg.window_left, self.y - self.bg.window_bottom + self.font_frame, 'Hit!', (100, 200, 100))
        self.image.clip_draw(int(self.frame) * 96, self.act_frame, 96, 64, self.x - self.bg.window_left, self.y - self.bg.window_bottom)
        # draw_rectangle(*self.get_hitbox())



skeleton_data_list = [
    {'speed': 1.0, 'hp': 0.1*100, 'damage': 0.1*100},
    {'speed': 1.0, 'hp': 0.1* 100,'damage':0.01*100},
    {'speed': 2.0, 'hp': 0.13* 100,'damage':0.013*100},
    {'speed': 2.0, 'hp': 0.15* 100,'damage':0.015*100},
    {'speed': 2.0, 'hp': 0.15* 100,'damage':0.015*100},
    {'speed': 2.0, 'hp': 0.2*100, 'damage': 0.2*100},
    {'speed': 2.0, 'hp': 0.25*100, 'damage': 0.2*100},
    {'speed': 2.0, 'hp': 0.25*100, 'damage': 0.2*100},
    {'speed': 2.0, 'hp': 0.3*100, 'damage': 0.2*100},
    {'speed': 2.0, 'hp': 0.3*100, 'damage': 0.2*100},
    {'speed': 2.0, 'hp': 0.35*100, 'damage': 0.2*100},
    {'speed': 2.0, 'hp': 0.35* 100,'damage':0.025*100},
    {'speed': 3.0, 'hp': 0.4* 100,'damage':0.03*100},
    {'speed': 3.0, 'hp': 0.4* 100,'damage':0.03*100},
    {'speed': 3.0, 'hp': 0.5* 100,'damage':0.03*100},
    {'speed': 3.0, 'hp': 0.5*100, 'damage': 0.35*100},
    {'speed': 3.0, 'hp': 0.5* 100,'damage':0.04*100},
    {'speed': 3.0, 'hp': 0.55* 100,'damage':0.045*100},
    {'speed': 3.0, 'hp': 0.55* 100,'damage':0.05*100},
    {'speed': 3.0, 'hp': 0.55* 100,'damage':0.055*100},
    {'speed': 4.0, 'hp': 0.6* 100,'damage':0.06*100},
    {'speed': 4.0, 'hp': 0.65* 100,'damage':0.065*100},
    {'speed': 4.0, 'hp': 1.0 * 100,'damage':0.09*100}
]

with open('skeleton_data_list.pickle', 'wb') as f:
    pickle.dump(skeleton_data_list, f)



