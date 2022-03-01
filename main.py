import pygame, sys, random
import configparser
from Isaac import Isaac
from Projectile import Projectile
from Fly import Fly
from Maw import Maw

# *** Initilization ***
config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
config.read('config.ini')

FPS = int(config.get('settings', 'fps', fallback=60))
WIDTH = int(config.get('settings', 'width', fallback=500))
HEIGHT = int(config.get('settings', 'height', fallback=480))

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Binding of Isaac')  
clock = pygame.time.Clock()

path = 'sprites'
background = pygame.image.load(f'{path}/Monstro1.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
gameOverWill = pygame.image.load(f'{path}/last_will.png')
gameOverWill = pygame.transform.scale(gameOverWill, (WIDTH * 0.8, HEIGHT * 0.8))

isGameOver = False
player = Isaac((WIDTH / 2, HEIGHT / 2))
enemies = [Fly((100, 100)), Maw((300, 100))]

bestTime = float(config['game']['best_time'])
currTime = 0

# *** Global Functions ***
def drawScore():
    font = pygame.font.SysFont("comicsans", 16, True, False)
    scoreText = font.render(f'Health: {player.health}', 1, (0))
    window.blit(scoreText, (10, 10))

def drawWindow():
    window.fill((116,63,51))
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

def drawGameOver():
    midX = (WIDTH - gameOverWill.get_width()) / 2
    midY = (HEIGHT - gameOverWill.get_height()) / 2
    window.fill("white")
    window.blit(gameOverWill, (midX, midY))
    x, y = 300, 210
    deathObject = player.diedTo.__class__((x, y))
    deathObject.draw(window)
    font = pygame.font.SysFont("arialblack", 16, True, False)
    currTimeText = font.render(f'Time: {round(currTime / FPS, 3)}', 1, (0))
    bestTimeText = font.render(f'Best Time: {bestTime}', 1, (0))
    window.blit(currTimeText, (100, 290))
    window.blit(bestTimeText, (100, 310))
    pygame.display.update()

def checkGameStats():
    global bestTime

    write = False

    time = round(currTime / FPS, 3)
    if time < bestTime:
        config.set('game', 'best_time', str(time))
        write = True
        
    if write:
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

def loadImageList(files):
    L = []
    for f in files:
        L.append(pygame.image.load(f))
    return L

# *** Pygame Loop ***
while True: 
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    if isGameOver:
        drawGameOver()
        checkGameStats()
        continue
    else:
        currTime += 1

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
                player.hitBy(proj)

        if checkCollision(player, enemy):
            player.hitBy(enemy)
        
        if player.health <= 0:
            isGameOver = True
            continue
        
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