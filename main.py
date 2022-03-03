import pygame, sys, random
import configparser
from Isaac import Isaac
from Sprite import Sprite
from Projectile import Projectile
from Fly import Fly
from Maw import Maw

# *** Initilization ***
config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
config.read('config.ini')

FPS = int(config.get('settings', 'fps', fallback=60))
WIDTH = int(config.get('settings', 'width', fallback=500))
HEIGHT = int(config.get('settings', 'height', fallback=480))
LEFT_BOUND = float(config['settings']['left_bound_scale']) * WIDTH
RIGHT_BOUND = float(config['settings']['right_bound_scale']) * WIDTH
TOP_BOUND = float(config['settings']['top_bound_scale']) * HEIGHT
BOTTOM_BOUND = float(config['settings']['bottom_bound_scale']) * HEIGHT

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Binding of Isaac')  
clock = pygame.time.Clock()

path = 'sprites'
background = pygame.image.load(f'{path}/Monstro1.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
gameOverWill = pygame.image.load(f'{path}/last_will.png')
gameOverWill = pygame.transform.scale(gameOverWill, (WIDTH * 0.5, HEIGHT * 0.8))
rockImage = pygame.image.load(f'{path}/rock.png')

isGameOver = False
player = Isaac((WIDTH / 2, HEIGHT / 2))
enemies = [Fly((100, 100)), Maw((300, 100))]
rocks = []

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
    drawScore()
    drawRocks()
    for enemy in enemies:
        enemy.track(player)
        enemy.draw(window)
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

def buildRocks(x, y, width, height, length, image):
    image = pygame.transform.scale(image, (width, height))
    for i in range(length):
        px = x + i * width
        py = y
        rock = Sprite((px, py), (width, height), image)
        rocks.append(rock)

def drawRocks():
    for rock in rocks:
        rock.draw(window)

def isNextToRock(obj):
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
    x, y = 355, 170
    if len(enemies) != 0:
        deathObject = player.diedTo.__class__((x, y))
        deathObject.draw(window)
    font = pygame.font.SysFont("arialblack", 16, True, False)
    if len(enemies) == 0:
        currTimeText = font.render(f'Time: {round(currTime / FPS, 3)}', 1, (0))
        window.blit(currTimeText, (10, HEIGHT - 50))
    bestTimeText = font.render(f'Best Time: {bestTime}', 1, (0))
    window.blit(bestTimeText, (10, HEIGHT - 30))
    pygame.display.update()

def checkGameStats():
    global bestTime

    write = False

    time = round(currTime / FPS, 3)
    if time < bestTime and len(enemies) == 0:
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

width, height = 40, 40

# top left corner
x = LEFT_BOUND
y = TOP_BOUND + height / 4
buildRocks(x, y, width, height, 2, rockImage)
buildRocks(x, y + height, width, height, 1, rockImage)

# top right corner
x = RIGHT_BOUND - 2 * width
y = TOP_BOUND + height / 4
buildRocks(x, y, width, height, 2, rockImage)
buildRocks(x + width, y + height, width, height, 1, rockImage)

# bottom left corner
x = LEFT_BOUND
y = BOTTOM_BOUND - height
buildRocks(x, y, width, height, 2, rockImage)
buildRocks(x, y - height, width, height, 1, rockImage)

# bottom right corner
x = RIGHT_BOUND - 2 * width
y = BOTTOM_BOUND - height
buildRocks(x, y, width, height, 2, rockImage)
buildRocks(x + width, y - height, width, height, 1, rockImage)


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
        
        if player.health <= 0 or len(enemies) == 0:
            isGameOver = True
            continue
        
        if isinstance(enemy, Maw):
            if random.random() < 0.005:
                enemy.shoot(player)
    
    for rock in rocks:
        if checkCollision(player, rock):
            player.reset()

    player.move()
    Projectile.moveAll()
    
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