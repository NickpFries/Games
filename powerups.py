import random
import pygame


# Generic Power Up class
class PowerUps:

    def __init__(self, img, window):
        self.speed = 5
        self.speed_x = 3
        self.life_span = 20 * 60
        self.img = img
        self.x = random.randint(50, window.get_width() - 50 - img.get_width())
        self.y = -100
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self):
        self.y += self.speed
        self.x += self.speed_x


class ExtraLife(PowerUps):

    def __init__(self, img, window):
        super().__init__(img, window)


class HealthBoost(PowerUps):

    def __init__(self, img, window):
        super().__init__(img, window)


class RapidFire(PowerUps):

    def __init__(self, img, window):
        super().__init__(img, window)


class TriShot(PowerUps):

    def __init__(self, img, window):
        super().__init__(img, window)


# Same as collide function in main.py
def collide(obj1, obj2):
    offset_x = int(obj2.x - obj1.x)
    offset_y = int(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None
