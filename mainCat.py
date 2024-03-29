from cmu_112_graphics import * 

class Cat():
    scrollX = 0
    scrollY = 0
    scrollMargin = 150

    def __init__(self, width, height, bgImage):
        self.bgImage = bgImage
        self.cx = width/2
        self.cy = height/2
        self.screenWidth = width 
        self.screenHeight = height

        # if cat CAN move that direction
        self.toggleMoveRight = True
        self.toggleMoveLeft = True 
        self.toggleMoveDown = True 
        self.toggleMoveUp = True

        self.timePassed = 0
    
    def appStarted(self, app):
        self.bg = app.loadImage(self.bgImage)
        self.bgX = 300
        self.bgY = self.bg.height - 300
        spritestrip = app.loadImage('images/allcatsprites.png')
        app.stillSprites = []
        for i in range(4):
            sprite = spritestrip.crop((64*i, 0, (64*i)+64, 64))
            app.stillSprites.append(sprite)
        
        app.moveRightSprites = []
        for i in range(2):
            j = i+1
            sprite = spritestrip.crop((0, 64*j, 64, 64*(j+1)))
            app.moveRightSprites.append(sprite)
        
        app.moveLeftSprites = []
        for i in range(2):
            j = i+1
            sprite = spritestrip.crop((64, 64*j, 128, 64*(j+1)))
            app.moveLeftSprites.append(sprite)
        
        app.moveDownSprites = []
        for i in range(2):
            j = i+1
            sprite = spritestrip.crop((128, 64*j, 192, 64*(j+1)))
            app.moveDownSprites.append(sprite)

        app.moveUpSprites = []
        for i in range(2):
            j = i+1
            sprite = spritestrip.crop((192, 64*j, 256, 64*(j+1)))
            app.moveUpSprites.append(sprite)

        app.catImage = app.stillSprites[0]
        
        app.spriteCounter = 0
        app.timerDelay = 0

        # IS cat moving that direction
        app.catIsMovingRight = False
        app.catIsMovingLeft = False
        app.catIsMovingDown = False
        app.catIsMovingUp = False

    
    def makeCatVisible(self, app):
        if (self.cx < (self.scrollX + self.scrollMargin)):
            self.scrollX = self.cx - self.scrollMargin
        elif (self.cx > (self.scrollX + self.screenWidth - self.scrollMargin)):
            self.scrollX = self.cx - self.screenWidth + self.scrollMargin
        
        if (self.cy < (self.scrollY + self.scrollMargin)):
            self.scrollY = self.cy - self.scrollMargin
        elif (self.cy > (self.scrollY + self.screenHeight - self.scrollMargin)):
            self.scrollY = self.cy - self.screenHeight + self.scrollMargin
    
    def moveCat(self, app, dx, dy):
        self.cx += dx 
        self.bgX += dx
        self.cy += dy
        self.bgY += dy
        self.makeCatVisible(app)

    def keyPressed(self, app, event):
        if (self.toggleMoveLeft and event.key == "Left"):
            self.moveCat(app, -15, 0)
            app.catImage = app.stillSprites[1]
            app.catIsMovingLeft = True
        elif (self.toggleMoveRight and event.key == "Right"):
            self.moveCat(app, +15, 0)
            app.catImage = app.stillSprites[0]
            app.catIsMovingRight = True
        elif (self.toggleMoveUp and event.key == "Up"):
            self.moveCat(app, 0, -15)
            app.catImage = app.stillSprites[3]
            app.catIsMovingUp = True
        elif (self.toggleMoveDown and event.key == "Down"):
            self.moveCat(app, 0, +15)
            app.catImage = app.stillSprites[2]
            app.catIsMovingDown = True
    
    def keyReleased(self, app, event):
        if (event.key == "Left" or event.key == "Right"
            or event.key == "Up" or event.key == "Down"):
            app.catIsMovingRight = False
            app.catIsMovingLeft = False
            app.catIsMovingDown = False
            app.catIsMovingUp = False

    def timerFired(self, app):
        self.timePassed += 1
        if self.timePassed == 25:
            if (self.toggleMoveLeft or self.toggleMoveRight or self.toggleMoveUp
                or self.toggleMoveDown):
                app.spriteCounter = (1 + app.spriteCounter) % 2
        elif self.timePassed > 25:
            self.timePassed = 0

    def getCatLocation(self):
        return (self.bgX, self.bgY)

    def redrawAll(self, app, canvas):
        x = self.cx
        x -= self.scrollX
        y = self.cy 
        y -= self.scrollY
        
        if (app.catIsMovingRight):
            sprite = app.moveRightSprites[app.spriteCounter]
            canvas.create_image(x, y, 
            image=ImageTk.PhotoImage(sprite))
        elif (app.catIsMovingLeft):
            sprite = app.moveLeftSprites[app.spriteCounter]
            canvas.create_image(x, y, 
            image=ImageTk.PhotoImage(sprite))
        elif (app.catIsMovingUp):
            sprite = app.moveUpSprites[app.spriteCounter]
            canvas.create_image(x, y, 
            image=ImageTk.PhotoImage(sprite))
        elif (app.catIsMovingDown):
            sprite = app.moveDownSprites[app.spriteCounter]
            canvas.create_image(x, y, 
            image=ImageTk.PhotoImage(sprite))
        else:
            canvas.create_image(x, y, 
            image=ImageTk.PhotoImage(app.catImage))

