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
class Object():
    def __init__(self):
        pass

# manages collision with walls (inherit from object)
# attack walls to the map
class Wall(Object):
    def appStarted(app):
        pass 
