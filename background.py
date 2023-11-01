from pico2d import load_image


class Background:
    def __init__(self):
        self.x = 0
        self.image = load_image('resource/back1.png')

    def draw(self):
        self.image.draw(self.x, 300, 2834, 638)
        self.image.draw(self.x+2834, 300, 2834, 638)

    def update(self):
        self.x -= 1
        if self.x <= -2834:
            self.x = 0
