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
from floor import Floor, nextFloor, Floorelseleft, nextFloorelse
from hp import Hp, Hpicon
from item import Item
from obstacle import Obstacle
from popcorn import Popcorn
from rod import Rod
from sound import Backgroundsound


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_v:
            if Popcorn.eat == 0:
                Popcorn.eat = 1
            elif Popcorn.eat == 1:
                Rod.size = Rod.frame
                Popcorn.eat = 2
            if Rod.Mode == 0:
                Rod.Mode = 1
            elif Rod.Mode == 1:
                Rod.size = Rod.frame
                Rod.Mode = 2
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
    game_world.add_collision_pair('cookie:floor', cookie, None)
    game_world.add_collision_pair('cookie:nothole', cookie, None)

    hp = Hp()
    game_world.add_object(hp, 1)

    hpicon = Hpicon()
    game_world.add_object(hpicon, 2)
    global rod
    rod = Rod()
    game_world.add_object(rod, 2)

    background = Polejumpbackground()
    game_world.add_object(background, 0)

    global floor
    floor = Floor()
    game_world.add_object(floor, 1)
    game_world.add_collision_pair('cookie:floor', None, floor)
    floor = nextFloor()
    game_world.add_object(floor, 1)
    game_world.add_collision_pair('cookie:floor', None, floor)

    global floorelselr
    floorelselr = Floorelseleft()
    game_world.add_object(floorelselr, 1)
    game_world.add_collision_pair('cookie:nothole', None, floorelselr)
    floorelselr = nextFloorelse()
    game_world.add_object(floorelselr, 1)
    game_world.add_collision_pair('cookie:nothole', None, floorelselr)


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
    if cookie.time > 40.0:
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