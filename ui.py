from cmu_112_graphics import *
from mainCat import *
from enemyattacks import *
class Button():
    def __init__(self, image, x, y, func):
        self.cx = x
        self.cy = y
        self.image = image 
        self.buttonImage = image
        self.funct = func
    
    def appStarted(self, app):
        self.buttonImage = app.loadImage(self.image)

    def mousePressed(self, app, event):
        x0 = self.cx - (self.buttonImage.width/2)
        y0 = self.cy - (self.buttonImage.height/2)
        x1 = self.cx + (self.buttonImage.width/2)
        y1 = self.cy + (self.buttonImage.height/2)
        if (event.x > x0 and event.x < x1 and 
            event.y > y0 and event.y < y1):
            self.funct(app)
        
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
        self.startText = False #Default is False, DEBUG makes it True

    def readFile(self):
        filename = self.fileName
        
        with open(filename) as f:
            for line in f:
                for ch in line:
                    self.textList.append(ch)

    def timerFired(self, app):
        if self.startText and not self.textEnded:
            self.timePassed += 1
            if self.timePassed == 2:
                if self.displayedIndex < len(self.textList):
                    if (self.textList[self.displayedIndex] == '\n'):
                        self.textEnded = True
                    else:
                        self.displayedText += self.textList[self.displayedIndex]
                    self.displayedIndex += 1
                else:
                    self.textEnded = True
            elif self.timePassed > 2:
                self.timePassed = 0

    def startEnemyAttackFunc(self, app):
        app.defending = True
        app.bossDefending = True
        import random
        attack1 = normalAttack1()
        attack2 = normalAttack2()
        attack3 = normalAttack3()
        enemyAttOptions = [attack1, attack2, attack3]
        
        randindex = random.randint(0, 2) # default 0, 2
        app.enemyAttack = enemyAttOptions[randindex]
        app.enemyAttack.attackOn = True
        
        if randindex == 2:
            app.batCat.cy = app.batCat.lowerBoundY - 20
            app.batCat.canMoveVert = False
        else:
            app.batCat.cx = 300
            app.batCat.cy = 350
            app.batCat.canMoveVert = True

    @staticmethod
    def triggerFuncs(self, app):
        if self.fileName == 'texts/scene1.2.txt':
            app.mode = 'gameMode2'

        elif self.fileName[6:12] == 'battle':
            if app.battleText == 4:
                 app.battleText = 0
            else:
                app.battleText += 1
            
            displaytext = "texts/hostiletext.txt" #level is 3 or 4
            if app.enemyInBattle.hostilityLevel == 0:
                if app.catInventory < 7:
                    app.catInventory += 1
                app.enemyInBattle.showing = False
                app.battleText = 0
                app.batCat = battleCat() #resets batcat
                app.batCat.appStarted(app)
                app.mode = 'gameMode21'
            else:
                app.enemyInBattle.hostilityLevel -= 1
                if app.enemyInBattle.hostilityLevel == 2:
                    displaytext = "texts/neutraltext.txt"
                elif app.enemyInBattle.hostilityLevel <= 1:
                    displaytext = "texts/friendlytext.txt"
                self.startEnemyAttackFunc(app)

            app.defaultText = TextBox(displaytext, 100, 260, 500, 425, True)
            app.defaultText.startText = True
            app.talking = False
        
        elif self.fileName[6:14] == 'bossnotr':
            app.bossText = TextBox('texts/bossnotready.txt', 20, 400, 580, 580, True)

        elif self.fileName[6:8] == 'bf':
            app.mode = 'bossBattleMode'
            app.enemyInBattle = app.bossCat
        
        elif self.fileName[6:14] == 'bosshost':
            displaytext = "texts/hostiletext.txt" 
            app.bossDefaultText = TextBox(displaytext, 100, 260, 500, 425, True)
            app.bossDefaultText.startText = True
            app.bossTalking = False

            self.startEnemyAttackFunc(app)
        
        elif self.fileName[6:11] == 'bossf':
            if app.bossBattleText == 4:
                 app.bossBattleText = 0
            else:
                app.bossBattleText += 1
            
            displaytext = "texts/hostiletext.txt" #level is 3 or 4
            if app.enemyInBattle.hostilityLevel == 0:
                app.enemyInBattle.showing = False
                app.bossBattleText = 0
                app.mode = 'gameMode2'
                app.bossCat.defeated = True
            else:
                app.enemyInBattle.hostilityLevel -= 1
                if app.enemyInBattle.hostilityLevel == 2:
                    displaytext = "texts/neutraltext.txt"
                elif app.enemyInBattle.hostilityLevel <= 1:
                    displaytext = "texts/friendlytext.txt"
                
                self.startEnemyAttackFunc(app)

            app.bossDefaultText = TextBox(displaytext, 100, 260, 500, 425, True)
            app.bossDefaultText.startText = True
            app.bossTalking = False

    def keyPressed(self, app, event):
        if self.startText and self.textEnded and event.key == 'z':
            if self.displayedIndex >= len(self.textList):
                self.allEnd = True
                self.startText = False
                if(app.mode == "gameMode"):
                    app.textOnScreen = False
                if(app.mode == "gameMode2"):
                    app.textOnScreen2 = False
                if(app.mode == "gameMode21"):
                    app.textOnScreen21 = False
                self.triggerFuncs(self, app)
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

            for chrInd in range(self.displayStartIndex, len(self.displayedText)):
                chr = self.displayedText[chrInd]
                if chrX > (self.x1-10):
                    chrX = self.x0 + 15
                    chrY += 20
                canvas.create_text(chrX, chrY, text=f"{chr}", font='Arial 20',
                                        fill='white')
                chrX += 15
