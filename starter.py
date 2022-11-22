from cmu_112_graphics import *
from mainCat import *
from map import *
from ui import *

# note: all art (sprites, bg, etc.) made by me!
mainCat = Cat(600, 600)
bg1 = Background('images/bluemap1.png', 600, 600, mainCat)
# make different backgrounds different modes
# add ways to trigger changing of modes

# make a start screen + story screen
# make textbox 

# make UI/Buttons class for HP and items collected

# make inventory class (ways to add object to inventory)
# press "C" for inventory
# objects have description attached to them
# can interact with objects using "Z"

# make enemy class
# def startButtonFunc(app):
#     app.mode = 'gameMode'
DEBUG = False

def appStarted(app):
    app.mode = 'startScreenMode'
    app.prevMode = ''
    if DEBUG:
        app.mouseX = 0
        app.mouseY = 0
    startScreenMode_appStarted(app)
    gameMode_appStarted(app)
    howToScreenMode_appStarted(app)

    gameMode2_appStarted(app)
###############################################
def startButtonFunc(app):
    app.mode = 'gameMode'
    app.prevMode = 'startScreenMode'

def howToButtonFunc(app):
    app.mode = 'howToScreenMode'
    app.prevMode = 'startScreenMode'

def backButtonFunc(app):
    app.mode = app.prevMode

def startScreenMode_appStarted(app): #startScreenMode
    app.background = app.loadImage('images/startScreen.png')
    
    app.startButton = Button('images/startButton.png', 150, 300, 'startButton',
                        startButtonFunc)
    app.startButton.appStarted(app)
    
    app.howToButton = Button('images/howToButton.png', 150, 400, 'howToButton',
                        howToButtonFunc)
    app.howToButton.appStarted(app)

def startScreenMode_mousePressed(app, event):
    app.startButton.mousePressed(app, event)
    app.howToButton.mousePressed(app, event)

def startScreenMode_mouseMoved(app, event):
    if DEBUG:
        app.mouseX = event.x
        app.mouseY = event.y

def startScreenMode_redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2, 
            image=ImageTk.PhotoImage(app.background))
    app.startButton.redrawAll(app, canvas)
    app.howToButton.redrawAll(app, canvas)
    if DEBUG:
        canvas.create_text(app.mouseX, app.mouseY, 
                            text=f"{app.mouseX}, {app.mouseY}")
    
###########################################
# DRAW IMAGE FOR HELP TEXTBOX LATER AND JUST SHOW IMAGE
def howToScreenMode_appStarted(app):
    # app.howToText = TextBox('texts/howtoplay.txt', 20, 20, 580, 580, False)
    # app.howToText.appStarted(app)
    # app.howToBackButton = Button()
    pass
def howToScreenMode_timerFired(app):
    # app.howToText.timerFired(app)
    pass
def howToScreenMode_mousePressed(app, event):
    pass
def howToScreenMode_mouseMoved(app, event):
    if DEBUG:
        app.mouseX = event.x
        app.mouseY = event.y
def howToScreenMode_redrawAll(app, canvas):
    startScreenMode_redrawAll(app, canvas)
    canvas.create_rectangle(200, 260, 430, 360, fill='white')
    displayedText = '''
        Use arrow keys to move around. 
        Press 'Z' to interact with something.
        Press 'Z' to continue text.
        Press 'X' to speed/skip up text.
        Press 'C' to open inventory.
    '''
    canvas.create_text(300, 300, text=displayedText, font='Arial5',
                                    fill='black')
    if DEBUG:
        canvas.create_text(app.mouseX, app.mouseY, 
                            text=f"{app.mouseX}, {app.mouseY}")
    # app.howToText.redrawAll(app, canvas)
###########################################
bg1Walls = [(0, 0, 330, 440),
            (300, 0, 480, 100),
            (480, 0, 1020, 440),
            (1020, 440, 1200, 570),
            (0, 570, 1020, 780)]

def redDoorFunc(app):
    app.scene12Text.startText = True
    app.textOnScreen = True

