from cmu_112_graphics import *
from mainCat import *
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
        app.prevMode = 'startScreenMode'
    @staticmethod
    def howToButtonFunc(app):
        app.mode = 'howToScreenMode'
        app.prevMode = 'startScreenMode'
    @staticmethod
    def backButtonFunc(app):
        app.mode = app.prevMode

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
            elif self.type == 'backButton':
                self.backButtonFunc(app)
        
    def redrawAll(self, app, canvas):
        canvas.create_image(self.cx, self.cy,   
            image=ImageTk.PhotoImage(self.buttonImage))

class TextBox():
    def __init__(self, textFile, x0, y0, x1, y1, toggleDelay):
        self.fileName = textFile
        self.textList = []
        self.readFile()

        self.displayedText = ""
        self.displayedIndex = 0
        self.displayStartIndex = 0
        self.toggleDelay = toggleDelay

        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

        self.timePassed = 0
        self.textEnded = False
        self.allEnd = False
        self.startText = True #Default is False, DEBUG makes it True

        # when text is showing, make cat unable to move
        # print("made textbox!")
        # self.cat = cat
        
    def appStarted(self, app):
        pass

    def readFile(self):
        filename = self.fileName
        
        with open(filename) as f:
            for line in f:
                for ch in line:
                    self.textList.append(ch)

    def timerFired(self, app):
        # print(self.timePassed)
        if self.startText and not self.textEnded:
            self.timePassed += 1
            if self.timePassed == 2:
                # print(self.displayedText)
                if self.displayedIndex < len(self.textList):
                    if (self.textList[self.displayedIndex] == '\n'):
                        self.textEnded = True
                        # self.displayedText = []
                    else:
                        self.displayedText += self.textList[self.displayedIndex]
                    self.displayedIndex += 1
                else:
                    self.textEnded = True
            elif self.timePassed > 2:
                self.timePassed = 0

    def keyPressed(self, app, event):
        if self.startText and self.textEnded and event.key == 'z':
            if self.displayedIndex >= len(self.textList):
                self.allEnd = True
                app.textOnScreen = False
            else:
                self.textEnded = False 
                self.displayedText = []
        if self.startText and not self.textEnded and event.key == 'x':
            while (self.displayedIndex < len(self.textList) and 
                    self.textList[self.displayedIndex] != '\n'):
                    self.displayedText += self.textList[self.displayedIndex]
                    self.displayedIndex += 1
                    if(self.displayedIndex >= len(self.textList)):
                        self.textEnded = True

    def redrawAll(self, app, canvas):
        if self.startText and not self.allEnd:
            canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, 
                                    fill='black', outline='white',
                                    width=4)
            chrX = self.x0 + 15
            chrY = self.y0 + 15
            # canvas.create_text(chrX, chrY, text=self.displayedText, font='Arial5',
            #                             fill='white')
            for chrInd in range(self.displayStartIndex, len(self.displayedText)):
                chr = self.displayedText[chrInd]
                if chrX > (self.x1-10):
                    chrX = self.x0 + 15
                    chrY += 20
                canvas.create_text(chrX, chrY, text=f"{chr}", font='Arial 20',
                                        fill='white')
                chrX += 15
        # go through displayedtext and display it
        # use size calculations and amount of text to determine font size
        # and when to go to the next line
        # use a loop
        # when text is done showing, delete textbox and move cat
        pass

# make class that stores list of TextBoxes for every scene
# make class for "static UI" the user can't interact with (HP)
# inventory