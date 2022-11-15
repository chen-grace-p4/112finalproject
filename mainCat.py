from cmu_112_graphics import * 
class Cat():
    scrollX = 0
    scrollY = 0
    scrollMargin = 200

    def __init__(self, width, height):
        self.image = 'catsprite.png'
        self.cx = width/2
        self.cy = height/2
        self.screenWidth = width 
        self.screenHeight = height

        self.toggleMoveRight = True
        self.toggleMoveLeft = True 
        self.toggleMoveDown = True 
        self.toggleMoveUp = True
    
    def appStarted(self, app):
        app.catImage = app.loadImage(self.image)
        spritestrip = app.loadImage('stillcatspritesheet.png')
        app.stillSprites = []
        for i in range(4):
            sprite = spritestrip.crop((64*i, 0, (64*i)+64, 64))
            app.stillSprites.append(sprite)
    
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
        self.cy += dy
        self.makeCatVisible(app)

    def keyPressed(self, app, event):
        if (self.toggleMoveLeft and event.key == "Left"):
            self.moveCat(app, -10, 0)
            app.catImage = app.stillSprites[1]
        elif (self.toggleMoveRight and event.key == "Right"):
            self.moveCat(app, +10, 0)
            app.catImage = app.stillSprites[0]
        elif (self.toggleMoveUp and event.key == "Up"):
            self.moveCat(app, 0, -10)
            app.catImage = app.stillSprites[3]
        elif (self.toggleMoveDown and event.key == "Down"):
            self.moveCat(app, 0, +10)
            app.catImage = app.stillSprites[2]

    def redrawAll(self, app, canvas):
        x = self.cx
        x -= self.scrollX
        y = self.cy 
        y -= self.scrollY
        canvas.create_image(x, y, 
        image=ImageTk.PhotoImage(app.catImage))
    


