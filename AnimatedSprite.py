from Sprite import Sprite
import configparser

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
config.read('config.ini')
SHOW_HITBOXES = config['settings']['show_hitboxes'] == 'True'

class AnimatedSprite(Sprite):
    def __init__(self, coords, moveLists, animDelay):
        self.leftMoveList, self.rightMoveList = moveLists
        self.width = self.leftMoveList[0].get_width()
        self.height = self.leftMoveList[0].get_height()
        super().__init__(coords, (self.width, self.height), None)
        self.animDelay = animDelay
        self.moveCount = 0
    
    def draw(self, window):
        frame = self.moveCount // self.animDelay
        window.blit(self.moveLeftList[frame], (self.x, self.y))
    
    def update(self):
        self.updateAnimation()

    def updateAnimation(self):
        self.moveCount = (self.moveCount + 1) % (len(self.moveLeftList) * self.animDelay)