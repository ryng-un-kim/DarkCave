from pico2d import *


class CombinationTable:
    image = None

    def __init__(self):
        if CombinationTable.image == None:
            CombinationTable.image = load_image('')

    def update(self):
        pass

    def draw(self):
        pass