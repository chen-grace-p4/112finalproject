from cmu_112_graphics import *
from mainCat import *
from map import *

mainCat = Cat(600, 600)
bg1 = Background('bluemap1.png', 600, 600, mainCat)

def appStarted(app):
    mainCat.appStarted(app)
    bg1.appStarted(app)

def keyPressed(app, event):
    mainCat.keyPressed(app, event)

def redrawAll(app, canvas):
    bg1.redrawAll(app, canvas)
    mainCat.redrawAll(app, canvas)

def main():
    print("Running game!")
    runApp(width=600,height=600)

main()