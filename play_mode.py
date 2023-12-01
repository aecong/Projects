import random

from pico2d import *
import game_framework

import game_world
import shotput_mode
import title_mode
from background import Background
from cookie import Cookie
from item import Item
from obstacle import Obstacle


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            if cookie.itemCount >= 30:
                cookie.itemCount -= 30
        else:
            cookie.handle_event(event)


def init():
    global running
    global cookie
    global background
    global obstacle
    global hp

    cookie = Cookie()
    game_world.add_object(cookie, 1)
    game_world.add_collision_pair('cookie:obstacle', cookie, None)
    game_world.add_collision_pair('cookie:item', cookie, None)

    background = Background()
    game_world.add_object(background, 0)

    obstacle = Obstacle()
    game_world.add_object(obstacle, 1)
    game_world.add_collision_pair('cookie:obstacle', None, obstacle)

    global items
    items = [Item(random.randint(100, 1600 - 100), 200, 0) for _ in range(5)]
    game_world.add_objects(items, 1)
    for item in items:
        game_world.add_collision_pair('cookie:item', None, item)  # 아이템을 등록
def finish():
    game_world.clear()


def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():

    pass

def resume():

    pass