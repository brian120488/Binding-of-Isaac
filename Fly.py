import pygame
from settings import *
from TrackingSprite import TrackingSprite

class Fly(TrackingSprite):
    ANIMATION_DELAY = 3
    SPEED = 1.25
    MAX_HEALTH = 3

    def __init__(self, coords):
        path = 'sprites/fly'
        self.moveLeftList = [pygame.image.load(f'{path}/fly{i}.png') for i in range (1,5)]
        self.moveRightList = [pygame.transform.flip(image, True, False) for image in self.moveLeftList]
        moveLists = (self.moveLeftList, self.moveRightList)
        super().__init__(coords, moveLists)