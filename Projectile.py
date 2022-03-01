import pygame
import configparser
from Sprite import Sprite

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
config.read('config.ini')

WIDTH = int(config.get('settings', 'width', fallback=500))
HEIGHT = int(config.get('settings', 'height', fallback=480))

class Projectile(Sprite):
    projectiles = []
    
    @staticmethod
    def drawAll(window):
        for proj in Projectile.projectiles:
            proj.draw(window)

    @staticmethod
    def moveAll():
        for proj in Projectile.projectiles:
            proj.move()
    
    def __init__(self, coords, size, speed, direction, shotFrom):
        path = 'sprites/tears'
        image = pygame.image.load(f'{path}/tear_{size}.png')
        super().__init__(coords, image.get_size(), image)
        self.speed = speed
        self.direction = direction
        self.shotFrom = shotFrom
 
    def draw(self, window):
        px = self.x - self.width / 2
        window.blit(self.image, (px, self.y))

    def move(self):
        self.x += self.direction[0] * self.speed
        self.y -= self.direction[1] * self.speed

        if self.getRight() < 0 or self.getLeft() > WIDTH:
            Projectile.projectiles.remove(self)
        if self.getBottom() < 0 or self.getTop() > HEIGHT:
            Projectile.projectiles.remove(self)


