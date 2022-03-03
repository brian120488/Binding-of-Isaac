import pygame

class Sprite(object):
    def __init__(self, coords, size, image=None):
        self.x, self.y = coords
        try:
            self.width, self.height = size
        except:
            self.width, self.height = 0, 0
        if image != None:
            self.image = image
            self.width = self.image.get_width()
            self.height = self.image.get_height()
        self.visible = True

    def draw(self, window):
        if not self.visible: return
        window.blit(self.image, (self.x, self.y))

    def hit(self):
        pass

    def showHitbox(self, window):
        x, y = self.getLeft(), self.getTop()
        width, height = self.width, self.height
        pygame.draw.rect(window, (255, 0, 0), [x, y, width, height], 2)

    # Returns coordinates of sprite adjusting for offsets
    def getLeft(self):
        return self.x
    def getRight(self):
        return self.x + self.width
    def getTop(self):
        return self.y
    def getBottom(self):
        return self.y + self.height

    # Moves sprite adjusting for offsets
    def setLeft(self, leftX):
        self.x = leftX
    def setRight(self, rightX):
        self.x = rightX - width
    def setTop(self, topY):
        self.y = topY
    def setBottom(self, bottomY):
        self.y = bottomY - height