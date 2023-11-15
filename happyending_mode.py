import random

from pico2d import *
import game_framework

import game_world
from background import Background, Happybackground
from cookie import Cookie
from sound import Backgroundsound


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            cookie.handle_event(event)


def init():
    Happybackground.ending = True
    global running
    global cookie
    global background
    global obstacle
    global hp, hpicon
    global sound

    sound = Backgroundsound()   # sound 바꾸기

    cookie = Cookie()
    game_world.add_object(cookie, 1)

    background = Happybackground()
    game_world.add_object(background, 0)

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