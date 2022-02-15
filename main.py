"""
Name: Brian Yang
Title: Pygame
Version: 12/1/2021
"""

import pygame, sys, random
from global_vars import *
from Projectile import Projectile
from Isaac import Isaac
from Fly import Fly
from Maw import Maw

# *** Initilization ***
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Binding of Isaac')  
clock = pygame.time.Clock()

path = 'sprites'
background = pygame.image.load(f'{path}/background.png').convert()

player = Isaac((50, 400))
enemies = [Fly((100, 100)), Maw((300, 100))]

# *** Global Functions ***
def drawScore():
    font = pygame.font.SysFont("comicsans", 30, True, False)
    scoreText = font.render(f'Health: {player.health}', 1, (255, 255, 0))
    window.blit(scoreText, (10, 40))

def drawWindow():
    window.fill("white")
    window.blit(background, (0, 0))
    for enemy in enemies:
        enemy.track(player)
        enemy.draw(window)
    drawScore()
    Projectile.drawAll(window)
    player.draw(window)
    pygame.display.update()

def checkCollision(obj1, obj2):
    noXOverlap = obj1.getRight() <= obj2.getLeft() or obj1.getLeft() >= obj2.getRight()
    noYOverlap = obj1.getTop() >= obj2.getBottom()  or obj1.getBottom() <= obj2.getTop()
    return not(noXOverlap or noYOverlap)

def checkCollisionList(obj1, L):
    collisionList = []
    for obj in L:
        if checkCollision(obj1, obj):
            collisionList.append(obj)
    return collisionList

def buildPlatforms(startX, startY, pWidth, pHeight, pLength, image):
    image = pygame.transform.scale(image, (pWidth, pHeight))
    for i in range(pLength):
        px = startX + i * pWidth
        py = startY
        platform = Sprite((px, py), (pWidth, pHeight), image)
        platforms.append(platform)

def drawPlatforms():
    for platform in platforms:
        platform.draw(window)

def isOnPlatform(obj):
    bottom = obj.getBottom()
    obj.setBottom(bottom + 5)
    collisions = checkCollisionList(obj, platforms)
    obj.setBottom(bottom)
    if len(collisions) > 0:
        return True
    return False

# *** Pygame Loop ***
while True: 
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    projectiles = Projectile.projectiles
    for enemy in enemies:
        for proj in projectiles:
            if proj.shotFrom == 'Isaac' and checkCollision(proj, enemy):
                projectiles.remove(proj)
                enemy.health -= 1;
                if enemy.health <= 0:
                    enemies.remove(enemy)
            elif proj.shotFrom != 'Isaac' and checkCollision(proj, player) and not player.isImmune:
                projectiles.remove(proj)
                player.hit()

        if checkCollision(player, enemy):
            player.hit()
        
        if player.health <= 0:
            pygame.quit()
            sys.exit()
        
        if isinstance(enemy, Maw):
            if random.random() < 0.005:
                enemy.shoot(player)


    player.move()
    Projectile.moveAll()

    # collisions = checkCollisionList(player, platforms)
    # if len(collisions) > 0:
    #     player.setLeft(collisions[0].getRight)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.shoot((-1, 0))
    elif keys[pygame.K_RIGHT]:
        player.shoot((1, 0))
    elif keys[pygame.K_UP]:
        player.shoot((0, 1))
    elif keys[pygame.K_DOWN]:
        player.shoot((0, -1))

    drawWindow()