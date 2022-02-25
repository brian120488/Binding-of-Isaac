from Sprite import Sprite
from settings import *

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
        
        if SHOW_HITBOXES:
            self.showHitbox(window)
    
    def update(self):
        self.updateAnimation()

    def updateAnimation(self):
        self.moveCount = (self.moveCount + 1) % (len(self.moveLeftList) * self.animDelay)