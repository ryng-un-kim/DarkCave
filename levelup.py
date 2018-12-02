from pico2d import *
import main_state

class LevelUp:
    image = None
    def __init__(self, x, y):
        self.x = x
        self.y = y
        if LevelUp.image == None:
            LevelUp.image = load_image('resource\level_up_choice.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)


class StoneDamage:
    image = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.jua_font = load_font('ENCR11B.TTF', 18)

    def update(self):
        pass

    def draw(self):
        self.jua_font.draw(self.x, self.y, 'Stone Damage :%3d' % main_state.player_damage, (255, 255, 255))
