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

def appStarted(app):
    app.mode = 'startScreenMode'
    startScreenMode_appStarted(app)
    gameMode_appStarted(app)

def startScreenMode_appStarted(app): #startScreenMode
    app.background = app.loadImage('images/startScreen.png')
    
    app.startButton = Button('images/startButton.png', 150, 300, 'startButton')
    app.startButton.appStarted(app)
    
    app.howToButton = Button('images/howToButton.png', 150, 400, 'howToButton')
    app.howToButton.appStarted(app)

def startScreenMode_mousePressed(app, event):
    app.startButton.mousePressed(app, event)
    app.howToButton.mousePressed(app, event)

def startScreenMode_redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2, 
            image=ImageTk.PhotoImage(app.background))
    app.startButton.redrawAll(app, canvas)
    app.howToButton.redrawAll(app, canvas)
    
###########################################
def howToScreenMode_appStarted(app):
    # app.howToText = TextBox('insertfile', 20, 20, 580, 580, False)
    pass
def howToScreenMode_timerFired(app):
    app.howToText.timerFired

def howToScreenMode_redrawAll(app, canvas):
    app.howToText.redrawAll
###########################################
def gameMode_appStarted(app):
    mainCat.appStarted(app)
    bg1.appStarted(app)

def gameMode_keyPressed(app, event):
    mainCat.keyPressed(app, event)

def gameMode_keyReleased(app, event):
    mainCat.keyReleased(app, event)

def gameMode_timerFired(app):
    mainCat.timerFired(app)

def gameMode_redrawAll(app, canvas):
    bg1.redrawAll(app, canvas)
    mainCat.redrawAll(app, canvas)
###########################################
def main():
    print("Running game!")
    runApp(width=600,height=600)

main()