# INCLUDES PHYSICS PART (cat jumping during enemy attack)
# jumping includes very basic version of gravity and acceleration
class battleCat():
    def __init__(self):
        leftBoundX, upperBoundY, rightBoundX, lowerBoundY = 100, 275, 500, 425
        self.leftBoundX = leftBoundX 
        self.rightBoundX = rightBoundX
        self.upperBoundY = upperBoundY
        self.lowerBoundY = lowerBoundY

        self.cx = 300
        self.cy = 350
        self.image = 'images/battlecat.png'

        self.canMoveVert = True

        self.timePassed = 0

        self.isJumpingUp = False
        self.isFallingDown = False
        self.accelRate = 10

        self.prevKeyPressed = ""
        self.prevKeyReleased = ""
    
    def keyPressed(self, app, event):
        if event.key == "Right":
            if self.cx + 16 < self.rightBoundX:
                self.cx += 10
        elif event.key == "Left":
            if self.cx - 16 > self.leftBoundX:
                self.cx -= 10
        
        if self.canMoveVert:
            if event.key == "Up":
                if self.cy - 16 > self.upperBoundY:
                    self.cy -= 10
            elif event.key == "Down":
                if self.cy + 20 < self.lowerBoundY:
                    self.cy += 10

        # cat can jump if it can't move vertically
        # cat needs to be on ground first to jump (prevent double jumps)
        if not self.canMoveVert and self.cy >= self.lowerBoundY - 20:  
            if event.key == "Up" or event.key == "Space":
                self.isJumpingUp = True
        self.prevKeyPressed = event.key

    def keyReleased(self, app, event):
        self.prevKeyReleased = event.key

    def timerFired(self, app):
        self.timePassed += 1
        if self.isJumpingUp:
            if self.accelRate > 0 and self.cy - 16 > self.upperBoundY: 
                self.cy -= self.accelRate
                self.accelRate -= 0.7
            else:
                self.isJumpingUp = False 
                self.isFallingDown = True
        elif self.isFallingDown:
            if self.cy + 20 < self.lowerBoundY:
                    self.cy += self.accelRate
                    self.accelRate += 0.7
            else:
                self.isFallingDown = False
                self.accelRate = 10

    def appStarted(self, app):
        self.sprite = app.loadImage(self.image)

    def redrawAll(self, app, canvas):
        canvas.create_image(self.cx, self.cy, 
            image=ImageTk.PhotoImage(self.sprite))

