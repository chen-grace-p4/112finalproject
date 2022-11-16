from cmu_112_graphics import *
from mainCat import *
from map import *

# note: all art (sprites, bg, etc.) made by me!
mainCat = Cat(600, 600)
bg1 = Background('bluemap1.png', 600, 600, mainCat)
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
def appStarted(app):
    mainCat.appStarted(app)
    bg1.appStarted(app)

def keyPressed(app, event):
    mainCat.keyPressed(app, event)

def keyReleased(app, event):
    mainCat.keyReleased(app, event)

def timerFired(app):
    mainCat.timerFired(app)

def redrawAll(app, canvas):
    bg1.redrawAll(app, canvas)
    mainCat.redrawAll(app, canvas)

def main():
    print("Running game!")
    runApp(width=600,height=600)

main()