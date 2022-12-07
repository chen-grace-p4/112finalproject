from cmu_112_graphics import * 

# this file has all moving block attacks enemy inflicts on player
# during battles. Blocks are considered obstacles and player
# needs to move to avoid the blocks or they lose health.
# player can only jump during normalattack3 (which 
# attack happens is chosen at random)
class enemyAttack():
    def __init__(self):
        x0, y0, x1, y1 = 100, 275, 500, 425
        self.x0 = x0
        self.y0 = y0 
        self.x1 = x1
        self.y1 = y1 

        self.timePassed = 0

        self.attackOn = False
        self.blocks = []

# batcat moves normally 
# blocks moving from right to left
class normalAttack1(enemyAttack):
    def __init__(self):
        super().__init__()
        self.blocks = [movingBlock('rightLeft'), movingBlock('rightLeft')]

    def timerFired(self, app):
        if self.attackOn:
            self.timePassed += 1
            for block in self.blocks:
                block.timerFired(app)
            if self.timePassed % 10 == 0:
                self.blocks.append(movingBlock('rightLeft'))
            if self.timePassed >= 400:
                self.attackOn = False
                app.defending = False
                app.bossDefending = False
    
    def redrawAll(self, app, canvas):
        if self.attackOn:
            for block in self.blocks:
                block.redrawAll(app, canvas)

    

# batcat can move normally
# blocks moving from top to down
class normalAttack2(enemyAttack):
    def __init__(self):
        super().__init__()
        self.blocks = [movingBlock('topDown'), movingBlock('topDown')]

    def timerFired(self, app):
        if self.attackOn:
            self.timePassed += 1
            for block in self.blocks:
                block.timerFired(app)
            if self.timePassed % 10 == 0:
                self.blocks.append(movingBlock('topDown'))
            if self.timePassed >= 400:
                self.attackOn = False
                app.defending = False
                app.bossDefending = False
    
    def redrawAll(self, app, canvas):
        if self.attackOn:
            for block in self.blocks:
                block.redrawAll(app, canvas)

# batcat can move left, right, and space to jump
# blocks coming from right to left
# blocks are stuck to the ground
class normalAttack3(enemyAttack):
    def __init__(self):
        super().__init__()
        self.blocks = [movingGravityBlock(), movingGravityBlock()]

    def timerFired(self, app):
        if self.attackOn:
            self.timePassed += 1
            for block in self.blocks:
                block.timerFired(app)
            if self.timePassed % 50 == 0:
                self.blocks.append(movingGravityBlock())
            if self.timePassed >= 400:
                self.attackOn = False
                app.defending = False
                app.bossDefending = False
    
    def redrawAll(self, app, canvas):
        if self.attackOn:
            for block in self.blocks:
                block.redrawAll(app, canvas)
    

# affected by gravity, moves right to left
import random
class movingGravityBlock():
    def __init__(self):
        leftBoundX, upperBoundY, rightBoundX, lowerBoundY = 100, 275, 500, 425
        self.leftBoundX = leftBoundX 
        self.rightBoundX = rightBoundX
        self.upperBoundY = upperBoundY
        self.lowerBoundY = lowerBoundY

        self.cx = self.rightBoundX
        self.height = random.randint(upperBoundY+70, lowerBoundY-10)
        self.cy = lowerBoundY + (self.height/2)

        self.halfSideLen = 10

        self.timePassed = 0

    
    def timerFired(self, app):
        self.timePassed += 1
        self.cx -= 5

        if self.timePassed == 2:
            self.checkCollision(app)
        elif self.timePassed > 2:
            self.timePassed = 0
    
    def checkCollision(self, app):
        x0 = self.cx - self.halfSideLen
        y0 = self.height
        x1 = self.cx + self.halfSideLen
        y1 = self.lowerBoundY

        catX0 = app.batCat.cx - 16
        catY0 = app.batCat.cy - 16
        catX1 = app.batCat.cx + 16
        catY1 = app.batCat.cy + 16
        catX = app.batCat.cx
        catY = app.batCat.cy

        boundY = y0 + ((y1-y0)/2)
        boundX = x0 + ((x1-x0)/2)
       
        if (catX > x0 and catX < x1 and
            catY0 > boundY and catY0 < y1):
            app.catHealth -= 5
    
        elif (catX0 > boundX and catX0 < x1 and
            catY > y0 and catY < y1):
            app.catHealth -= 5
        
        elif (catX1 > x0 and catX1 < boundX and
            catY > y0 and catY < y1):
            app.catHealth -= 5
 
        elif (catX > x0 and catX < x1 and
            catY1 > y0 and catY1 < boundY):
            app.catHealth -= 5
        
        # cat health will not be lower than 1 but you can't progress game
        # without a health 20 or higher
        if app.catHealth < 1:
                app.catHealth = 1

    def redrawAll(self, app, canvas):
        x0 = self.cx - self.halfSideLen
        y0 = self.height
        x1 = self.cx + self.halfSideLen
        y1 = self.lowerBoundY
        if self.cx > self.leftBoundX:
            canvas.create_rectangle(x0, y0, x1, y1, fill='red',
                                    outline='red')

