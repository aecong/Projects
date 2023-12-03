import random

from pico2d import *

import game_world
import game_framework
from popcorn import Popcorn
from rod import Rod

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

ROD_SPEED_KMPH = 15.0
ROD_SPEED_MPM = ROD_SPEED_KMPH * 1000.0 / 60.0
ROD_SPEED_MPS = ROD_SPEED_MPM / 60.0
ROD_SPEED_PPS = ROD_SPEED_MPS * PIXEL_PER_METER
class Item:
    image = None
    item_eat_sound = None
    def __init__(self, x = 400, y = 300, velocity = 1):
        if Item.image == None:
            Item.image = load_image('resource/item.png')
        self.x, self.y, self.velocity = x, y, velocity
        if not Item.item_eat_sound:
            Item.item_eat_sound = load_wav('resource/bgm_jelly.wav')
            Item.item_eat_sound.set_volume(32)

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        if Popcorn.eat == 0 or Rod.Mode == 0 or Rod.Mode == 2 or Rod.Mode == 3:
            if Rod.Mode == 2 or Rod.Mode == 3:
                self.x -= ROD_SPEED_PPS * game_framework.frame_time
            else:
                self.x -= RUN_SPEED_PPS * game_framework.frame_time

        if self.x < 25:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

    def handle_collision(self, group, other):
        global items
        if group == 'cookie:item':
            game_world.remove_object(self)
            Item.item_eat_sound.play()
            if Rod.Mode == 4:
                items = [Item(random.randint(800, 1600 - 100), 200, 0) for _ in range(1)]
                game_world.add_objects(items, 1)
                for item in items:
                    game_world.add_collision_pair('cookie:item', None, item)
                return
        elif group == 'popcorn:item':
            game_world.remove_object(self)
            Item.item_eat_sound.play()
            return