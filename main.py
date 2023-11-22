from pico2d import open_canvas, close_canvas
import badending_mode as start_mode
# import title_mode as start_mode
import game_framework

open_canvas()
game_framework.run(start_mode)
close_canvas()