# floats in air
class movingBlock():
    # block can either move from right to left
    # or from top to down
    def __init__(self, moveDir):
        leftBoundX, upperBoundY, rightBoundX, lowerBoundY = 100, 275, 500, 425
        self.leftBoundX = leftBoundX 
        self.rightBoundX = rightBoundX
        self.upperBoundY = upperBoundY
        self.lowerBoundY = lowerBoundY

        self.sideLen = 16 #has to be even number

        self.cx = leftBoundX
        self.cy = upperBoundY
        self.halfSideLen = self.sideLen / 2

        halfSideLen = self.sideLen / 2
        if moveDir == 'topDown':
            self.cx = random.randint(leftBoundX+halfSideLen, 
                                    rightBoundX-halfSideLen)
            self.cy = self.upperBoundY - halfSideLen
        elif moveDir == 'rightLeft':
            self.cx = self.rightBoundX + halfSideLen
            self.cy = random.randint(upperBoundY+halfSideLen, 
                                    lowerBoundY-halfSideLen)
        
        self.moveDir = moveDir

        self.timePassed = 0
    
    def timerFired(self, app):
        self.timePassed += 1
        if self.moveDir == 'topDown':
            self.cy += 5
        elif self.moveDir == 'rightLeft':
            self.cx -= 5 
        
        if self.timePassed == 2:
            self.checkCollision(app)
        elif self.timePassed > 2:
            self.timePassed = 0
    
    def checkCollision(self, app):
        x0 = self.cx - self.halfSideLen
        y0 = self.cy - self.halfSideLen
        x1 = self.cx + self.halfSideLen
        y1 = self.cy + self.halfSideLen

        catX0 = app.batCat.cx - 16
        catY0 = app.batCat.cy - 16
        catX1 = app.batCat.cx + 16
        catY1 = app.batCat.cy + 16
        catX = app.batCat.cx
        catY = app.batCat.cy

        boundY = y0 + ((y1-y0)/2)
        boundX = x0 + ((x1-x0)/2)
       
        if (catX > x0 and catX < x1 and
            catY0 > boundY and catY0 < y1):
            app.catHealth -= 5
    
        elif (catX0 > boundX and catX0 < x1 and
            catY > y0 and catY < y1):
            app.catHealth -= 5
        
        elif (catX1 > x0 and catX1 < boundX and
            catY > y0 and catY < y1):
            app.catHealth -= 5
 
        elif (catX > x0 and catX < x1 and
            catY1 > y0 and catY1 < boundY):
            app.catHealth -= 5
        
        if app.catHealth < 1:
            app.catHealth = 1

    def redrawAll(self, app, canvas):
        x0 = self.cx - self.halfSideLen
        y0 = self.cy - self.halfSideLen
        x1 = self.cx + self.halfSideLen
        y1 = self.cy + self.halfSideLen
        if self.moveDir == 'topDown':
            if self.cy < self.lowerBoundY:
                canvas.create_rectangle(x0, y0, x1, y1, fill='red',
                                        outline='red')
        elif self.moveDir == 'rightLeft':
            if self.cx > self.leftBoundX:
                canvas.create_rectangle(x0, y0, x1, y1, fill='red',
                                        outline='red')