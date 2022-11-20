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

def startScreenMode_appStarted(app): #startScreenMode
    app.background = app.loadImage('images/startScreen.png')
    
    app.startButton = Button('images/startButton.png', 150, 300, 'startButton')
    app.startButton.appStarted(app)
    
    app.howToButton = Button('images/howToButton.png', 150, 400, 'howToButton')
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
def gameMode_appStarted(app):
    mainCat.appStarted(app)
    bg1.appStarted(app)
    app.scene1Text = TextBox('texts/scene1.txt', 20, 400, 580, 580, True)
    app.scene1Text.appStarted(app) # appstarted doens't do anything yet
    app.textOnScreen = True #Default is False, only True when textbox displayed

    app.testObject = Object(200, 200, 250, 250, mainCat)

def gameMode_keyPressed(app, event):
    if not app.textOnScreen: mainCat.keyPressed(app, event)
    app.scene1Text.keyPressed(app, event)

def gameMode_keyReleased(app, event):
    if not app.textOnScreen: mainCat.keyReleased(app, event)

def gameMode_timerFired(app):
    mainCat.timerFired(app)
    app.scene1Text.timerFired(app)

def gameMode_redrawAll(app, canvas):
    bg1.redrawAll(app, canvas)
    mainCat.redrawAll(app, canvas)
    app.scene1Text.redrawAll(app, canvas)
    app.testObject.redrawAll(app, canvas)
    # when cat reaches red door, change app.scene1Text.startText = True
    # and textonscreen = true
###########################################
def main():
    print("Running game!")
    runApp(width=600,height=600)

main()