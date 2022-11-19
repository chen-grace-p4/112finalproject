from cmu_112_graphics import *
class Button():
    def __init__(self, image, x, y, type):
        self.cx = x
        self.cy = y
        self.image = image 
        self.type = type
        self.buttonImage = image
    
    def appStarted(self, app):
        self.buttonImage = app.loadImage(self.image)

    @staticmethod
    def startButtonFunc(app):
        app.mode = 'gameMode'
    @staticmethod
    def howToButtonFunc(app):
        app.mode = 'howToMode'

    def mousePressed(self, app, event):
        x0 = self.cx - (self.buttonImage.width/2)
        y0 = self.cy - (self.buttonImage.height/2)
        x1 = self.cx + (self.buttonImage.width/2)
        y1 = self.cy + (self.buttonImage.height/2)
        if (event.x > x0 and event.x < x1 and 
            event.y > y0 and event.y < y1):
            if self.type == 'startButton':
                self.startButtonFunc(app)
            elif self.type == 'howToButton':
                self.howToButtonFunc(app)
        
    def redrawAll(self, app, canvas):
        canvas.create_image(self.cx, self.cy,   
            image=ImageTk.PhotoImage(self.buttonImage))

class TextBox():
    def __init__(self, textFile, x0, y0, x1, y1, toggleDelay):
        self.fileName = textFile
        self.textList = []
        self.displayedText = []

        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

        if toggleDelay: self.timerDelay = 500
        # when text is showing, make cat unable to move
    
    def readFile(self, app):
        # loop through words and store each character in textlist
        pass
    def timerFired(self, app):
        # go through textlist and add char by char to displayed text
        pass
    def redrawAll(self, app, canvas):
        # go through displayedtext and display it
        # use size calculations and amount of text to determine font size
        # and when to go to the next line
        # use a loop
        # when text is done showing, delete textbox and move cat
        pass

# make class that stores list of TextBoxes for every scene