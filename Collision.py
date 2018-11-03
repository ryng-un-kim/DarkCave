from pico2d import *
import settings
import player


class Collision:
    image = None
    def __init__(self, x=0, y=0, rect_x=100, rect_y=100 ,sizeX = 64, sizeY = 64):
        self.x, self.y = x, y
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.rect_x = rect_x
        self.rect_y = rect_y
        self.Hit = False
        self.Rx = self.rect_x + self.sizeX/2  #  right line
        self.Uy = self.rect_y + self.sizeY/2  #  up line
        self.Lx = self.rect_x - self.sizeX/2  #  left line
        self.Dy = self.rect_y - self.sizeY/2  #  down line
        if Collision.image == None:
            Collision.image = load_image('wall.png')

    def update(self):
        if self.x > self.Lx and self.y < self.Uy:
            if self.x < self.Rx and self.y > self.Dy:
                self.Hit = True

    def draw(self):
        if self.Hit:
            self.image.clip_draw(0, 0, self.sizeX*2, self.sizeY, self.rect_x, self.rect_y)
        else:
            self.image.clip_draw(0, 0, self.sizeX, self.sizeY, self.rect_x, self.rect_y)


