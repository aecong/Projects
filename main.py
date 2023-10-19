from pico2d import *

import game_world
from title import Title, Name, TitleCookie, TitleLaser


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_MOUSEMOTION:  # 마우스 이동 이벤트
            x, y = event.x, 600 - event.y  # 좌표 변환
            if x >= 500 and x <= 500 + name.size_x and y >= 150 and y <= 150 + name.size_y:
                name.is_mouse_over = True
            else:
                name.is_mouse_over = False
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:  # 마우스 클릭 이벤트
            if name.is_mouse_over:
                game_world.remove_object(name)
                game_world.remove_object(title)
                game_world.remove_object(titlelaser)
                game_world.remove_object(titlecookie)


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