def gameMode_appStarted(app):
    mainCat.appStarted(app)
    bg1.appStarted(app)
    app.scene11Text = TextBox('texts/scene1.1.txt', 20, 400, 580, 580, True)
    app.scene11Text.startText = True
    # app.scene1Text.appStarted(app) # appstarted doens't do anything yet
    app.scene12Text = TextBox('texts/scene1.2.txt', 20, 400, 580, 580, True)
    app.textOnScreen = True #Default is False, only True when textbox displayed

    app.testDoor = InteractObj('redDoorObj.png',900, 480, 940, 530, 
                    mainCat, bg1.bgImage.height, redDoorFunc)

    app.bg1WallObj = []
    createWalls(bg1Walls, app, mainCat, bg1, app.bg1WallObj)

def createWalls(wallList, app, cat, bg, newList):
    for tup in wallList:
        x0 = tup[0]
        y0 = tup[1]
        x1 = tup[2]
        y1 = tup[3]
        obj = Object(x0, y0, x1, y1, cat, bg.bgImage.height)
        newList.append(obj)

def gameMode_keyPressed(app, event):
    if not app.textOnScreen: mainCat.keyPressed(app, event)
    if app.scene11Text.startText:
        app.scene11Text.keyPressed(app, event)
    if app.scene12Text.startText:
        app.scene12Text.keyPressed(app, event)
    app.testDoor.keyPressed(app, event)

def gameMode_keyReleased(app, event):
    if not app.textOnScreen: mainCat.keyReleased(app, event)

def gameMode_timerFired(app):
    mainCat.timerFired(app)
    if app.scene11Text.startText:
        app.scene11Text.timerFired(app)
    if app.scene12Text.startText:
        app.scene12Text.timerFired(app)

def gameMode_redrawAll(app, canvas):
    bg1.redrawAll(app, canvas)
    mainCat.redrawAll(app, canvas)
    app.testDoor.redrawAll(app, canvas)
    if app.scene11Text.startText:
        app.scene11Text.redrawAll(app, canvas)
    if app.scene12Text.startText:
        app.scene12Text.redrawAll(app, canvas)
    for wall in app.bg1WallObj:
        wall.redrawAll(app, canvas)
    
###########################################
###########################################
bg2Walls = [(0, 0, 680, 500),
            (690, 0, 1080, 150),
            (1080, 0, 1780, 260),
            (1560, 260, 1800, 710),
            (1760, 710, 1800, 1045),
            (1490, 1045, 1800, 1250),
            (1100, 350, 1480, 1180),
            (990, 490, 1100, 1180),
            (480, 500, 850, 890),
            (0, 500, 350, 890),
            (0, 1040, 980, 1240)]
mainCat2 = Cat(600, 600)
bg2 = Background('images/redmap1.png', 600, 600, mainCat2)
def gameMode2_appStarted(app):
    app.inventory = []

    mainCat2.appStarted(app)
    bg2.appStarted(app)
    app.scene21Text = TextBox('texts/scene2.1.txt', 20, 400, 580, 580, True)
    app.scene21Text.startText = True
    # app.scene1Text.appStarted(app) # appstarted doens't do anything yet
    app.textOnScreen2 = True #Default is False, only True when textbox displayed
    print(f"appstarted textOnScreen2: {app.textOnScreen2}")
    # app.testDoor = InteractObj('redDoorObj.png',900, 480, 940, 530, mainCat, bg1.bgImage.height)

    app.bg2WallObj = []
    createWalls(bg2Walls, app, mainCat2, bg2, app.bg2WallObj)

def createWalls(wallList, app, cat, bg, newList):
    for tup in wallList:
        x0 = tup[0]
        y0 = tup[1]
        x1 = tup[2]
        y1 = tup[3]
        obj = Object(x0, y0, x1, y1, cat, bg.bgImage.height)
        newList.append(obj)

def gameMode2_keyPressed(app, event):
    if not app.textOnScreen2: mainCat2.keyPressed(app, event)
    app.scene21Text.keyPressed(app, event)
    # app.testDoor.keyPressed(app, event)

def gameMode2_keyReleased(app, event):
    if not app.textOnScreen2: mainCat2.keyReleased(app, event)

def gameMode2_timerFired(app):
    mainCat2.timerFired(app)
    app.scene21Text.timerFired(app)

def gameMode2_redrawAll(app, canvas):
    bg2.redrawAll(app, canvas)
    mainCat2.redrawAll(app, canvas)
    # app.testDoor.redrawAll(app, canvas)
    app.scene21Text.redrawAll(app, canvas)
    for wall in app.bg2WallObj:
        wall.redrawAll(app, canvas)
    
###########################################
def main():
    print("Running game!")
    runApp(width=600,height=600)

main()