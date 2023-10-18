from pico2d import *

import game_world
from title import Title, Name, TitleCookie, TitleLaser


# Game object class here


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            name.handle_events((event.type, event))



def reset_world():
    global running
    global title, name, titlecookie, titlelaser

    running = True

    title = Title()
    name = Name()
    titlecookie = TitleCookie()
    titlelaser = TitleLaser()
    game_world.add_object(title, 0)
    game_world.add_object(name, 1)
    game_world.add_object(titlecookie, 1)
    game_world.add_object(titlelaser, 2)

def update_world():
    game_world.update()



def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()


open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)
# finalization code
close_canvas()
