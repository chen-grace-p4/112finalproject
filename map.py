from cmu_112_graphics import * 
from mainCat import *

# manages sidescrolling of background
class Background():
    def __init__ (self, image, width, height, cat):
        self.image = image 
        self.screenWidth = width
        self.screenHeight = height
        self.cat = cat
    
    def appStarted(self, app):
        self.bgImage = app.loadImage(self.image)

    @staticmethod
    def checkBounds(self, app, x0, y0, x1, y1):
        if x1 > self.bgImage.width:
            x1 = self.bgImage.width
            x0 = self.bgImage.width - 600
            if (self.cat.cx < self.bgImage.width - self.cat.scrollMargin):
                self.cat.toggleMoveRight = True
            else:
                self.cat.toggleMoveRight = False
        else:
            self.cat.toggleMoveRight = True

        # a little bit off for some reason
        if x0 < 0:
            x0 = 0
            x1 = 600
            if (self.cat.cx > self.cat.scrollMargin):
                self.cat.toggleMoveLeft = True
            else:
                self.cat.toggleMoveLeft = False 
        else:
            self.cat.toggleMoveLeft = True
    
        if y1 > self.bgImage.height:
            y1 = self.bgImage.height
            y0 = self.bgImage.height - self.screenHeight
            if (self.cat.cy < self.screenHeight - self.cat.scrollMargin):
                self.cat.toggleMoveDown = True
            else:
                self.cat.toggleMoveDown = False
        else:
            self.cat.toggleMoveDown = True

        if y0 < 0:
            y0 = 0
            y1 = self.screenHeight
            if (self.cat.cy > self.cat.scrollMargin + self.cat.scrollY):
                self.cat.toggleMoveUp = True
            else:
                self.cat.toggleMoveUp = False 
        else:
            self.cat.toggleMoveUp = True

    def redrawAll(self, app, canvas):
        x0 = 0
        y0 = self.bgImage.height-self.screenHeight
        x1 = 600
        y1 = self.bgImage.height

        x0 += self.cat.scrollX
        x1 += self.cat.scrollX

        y0 += self.cat.scrollY
        y1 += self.cat.scrollY
        
        self.checkBounds(self, app, x0, y0, x1, y1)

        cropped = self.bgImage.crop((x0, y0, x1, y1))
        canvas.create_image(self.screenWidth/2, self.screenHeight/2, 
        image=ImageTk.PhotoImage(cropped))

# manages collision and interaction with objects
# invisible and attached to a map
class Object():
    def __init__(self, x0, y0, x1, y1, cat, bgHeight):
        self.onScreen = True
        self.catTouchingObj = False

        self.cat = cat 

        self.x0 = x0
        bgY0 = y0 
        self.y0 = bgY0 - (bgHeight - 600)
        self.x1 = x1 
        bgY1 = y1 
        self.y1 = bgY1 - (bgHeight - 600)
    
    # @staticmethod
    def checkCollision(self):
        catX = self.cat.cx 
        catY = self.cat.cy 
        catX0 = self.cat.cx - 32
        catY0 = self.cat.cy - 32
        catX1 = self.cat.cx + 32
        catY1 = self.cat.cy + 32

        boundY = self.y0 + ((self.y1-self.y0)/2)
        boundX = self.x0 + ((self.x1-self.x0)/2)
        # cat touches from bottom edge
        touchedBottomEdge = False
        if (catX > self.x0 and catX < self.x1 and
            catY0 > boundY and catY0 < self.y1):
            # print("touched bottom edge!")
            self.cat.toggleMoveUp = False
            touchedBottomEdge = True 
            self.catTouchingObj = True
        if (touchedBottomEdge):
            if (catY0 > self.y1): 
                self.cat.toggleMoveUp = True
                touchedBottomEdge = False
                self.catTouchingObj = False
        
        # cat touches right edge
        touchedRightEdge = False 
        if (catX0 > boundX and catX0 < self.x1 and
            catY > self.y0 and catY < self.y1):
            # print("touched right edge!")
            self.cat.toggleMoveLeft = False
            touchedRightEdge = True 
            self.catTouchingObj = True
        if (touchedRightEdge):
            if (catX0 > self.x1): 
                self.cat.toggleMoveLeft = True
                touchedRightEdge = False
                self.catTouchingObj = False
        
        # cat touches left edge
        touchedLeftEdge = False 
        if (catX1 > self.x0 and catX1 < boundX and
            catY > self.y0 and catY < self.y1):
            # print("touched left edge!")
            self.cat.toggleMoveRight = False
            touchedLeftEdge = True 
            self.catTouchingObj = True
        if (touchedLeftEdge):
            if (catX1 < self.x0): 
                self.cat.toggleMoveRight = True
                touchedLeftEdge = False
                self.catTouchingObj = False

        # cat touches top edge
        touchedTopEdge = False 
        if (catX > self.x0 and catX < self.x1 and
            catY1 > self.y0 and catY1 < boundY):
            # print("touched top edge!")
            self.cat.toggleMoveDown = False
            touchedTopEdge = True 
            self.catTouchingObj = True
        if (touchedTopEdge):
            if (catY1 < self.y0): 
                self.cat.toggleMoveDown = True
                touchedTopEdge = False
                self.catTouchingObj = False
    
    def redrawAll(self, app, canvas):
        if (self.onScreen):
            x0 = self.x0 
            x1 = self.x1
            y0 = self.y0
            y1 = self.y1
            
            x0 -= self.cat.scrollX
            x1 -= self.cat.scrollX
            y0 -= self.cat.scrollY
            y1 -= self.cat.scrollY
            # print(x0)
            # print(y0)
            # canvas.create_rectangle(x0, y0, x1, y1, fill='red')
            self.checkCollision()

# object that you can interact with and does something
# has image attached to it
class InteractObj(Object):
    def __init__(self, image, x0, y0, x1, y1, cat, bgHeight, func):
        self.image = image
        self.funct = func
        super().__init__(x0, y0, x1, y1, cat, bgHeight)
    
    def appStarted(self, app):
        self.objImage = app.loadImage(self.image)
        # pass

    def keyPressed(self, app, event):
        if (self.catTouchingObj and event.key == 'z'):
            self.funct(app)

    def redrawAll(self, app, canvas):
        if (self.onScreen):
            cx = self.x0 + (self.objImage.width/2)
            cy = self.y0 + (self.objImage.height/2)
            cx -= self.cat.scrollX
            cy -= self.cat.scrollY
            
            # x0 = self.x0 
            # x1 = self.x1
            # y0 = self.y0
            # y1 = self.y1
            
            # x0 -= self.cat.scrollX
            # x1 -= self.cat.scrollX
            # y0 -= self.cat.scrollY
            # y1 -= self.cat.scrollY

            # canvas.create_rectangle(x0, y0, x1, y1, fill='red')
            canvas.create_image(cx, cy,   
                image=ImageTk.PhotoImage(self.objImage))
            self.checkCollision()

