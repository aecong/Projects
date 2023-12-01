import random

from pico2d import *

import badending_mode
import happyending_mode
import game_framework

import game_world

import title_mode
from background import Shotputbackground
from cookie import Cookie
from hp import Hp, Hpicon
from item import Item
from obstacle import Obstacle
from popcorn import Popcorn
from rod import Rod
from sound import Backgroundsound, Clicksound, ShotputModesound


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_f:
            # global bgm
            Clicksound.bgm.play()

            if Popcorn.eat == 1:
                Popcorn.eat = 2
                Popcorn.throwPower = Popcorn.power
                items = [Item(random.randint(100, 800 - 100), random.randint(200, 600 - 200), 0) for _ in range(10)]
                game_world.add_objects(items, 1)
                for item in items:
                    game_world.add_collision_pair('popcorn:item', None, item)
            elif Popcorn.eat == 2:
                Popcorn.eat = 3

        else:
            cookie.handle_event(event)


def init():
    Rod.Mode = 4

    global running
    global cookie
    global background
    global hp, hpicon
    global sound


    sound = ShotputModesound()
    global bgm
    bgm = Clicksound()

    cookie = Cookie()
    game_world.add_object(cookie, 1)
    game_world.add_collision_pair('cookie:popcorn', cookie, None)
    game_world.add_collision_pair('cookie:obstacle', cookie, None)

    hp = Hp()
    game_world.add_object(hp, 1)

    hpicon = Hpicon()
    game_world.add_object(hpicon, 2)

    obstacle = Obstacle()
    game_world.add_object(obstacle, 1)
    game_world.add_collision_pair('cookie:obstacle', None, obstacle)

    background = Shotputbackground()
    game_world.add_object(background, 0)

    global popcorn
    popcorn = Popcorn()
    game_world.add_object(popcorn, 2)
    game_world.add_collision_pair('cookie:popcorn', None, popcorn)
    game_world.add_collision_pair('popcorn:item', popcorn, None)

    global items
    items = [Item(random.randint(100, 1600 - 100), random.randint(200, 600 - 200), 0) for _ in range(5)]
    game_world.add_objects(items, 1)
    for item in items:
        game_world.add_collision_pair('popcorn:item', None, item)  # 아이템을 등록
def finish():
    game_world.clear()
    game_world.collision_pairs = {}


def update():
    game_world.update()
    game_world.handle_collisions()
    if cookie.time > 60.0:
        game_framework.change_mode(happyending_mode)
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