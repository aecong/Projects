import random

from pico2d import load_image

import game_world


class Obstacle:
    def __init__(self):
        self.x = random.randint(400, 800)
        self.image = load_image('resource/obstacle.png')

    def draw(self):
        self.image.draw(self.x, 200, 155, 216)

    def update(self):
        self.x -= 1
        if self.x < 0:
            self.x = random.randint(400, 800)

