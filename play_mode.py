from pico2d import *

import cookie
import game_framework
import game_world
import title_mode
from cookie import Cookie


# Game object class here


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            cookie.handle_event(event)


def init():
    global running
    global cookie

    running = True

    cookie = Cookie()
    game_world.add_object(cookie, 1)


def finish():
    game_world.clear()
    pass


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