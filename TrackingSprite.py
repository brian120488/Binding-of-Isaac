import pygame, math
import configparser
from Sprite import Sprite
from AnimatedSprite import AnimatedSprite

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
config.read('config.ini')
PATH = config.get('paths', 'sprites', fallback='sprites')
SHOW_HITBOXES = config['settings']['show_hitboxes'] == 'True'

class TrackingSprite(AnimatedSprite):
    ANIMATION_DELAY = 1
    SPEED = 1
    MAX_HEALTH = 1

    def __init__(self, coords, moveLists):
        super().__init__(coords, moveLists, self.__class__.ANIMATION_DELAY)
        self.health = self.MAX_HEALTH
        self.xDirection = 1

    def draw(self, window):
        self.update()
        frame = self.moveCount // self.ANIMATION_DELAY

        if self.xDirection == -1:
            window.blit(self.moveLeftList[frame], (self.x, self.y))
        else:
            window.blit(self.moveRightList[frame], (self.x, self.y))
        
        if SHOW_HITBOXES: self.showHitbox(window)

    def track(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        ang = abs(math.atan(dy/dx))

        self.x += self.SPEED * abs(math.cos(ang)) * (dx/abs(dx))
        self.y += self.SPEED * abs(math.sin(ang)) * (dy/abs(dy))
        self.xDirection = 1 if dx > 0 else -1

    def drop(self, hearts):
        global rockImage
        if 'heartDropImage' not in globals():
            heartDropImage = pygame.image.load(f'{PATH}/heart_drop.png') 
        heart = Sprite((self.x, self.y), heartDropImage.get_size(), heartDropImage)
        hearts.append(heart)
        
