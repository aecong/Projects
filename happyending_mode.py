import random

from pico2d import *
import game_framework

import game_world
import play_mode
import title_mode
from background import Background, Happybackground
from cookie import Cookie
from hp import Hp
from popcorn import Popcorn
from sound import Backgroundsound


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

        elif event.type == SDL_KEYDOWN and event.key == SDLK_r:
            Hp.hpCnt = 850
            Cookie.itemCount = 0
            Hp.x = 0
            Cookie.start = True
            Cookie.time = 0.0
            Cookie.jump_sound.play()
            Popcorn.eat = 0
            game_framework.change_mode(title_mode)

        else:
            cookie.handle_event(event)


def init():
    Cookie.start = False

    global running
    global cookie
    global background


    cookie = Cookie()
    game_world.add_object(cookie, 1)

    background = Happybackground()
    game_world.add_object(background, 0)

def finish():
    game_world.collision_pairs = {}
    game_world.clear()


def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():

    pass

def resume():

    pass