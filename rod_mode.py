import random

from pico2d import *

import badending_mode
import happyending_mode
import game_framework

import game_world
import play_mode
import shotput_mode
import title_mode
from background import Background, Shotputbackground, Polejumpbackground
from cookie import Cookie
from floor import Floor
from hp import Hp, Hpicon
from item import Item
from obstacle import Obstacle
from popcorn import Popcorn
from sound import Backgroundsound


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_f:
            if Popcorn.eat == 1:
                Popcorn.eat = 2
                Popcorn.throwPower = Popcorn.power

            elif Popcorn.eat == 2:
                Popcorn.eat = 3
                items = [Item(random.randint(100, 1600 - 100), random.randint(200, 600 - 200), 0) for _ in range(10)]
                game_world.add_objects(items, 1)
                for item in items:
                    game_world.add_collision_pair('popcorn:item', None, item)
        else:
            cookie.handle_event(event)


def init():

    global running
    global cookie
    global background
    global hp, hpicon
    global sound


    sound = Backgroundsound()

    cookie = Cookie()
    game_world.add_object(cookie, 1)
    game_world.add_collision_pair('cookie:item', cookie, None)

    hp = Hp()
    game_world.add_object(hp, 1)

    hpicon = Hpicon()
    game_world.add_object(hpicon, 2)

    # obstacle = Obstacle()
    # game_world.add_object(obstacle, 1)
    # game_world.add_collision_pair('cookie:obstacle', None, obstacle)

    background = Polejumpbackground()
    game_world.add_object(background, 0)
    global floor
    floor = Floor()
    game_world.add_object(floor, 1)
    global items
    items = [Item(random.randint(100, 1600 - 100), random.randint(300, 600 - 300), 0) for _ in range(5)]
    game_world.add_objects(items, 1)
    for item in items:
        game_world.add_collision_pair('cookie:item', None, item)

def finish():
    game_world.clear()
    game_world.collision_pairs = {}


def update():
    game_world.update()
    game_world.handle_collisions()
    if cookie.time > 60.0:
        game_framework.change_mode(shotput_mode)
    if Hp.hpCnt <= 0:
        game_framework.change_mode(badending_mode)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():

    pass

def resume():

    pass