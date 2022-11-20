from cmu_112_graphics import * 
from map import *

class Enemy(Object):
    def __init__(self, image, x0, y0, x1, y1, cat, bgHeight):
        self.image = image
        super().__init__(x0, y0, x1, y1, cat, bgHeight)
    
    def appStarted(self, app):
        # self.objImage = app.loadImage(self.image)
        pass

    @staticmethod
    def enemy1(app):
        pass

    def keyPressed(self, app, event):
        if (self.catTouchingObj and event.key == 'z'):
            if self.image == 'enemy1.png':
                self.redDoorFunc(app)

    def catInRange(self, app):
        # determines if cat is in range to start dialogue/battle
        pass
    
    def redrawAll(self, app, canvas):
        if (self.onScreen):
            # cx = self.x0 + (self.objImage.width/2)
            # cy = self.y0 + (self.objImage.height/2)
            # cx -= self.cat.scrollX
            # cy -= self.cat.scrollY
            
            x0 = self.x0 
            x1 = self.x1
            y0 = self.y0
            y1 = self.y1
            
            x0 -= self.cat.scrollX
            x1 -= self.cat.scrollX
            y0 -= self.cat.scrollY
            y1 -= self.cat.scrollY

            canvas.create_rectangle(x0, y0, x1, y1, fill='red')
            # canvas.create_image(cx, cy,   
            #     image=ImageTk.PhotoImage(self.objImage))
            self.checkCollision()