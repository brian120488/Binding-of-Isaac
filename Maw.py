import pygame, math
from settings import *
from TrackingSprite import TrackingSprite
from Projectile import Projectile

class Maw(TrackingSprite):
    ANIMATION_DELAY = 3
    SPEED = 0.5
    MAX_HEALTH = 5

    def __init__(self, coords):
        path = 'sprites/maw'
        self.moveLeftList = [pygame.image.load(f'{path}/maw.png')]
        self.moveRightList = self.moveLeftList
        moveLists = (self.moveLeftList, self.moveRightList)
        super().__init__(coords, moveLists)

    def shoot(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        ang = abs(math.atan(dy/dx))

        xScale = abs(math.cos(ang)) * (dx/abs(dx))
        yScale = -abs(math.sin(ang)) * (dy/abs(dy))
        px = self.getLeft() + self.width / 2
        py = self.getTop() + self.height / 2
        tearSize = 2
        tearSPEED = 1.5
        shotFrom = self.__class__.__name__
        projectile = Projectile((px, py), tearSize, tearSPEED, (xScale, yScale), shotFrom)
        Projectile.projectiles.append(projectile)