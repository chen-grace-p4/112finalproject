from cmu_112_graphics import * 

# all attack last for 15 secons 

# batcat moves normally 
# balls moving from right to left
class normalAttack1():
    def __init__(self, battCat):
        x0, y0, x1, y1 = 100, 275, 500, 425
        self.x0 = x0
        self.y0 = y0 
        self.x1 = x1
        self.y1 = y1 

        self.timePassed = 0
        self.battCat = battCat
    pass 

# batcat can move normally
# balls moving from top to down
class normalAttack2():
    def __init__(self, battCat):
        x0, y0, x1, y1 = 100, 275, 500, 425
        self.x0 = x0
        self.y0 = y0 
        self.x1 = x1
        self.y1 = y1 

        self.timePassed = 0
        self.battCat = battCat

# batcat can move left, right, and space to jump
# blocks coming from right to left
# blocks are stuck to the ground
class normalAttack3():
    def __init__(self, battCat):
        x0, y0, x1, y1 = 100, 275, 500, 425
        self.x0 = x0
        self.y0 = y0 
        self.x1 = x1
        self.y1 = y1 

        self.timePassed = 0
        self.battCat = battCat

        battCat.cy = self.lowerBoundY - 16

# affected by gravity, moves right to left
import random
class movingBlock():
    def __init__(self):
        leftBoundX, upperBoundY, rightBoundX, lowerBoundY = 100, 275, 500, 425
        # self.leftBoundX = leftBoundX 
        # self.rightBoundX = rightBoundX
        # self.upperBoundY = upperBoundY
        # self.lowerBoundY = lowerBoundY

        self.cx = random.randint(leftBoundX, rightBoundX)
        self.height = random.randint(upperBoundY+100, lowerBoundY-50)

        self.halfWidth = 50

        self.x0 = self.cx - self.halfWidth
        self.y0 = self.height 
        self.x1 = self.cx + self.halfWidth 

    
    def timerFired(self, app):
        pass 

    def redrawAll(self, app, canvas):
        pass
    pass 

# floats in air
class movingBall():
    # ball can either move from right to left
    # or from top to down
    def __init__(self, moveDir):
        leftBoundX, upperBoundY, rightBoundX, lowerBoundY = 100, 275, 500, 425
        self.leftBoundX = leftBoundX 
        self.rightBoundX = rightBoundX
        self.upperBoundY = upperBoundY
        self.lowerBoundY = lowerBoundY

        self.cx = random.randint(leftBoundX, rightBoundX)
        self.cy = random.randint(upperBoundY, lowerBoundY)
