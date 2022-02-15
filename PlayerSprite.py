import pygame
from global_vars import *
from AnimatedSprite import AnimatedSprite

class PlayerSprite(AnimatedSprite):
    JUMP_HEIGHT = 10

    def __init__(self, coords, size, moveLists, velocity, offsets=None):
        super().__init__(coords, size, moveLists, velocity, offsets)

        self.direction = 1
        self.isJumping = False
        self.dy = 0      
        self.isHit = False

    def draw(self, window):
        frame = self.moveCount // AnimatedSprite.ANIMATION_DELAY
        if self.direction == -1: 
            window.blit(self.moveLeftList[frame], (self.x, self.y))
        elif self.direction == 1:
            window.blit(self.moveRightList[frame], (self.x, self.y))
        if SHOW_HITBOXES:
            self.hitbox(window)
        
    def move(self):
        keys = pygame.key.get_pressed()
        self.moveCount = (self.moveCount + 1) % (len(self.moveLeftList) * PlayerSprite.ANIMATION_DELAY)
        if keys[pygame.K_UP]:
            self.y -= self.velocity
            if self.y < 0:
                self.y = 0
        elif keys[pygame.K_DOWN]:
            self.y += self.velocity
            if self.y + self.height > HEIGHT:
                self.y = HEIGHT - self.height
        if keys[pygame.K_LEFT]:
            self.direction = -1
            self.x -= self.velocity
            if self.x < 0:
                self.x = 0
        elif keys[pygame.K_RIGHT]:
            self.direction = 1
            self.x += self.velocity
            if self.x + self.width > WIDTH:
                self.x = WIDTH - self.width
        else:
            self.moveCount = 0


    
    
