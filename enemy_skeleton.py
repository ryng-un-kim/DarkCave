from pico2d import *
import game_framework
import game_world
import main_state
import random
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode


PIXEL_PER_METER = (10.0/0.3)  # 10 pixel 30cm
RUN_SPEED_KMPH = 2.0  # km/hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000/60)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4


class Skeleton:
    image = None

    def __init__(self):
        self.x, self.y = random.randint(300, 1600), random.randint(300, 1600)
        self.frame = 0
        self.timer = 1.0
        self.dir = random.random() * 2 * math.pi  # random moving direction
        self.speed = 0
        self.hp = 0.1 * 100
        self.damage = 0.01 * 100
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

    def set_background(self, bg):
        self.bg = bg


    def build_behavior_tree(self):
        wander_node = LeafNode("Wander", self.wander)
        self.bt = BehaviorTree(wander_node)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_Time)%FRAMES_PER_ACTION
        self.bt.run()
        self.x += self.speed * math.cos(self.dir)*game_framework.frame_Time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_Time
        self.x = clamp(50, self.x, self.bg.w - 50)
        self.y = clamp(50, self.y, self.bg.h - 50)

    def die(self):
        pass

    def get_hitbox(self):
        return self.x - self.bg.window_left - 12, self.y - self.bg.window_bottom - 32, \
               self.x - self.bg.window_left + 12, self.y - self.bg.window_bottom + 32

    def draw(self):
        self.image.clip_draw(int(self.frame) * 96, 768-96, 96, 64, self.x - self.bg.window_left, self.y - self.bg.window_bottom)
        draw_rectangle(*self.get_hitbox())
