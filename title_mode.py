from pico2d import load_image, get_events, clear_canvas, update_canvas, delay
from sdl2 import SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import game_framework
import play_mode


def init():
    global titleimage, titlelaser, titlecookie, titlename
    titleimage = load_image('resource/title.png')
    titlelaser = load_image('resource/title_laser.png')
    titlecookie = load_image('resource/title_cookie.png')
    titlename = load_image('resource/name.png')

    titlecookie.frame = 0
    titlelaser.frame = 0

def finish():
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)

def draw():
    clear_canvas()
    titleimage.draw(400, 300, 900, 700)
    titlelaser.clip_draw(titlelaser.frame * 851, 0, 851, 101, 540, 290, 851 * 0.75, 101)
    titlecookie.clip_draw(titlecookie.frame * 148, 0, 148, 164, 170, 270, 148 * 2.2, 164 * 2.2)
    titlename.draw(500, 150, 506, 111)
    update_canvas()
    delay(0.05)

def update():
    titlelaser.frame = (titlelaser.frame + 1) % 3
    titlecookie.frame = (titlecookie.frame + 1) % 4
