import pygame, math
from settings import *
from Sprite import Sprite
from Projectile import Projectile

class Isaac(Sprite):
    ANIMATION_DELAY = 5
    SPEED = 2.5
    MAX_HEALTH = 5
    IMMUNITY_FRAMES = 70
    FLICKER_LENGTH = 8

    def __init__(self, coords):
        super().__init__(coords, None)
        self.moveCount = 0
        path = 'sprites/Isaac'
        self.moveRightList = [pygame.image.load(f'{path}/Body/H{i}.png') for i in range(1,10)]
        self.moveLeftList = [pygame.transform.flip(image, True, False) for image in self.moveRightList] 
        self.moveDownList = [pygame.image.load(f'{path}/Body/V{i}.png') for i in range (1,10)]   
        self.moveUpList = [self.moveDownList[0]] + self.moveDownList[::-1]
        self.heads = []
        for i in range(1, 9, 2):
            openedEyesImage = pygame.image.load(f'{path}/Head/H{i}.png')
            closedEyesImage = pygame.image.load(f'{path}/Head/H{i+1}.png')
            T = (openedEyesImage, closedEyesImage)
            self.heads.append(T)
        self.width = self.heads[0][0].get_width()
        self.height = self.moveRightList[0].get_height() + self.heads[0][0].get_height() - 3
        self.directionFacing = (1, 0)
        self.directionMoving = (0, 0)
        self.fireDelay = 30
        self.projectileTimer = 0
        self.shootingDuration = 10   # how long Isaac's eyes are closed
        self.health = self.MAX_HEALTH
        self.isImmune = False
        self.immuneCount = 0
        self.diedTo = None

    def draw(self, window):
        keys = pygame.key.get_pressed()
        frame = self.moveCount // self.ANIMATION_DELAY
        headX, headY = self.x, self.y - self.height / 2
        legsX, legsY = self.x + 5, self.y + 3
        eyes = 1 if self.projectileTimer <= self.shootingDuration else 0
        if self.immuneCount % self.FLICKER_LENGTH >= self.FLICKER_LENGTH / 2: return
        match self.directionMoving:
            case (-1, _): 
                window.blit(self.moveLeftList[frame], (legsX, legsY))
            case (1, _):
                window.blit(self.moveRightList[frame], (legsX, legsY))
            case (_, 1):
                window.blit(self.moveUpList[frame], (legsX, legsY))
            case (_, -1) | (0, 0):
                window.blit(self.moveDownList[frame], (legsX, legsY))
        match self.directionFacing:
            case (-1, _): 
                window.blit(self.heads[3][eyes], (headX, headY))
            case (1, _):
                window.blit(self.heads[1][eyes], (headX, headY))
            case (_, 1):
                window.blit(self.heads[2][eyes], (headX, headY))
            case (_, -1):
                window.blit(self.heads[0][eyes], (headX, headY))

        if SHOW_HITBOXES:
            self.showHitbox(window)
        
    def move(self):
        self.update()

        keys = pygame.key.get_pressed()
        self.moveCount = (self.moveCount + 1) % (len(self.moveLeftList) * Isaac.ANIMATION_DELAY)
        isMovingX, isMovingY = True, True

        # check movement
        if keys[pygame.K_a]:
            self.directionFacing = (-1, 0)
            self.directionMoving = (-1, 0)
        elif keys[pygame.K_d]:
            self.directionFacing = (1, 0)
            self.directionMoving = (1, 0)
        else:
            isMovingX = False
        if keys[pygame.K_w]:
            if not isMovingX:
                self.directionFacing = (0, 1)
                self.directionMoving = (0, 1)
            self.directionMoving = (self.directionMoving[0], 1)
        elif keys[pygame.K_s]:
            if not isMovingX:
                self.directionFacing = (0, -1)
                self.directionMoving = (0, -1)
            self.directionMoving = (self.directionMoving[0], -1)
        else:
            isMovingY = False
            
        # reset animation if not moving
        if not isMovingX and not isMovingY:
            self.moveCount = 0
            self.directionFacing = (0, -1)
            self.directionMoving = (0, 0)

        # change coords based on direction
        if isMovingX and isMovingY:
            SPEED = self.SPEED / math.sqrt(2)
            dx = self.directionMoving[0] * SPEED
            dy = -self.directionMoving[1] * SPEED
            self.moveHelper(dx, dy)
        elif isMovingX:
            dx = self.directionMoving[0] * self.SPEED
            self.moveHelper(dx, 0)
        elif isMovingY:
            dy = -self.directionMoving[1] * self.SPEED
            self.moveHelper(0, dy)

    def moveHelper(self, dx, dy):
        self.x += dx
        self.y += dy

        if self.getLeft() < 0:
            self.setLeft(0)
        elif self.getRight() > WIDTH:
            self.setRight(WIDTH)
        if self.getTop() < 0:
            self.setTop(0)
        elif self.getBottom() > HEIGHT:
            self.setBottom(HEIGHT)
    
    def update(self):
        self.projectileTimer += 1
        if self.isImmune: self.immuneCount += 1
        if self.immuneCount >= self.IMMUNITY_FRAMES: 
            self.isImmune = False
            self.immuneCount = 0
    
    def shoot(self, direction):
        self.directionFacing = direction

        projectiles = Projectile.projectiles
        if self.projectileTimer >= self.fireDelay:
            self.projectileTimer = 0
            px = (self.getLeft() + self.getRight()) / 2
            py = self.getTop() + self.height / 10
            tearSize = 4
            tearSPEED = 3.5
            shotFrom = self.__class__.__name__
            projectile = Projectile((px, py), tearSize, tearSPEED, direction, shotFrom)
            projectiles.append(projectile)

    def hitBy(self, enemy):
        if not self.isImmune:
            self.health -= 1
            self.isImmune = True
        self.diedTo = enemy

    # Returns coordinates of sprite adjusting for offsets
    def getLeft(self):
        return self.x
    def getRight(self):
        return self.x + self.width
    def getTop(self):
        return self.y - self.height / 2
    def getBottom(self):
        return self.y + self.height / 2

    # Moves sprite adjusting for offsets
    def setLeft(self, leftX):
        self.x = leftX
    def setRight(self, rightX):
        self.x = rightX - self.width
    def setTop(self, topY):
        self.y = topY + self.height / 2
    def setBottom(self, bottomY):
        self.y = bottomY - self.height / 2


    
    
