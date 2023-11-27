import random

from pico2d import *

import cookie
import game_world
import game_framework
import play_mode

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

class Item:
    image = None
    def __init__(self, x = 400, y = 300, velocity = 1):
        if Item.image == None:
            Item.image = load_image('resource/item.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.x -= RUN_SPEED_PPS * game_framework.frame_time

        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)


    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

    def handle_collision(self, group, other):
        global count
        if group == 'cookie:item':
            game_world.remove_object(self)
            global items
            items = [Item(random.randint(100, 1600 - 100), 200, 0) for _ in range(1)]
            game_world.add_objects(items, 1)
            for item in items:
                game_world.add_collision_pair('cookie:item', None, item)  # 아이템을 등록
            return