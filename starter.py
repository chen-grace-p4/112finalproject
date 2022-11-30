from cmu_112_graphics import *
from mainCat import *
from map import *
from enemy import *
from enemyattacks import *
from ui import *

# note: all art (sprites, background, etc.) made by me!

# make UI/Buttons class for HP and items collected

# make inventory class (ways to add object to inventory)
# press "C" for inventory
# objects have description attached to them
# can interact with objects using "Z"

DEBUG = False
mainCat = Cat(600, 600, 'images/bluemap1.png')
bg1 = Background('images/bluemap1.png', 600, 600, mainCat)

def appStarted(app):
    # app.mode = 'startScreenMode'
    app.mode = 'gameMode21'
    app.prevMode = ''
    if DEBUG:
        app.mouseX = 0
        app.mouseY = 0
    startScreenMode_appStarted(app)
    gameMode_appStarted(app)
    howToScreenMode_appStarted(app)

    gameMode2_appStarted(app)
    gameMode21_appStarted(app)

    battleMode_appStarted(app)
    bossBattleMode_appStarted(app)

    gameModeEnd_appStarted(app)
###############################################
def startButtonFunc(app):
    app.mode = 'gameMode'

def howToButtonFunc(app):
    app.mode = 'howToScreenMode'

def startScreenMode_appStarted(app): #startScreenMode
    app.background = app.loadImage('images/startScreen.png')
    
    app.startButton = Button('images/startButton.png', 150, 300,
                        startButtonFunc)
    app.startButton.appStarted(app)
    
    app.howToButton = Button('images/howToButton.png', 150, 400,
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
def howToButtonFunc2(app):
    app.mode = 'startScreenMode'

def howToScreenMode_appStarted(app):
    app.howToButton2 = Button('images/howToButton.png', 150, 400,
                        howToButtonFunc2)
    app.howToButton2.appStarted(app)

def howToScreenMode_timerFired(app):
    # app.howToText.timerFired(app)
    pass
def howToScreenMode_mousePressed(app, event):
    app.howToButton2.mousePressed(app, event)
def howToScreenMode_mouseMoved(app, event):
    if DEBUG:
        app.mouseX = event.x
        app.mouseY = event.y
def howToScreenMode_redrawAll(app, canvas):
    startScreenMode_redrawAll(app, canvas)
    canvas.create_rectangle(200, 240, 430, 360, fill='white')
    displayedText = '''
        Use arrow keys to move around. 
        Press 'Z' to interact with something.
        Press 'Z' to continue text.
        Press 'X' to speed/skip up text.
        Press 'C' to see your health 
        and items left to collect.
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

    app.testDoor = InteractObj('images/redDoorObj.png',900, 480, 940, 530, 
                    mainCat, bg1.bgImage.height, redDoorFunc)
    app.testDoor.appStarted(app)
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
    
    canvas.create_text(100, 40, text=f"Your Health: {app.catHealth}/100",
                                        font='Arial 17',
                                        fill='white')
    
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
mainCat2 = Cat(600, 600, 'images/redmap1.png')
bg2 = Background('images/redmap1.png', 600, 600, mainCat2)
def door2Func(app):
    app.mode = 'gameMode21'

def blueDoorFunc(app):
    app.mode = 'gameModeEnd'

def gameMode2_appStarted(app):
    app.inventory = []

    mainCat2.appStarted(app)
    bg2.appStarted(app)
    app.scene21Text = TextBox('texts/scene2.1.txt', 20, 400, 580, 580, True)
    app.scene21Text.startText = True

    app.bossCat = BossEnemy('images/tempredcatsprites.png', 840, 300, 904, 364,
                                mainCat2, bg2.bgImage.height)
    app.bossCat.appStarted(app)
    app.bossText = TextBox('texts/bossnotready.txt', 20, 400, 580, 580, True)

    app.textOnScreen2 = True #Default is False, only True when textbox displayed
  
    app.testDoor2 = InteractObj('images/redDoorObj.png',380, 720, 420, 760, 
                            mainCat2, bg2.bgImage.height, door2Func)
    app.testDoor2.appStarted(app)
    app.blueDoor = InteractObj('images/blueDoorObj.png',1640, 860, 1680, 900, 
                            mainCat2, bg2.bgImage.height, blueDoorFunc)
    app.blueDoor.appStarted(app)
    app.bg2WallObj = []
    createWalls(bg2Walls, app, mainCat2, bg2, app.bg2WallObj)

    beforeDefeatBossWall = [(1000, 240, 1080, 380)]
    app.bfDefeatBossObj = []
    createWalls(beforeDefeatBossWall, app, mainCat2, bg2, app.bfDefeatBossObj)

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
    app.bossText.keyPressed(app, event)
    app.scene21Text.keyPressed(app, event)
    app.testDoor2.keyPressed(app, event)
    if app.catInventory >= 7:
        app.blueDoor.keyPressed(app, event)

def gameMode2_keyReleased(app, event):
    if not app.textOnScreen2: mainCat2.keyReleased(app, event)

def gameMode2_timerFired(app):
    mainCat2.timerFired(app)
    app.scene21Text.timerFired(app)
    app.bossText.timerFired(app)
    app.bossCat.timerFired(app)

def gameMode2_redrawAll(app, canvas):
    bg2.redrawAll(app, canvas)
    mainCat2.redrawAll(app, canvas)
    app.bossCat.redrawAll(app, canvas)
    app.testDoor2.redrawAll(app, canvas)

    if app.catInventory >= 7:
        app.blueDoor.redrawAll(app, canvas)

    app.scene21Text.redrawAll(app, canvas)
    app.bossText.redrawAll(app, canvas)

    for wall in app.bg2WallObj:
        wall.redrawAll(app, canvas)
    
    if not app.bossCat.defeated:
        app.bfDefeatBossObj[0].redrawAll(app, canvas)

    if not (app.textOnScreen2):
        canvas.create_text(100, 40, text=f"Your Health: {app.catHealth}/100",
                                            font='Arial 17',
                                            fill='white')
        
        if app.catInventory == 0:
            canvas.create_text(300, 10, text="Interact with red cats to get enough pieces to go home.", 
                                font='Arial 10', fill='#8ce8ff')
        elif app.catInventory == 7:
            canvas.create_text(460, 40, text='''You found all 7 pieces!''',
                                            font='Arial 20',
                                            fill='white')
            canvas.create_text(460, 65, text='''Find the blue door to go home.''',
                                            font='Arial 20',
                                            fill='white')
        elif app.catInventory > 0:
            canvas.create_text(460, 40, text=f"Pieces Left To Collect: {7 - app.catInventory}",
                                            font='Arial 20',
                                            fill='white')
        
        if app.catHealth < 20 and app.catInventory < 7:
            canvas.create_text(300, 80, text="Red cats will not interact with you if", 
                                font='Arial 15', fill='#8ce8ff')
            canvas.create_text(300, 100, text="your health is too low. Green items will heal you.",
                                font='Arial 15', fill='#8ce8ff')
        
        

###########################################
###########################################
bg21Walls = [(0, 0, 126, 1215), (130, 0, 256, 320),
            (256, 0, 1150, 128), (832, 128, 1150, 320),
            (320, 320, 384, 384), (448, 288, 575, 449),
            (576, 256, 704, 320), (255, 445, 575, 575),
            (705, 445, 830, 895), (830, 450, 960, 705),
            (125, 705, 580, 765), (320, 765, 575, 895),
            (125, 1150, 320, 1215), (320, 1022, 960, 1215),
            (960, 830, 1215, 1215), (1085, 705, 1215, 832),
            (1215, 705, 1340, 895), (1344, 960, 1410, 1090),
            (1220, 1152, 1472, 1215), (1470, 707, 1660, 1215),
            (1535, 576, 1600, 640), (1084, 445, 1340, 576),
            (1280, 248, 1342, 445), (1150, 0, 1790, 65),
            (1280, 50, 1790, 256), (1664, 256, 1790, 1215),
            (1470, 384, 1665, 510)]
mainCat21 = Cat(600, 600, 'images/redmap12.png')
bg21 = Background('images/redmap12.png', 600, 600, mainCat21)
def door21Func(app):
    app.mode = 'gameMode2'

def healthItemFunc(app):
    app.catHealth += 15
    if app.catHealth > 100:
        app.catHealth = 100

def gameMode21_appStarted(app):
    mainCat21.appStarted(app)
    bg21.appStarted(app)

    app.textOnScreen21 = False #Default is False, only True when textbox displayed
    app.testDoor21 = InteractObj('images/redDoorObj.png',170, 850, 210, 890, 
                            mainCat21, bg21.bgImage.height, door21Func)
    app.testDoor21.appStarted(app)

    app.graphRedMap21 = GraphCreator('redmap21', 19, 28)

    app.redmap21enemy1 = Enemy('images/tempredcatsprites.png', 384, 130, 448, 192, 
                                 mainCat21, bg21.bgImage.height, app.graphRedMap21)
    app.redmap21enemy2 = Enemy('images/tempredcatsprites.png', 640, 704, 704, 768, 
                                mainCat21, bg21.bgImage.height, app.graphRedMap21)
    app.redmap21enemy3 = Enemy('images/tempredcatsprites.png', 128, 384, 192, 448, 
                                mainCat21, bg21.bgImage.height, app.graphRedMap21)
    app.redmap21enemy4 = Enemy('images/tempredcatsprites.png', 1216, 192, 1280, 256, 
                                mainCat21, bg21.bgImage.height, app.graphRedMap21)
    app.redmap21enemy5 = Enemy('images/tempredcatsprites.png', 1120, 576, 1184, 640, 
                                mainCat21, bg21.bgImage.height, app.graphRedMap21)
    app.redmap21enemy6 = Enemy('images/tempredcatsprites.png', 1536, 512, 1600, 576, 
                                mainCat21, bg21.bgImage.height, app.graphRedMap21)
    app.redmap21enemy7 = Enemy('images/tempredcatsprites.png', 1216, 1024, 1280, 1088, 
                                mainCat21, bg21.bgImage.height, app.graphRedMap21)
    app.enemyList = [app.redmap21enemy1, app.redmap21enemy2,app.redmap21enemy3,
                     app.redmap21enemy4, app.redmap21enemy5, app.redmap21enemy6,
                     app.redmap21enemy7 ]

    for mapEnemy in app.enemyList:
        mapEnemy.appStarted(app)
    
    # make healing items have a cool down later
    app.healing1 = InteractObj('images/healthitem.png', 130, 770, 192, 832,
                                mainCat21, bg21.bgImage.height, healthItemFunc)
    app.healing2 = InteractObj('images/healthitem.png', 768, 130, 830, 192,
                                mainCat21, bg21.bgImage.height, healthItemFunc)
    app.healing3 = InteractObj('images/healthitem.png', 1024, 768, 1086, 832,
                                mainCat21, bg21.bgImage.height, healthItemFunc)
    app.healing4 = InteractObj('images/healthitem.png', 1600, 258, 1662, 320,
                                mainCat21, bg21.bgImage.height, healthItemFunc)
    
    app.healingList = [app.healing1, app.healing2, app.healing3, app.healing4]
    for healing in app.healingList:
        healing.appStarted(app)

    app.bg21WallObj = []
    createWalls(bg21Walls, app, mainCat21, bg21, app.bg21WallObj)

def gameMode21_keyPressed(app, event):
    if not app.textOnScreen21: mainCat21.keyPressed(app, event)
    app.scene21Text.keyPressed(app, event)
    app.testDoor21.keyPressed(app, event)
    for healing in app.healingList:
        healing.keyPressed(app, event)

def gameMode21_keyReleased(app, event):
    if not app.textOnScreen21: mainCat21.keyReleased(app, event)

def gameMode21_timerFired(app):
    mainCat21.timerFired(app)
    app.scene21Text.timerFired(app)

    for mapEnemy in app.enemyList:
        if (mapEnemy.healthLevel != 0 and 
            mapEnemy.hostilityLevel != 0):
            mapEnemy.timerFired(app)
    

def gameMode21_redrawAll(app, canvas):
    bg21.redrawAll(app, canvas)
    mainCat21.redrawAll(app, canvas)
    app.testDoor21.redrawAll(app, canvas)
    for mapEnemy in app.enemyList:
        if (mapEnemy.healthLevel != 0 and 
            mapEnemy.hostilityLevel != 0):
            mapEnemy.redrawAll(app, canvas)
    
    for healing in app.healingList:
        healing.redrawAll(app, canvas)

    for wall in app.bg21WallObj:
        wall.redrawAll(app, canvas)
    
    canvas.create_text(100, 40, text=f"Your Health: {app.catHealth}/100",
                                        font='Arial 17',
                                        fill='white')

    if app.catInventory == 7:
        canvas.create_text(460, 40, text='''You found all 7 pieces!''',
                                        font='Arial 20',
                                        fill='white')
        canvas.create_text(460, 65, text='''Find the blue door to go home.''',
                                        font='Arial 20',
                                        fill='white')
    elif app.catInventory > 0:
        canvas.create_text(460, 40, text=f"Pieces Left To Collect: {7 - app.catInventory}",
                                        font='Arial 20',
                                        fill='white')
    
    if app.catHealth < 20 and app.catInventory < 7:
            canvas.create_text(300, 80, text="Red cats will not interact with you if", 
                                font='Arial 15', fill='#8ce8ff')
            canvas.create_text(300, 100, text="your health is too low. Green items will heal you.",
                                font='Arial 15', fill='#8ce8ff')
    
    if app.catInventory < 7:
        canvas.create_text(300, 15, text="Interact with red cats to get enough pieces to go home.", 
                                font='Arial 15', fill='#8ce8ff')
    

###########################################
###########################################
# player can choose to fight to lower health level or talk to 
# lower hostility level 
# when either hp or hostility reaches 0, the battle ends and 
# the player gets a piece of a blue door

# if they fight, they will earn exp and level up themselves
# it will be easier to fight the boss battle and go home
# but they will leave thinking they shouldve never came and red sucks

# if they talk, they will earn no exp and have to fight longer,
# but at the end they will have become friends with the red cats
battleWalls = []

def fightButFunc(app):
    # app.attacking = True
    app.enemyInBattle.healthLevel -= app.catAttack
    app.defending = True
    import random
    attack1 = normalAttack1()
    attack2 = normalAttack2()
    attack3 = normalAttack3()
    enemyAttOptions = [attack1, attack2, attack3]
    
    randindex = random.randint(0, 2) # default 0, 2
    # randindex = 2
    app.enemyAttack = enemyAttOptions[randindex]
    app.enemyAttack.attackOn = True

    if randindex == 2:
        app.batCat.cy = app.batCat.lowerBoundY - 20
        app.batCat.canMoveVert = False
    else:
        app.batCat.cx = 300
        app.batCat.cy = 350
        app.batCat.canMoveVert = True

def talkButFunc(app):
    app.talking = True
    app.talkText.startText = True

import random
def battleMode_appStarted(app):
    app.batCat = battleCat()
    # battleBg = Background('images/battlebg.png', 600, 600, batCat)

    app.catHealth = 100
    app.catInventory = 7 # number of blue pieces you have
    # at the end, if cat's level is 3 or more, -> "bad" end
    # cat level is greater than 0 but less than 3 -> neutral end
    # cat level is 0 -> "good" end

    # cat's level goes up by 0.5 for every cat killed
    # killing final boss cat raises level by 3
    app.catLevel = 4
    app.catAttack = 20
    # for each level up, cat's attack goes up by 10
    app.battleNum = 1 #goes up to 7 for the 7th cat you can fight
    app.battleText = 0 #resets to 0 after every battle

    app.enemyInBattle = None
    app.talking = False 
    app.attacking = False 
    app.defending = False
    app.battleSelectOption = "fight"

    app.battleBg = app.loadImage('images/battlebg.png')
    app.batCat.appStarted(app)

    app.defaultText = TextBox('texts/hostiletext.txt', 100, 260, 500, 425, True)
    app.defaultText.startText = True

    app.talkText = TextBox(f'texts/battle{app.battleNum}.{app.battleText}.txt',
                        100, 260, 500, 425, True)

    app.fightBut = Button('images/fightbutton.png', 186, 486, fightButFunc)
    app.fightBut.appStarted(app)
    app.talkBut = Button('images/talkbutton.png', 412, 486, talkButFunc)
    app.talkBut.appStarted(app)

    # enemy attacks
    attack1 = normalAttack1()
    attack2 = normalAttack2()
    attack3 = normalAttack3()
    enemyAttOptions = [attack1, attack2, attack3]
    
    randindex = random.randint(0, 2)
    app.enemyAttack = enemyAttOptions[randindex]


def battleMode_keyPressed(app, event):
    if not app.talking and not app.attacking and not app.defending:
        if event.key == 'Right' or event.key == "Left":
            if app.battleSelectOption == "fight":
                app.battleSelectOption = "talk"
            else:
                app.battleSelectOption = "fight"
        elif event.key == "z":
            if app.battleSelectOption == "fight":
                app.fightBut.funct(app)
            else:
                app.talkText = TextBox(f'texts/battle{app.battleNum}.{app.battleText}.txt',
                        100, 260, 500, 425, True)
                app.talkBut.funct(app)
        elif event.key == "x":
            app.defaultText.keyPressed(app, event)
    elif app.talking:
        app.talkText.keyPressed(app, event)
    elif app.defending:
        app.batCat.keyPressed(app, event)

def battleMode_keyReleased(app, event):
    if app.defending:
        app.batCat.keyReleased(app, event)

def battleMode_timerFired(app):
    # add ending animation + text to explain you got a blue door piece
    # after choosing to fight to end the battle
    if app.enemyInBattle.healthLevel <= 0:
        app.catInventory += 1
        app.catLevel += 1
        app.catAttack += 10
        app.enemyInBattle.showing = False
        # app.battleNum += 1 # add in later when i have more texts
        app.battleText = 0
        app.batCat = battleCat() #resets batcat
        app.batCat.appStarted(app)
        app.mode = 'gameMode21'
        app.defending = False
    if not app.talking and not app.attacking and not app.defending:
        app.defaultText.timerFired(app)
    elif app.talking:
        app.talkText.timerFired(app)
    elif app.defending:
        app.batCat.timerFired(app)
        app.enemyAttack.timerFired(app)

def battleMode_redrawAll(app, canvas):
    canvas.create_image(300, 300,  
            image=ImageTk.PhotoImage(app.battleBg))
    if not app.talking and not app.attacking and not app.defending:
        app.defaultText.redrawAll(app, canvas)

        if app.battleSelectOption == "fight":
            app.fightBut.redrawAll(app, canvas)
        elif app.battleSelectOption == "talk":
            app.talkBut.redrawAll(app, canvas)
    elif app.talking:
        app.talkText.redrawAll(app, canvas)
    elif app.defending:
        app.batCat.redrawAll(app, canvas)
        app.enemyAttack.redrawAll(app, canvas)
    
    #enemy health
    canvas.create_text(485, 160, text=f"Enemy Health: {app.enemyInBattle.healthLevel}/100", 
                                        font='Arial 15',
                                        fill='white')
    #player health and level
    canvas.create_text(175, 550, text=f"Your Health: {app.catHealth}/100",
                                        font='Arial 15',
                                        fill='white')
    canvas.create_text(400, 550, text=f"Your Level: {app.catLevel}",
                                        font='Arial 15',
                                        fill='white')

###########################################
###########################################
###########################################

battleWalls = []

def bossFightButFunc(app):
    # app.bossAttacking = True
    app.enemyInBattle.healthLevel -= app.catAttack
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

def bossTalkButFunc(app):
    app.bossTalking = True
    app.bossTalkText.startText = True

import random
def bossBattleMode_appStarted(app):
    app.batCat = battleCat()
    app.batCat.appStarted(app)
    app.bossBattleText = 0 #resets to 0 after every battle

    app.bossTalking = False 
    app.bossAttacking = False 
    app.bossDefending = False
    app.bossBattleSelectOption = "fight"

    app.batCat.appStarted(app)

    app.bossDefaultText = TextBox('texts/hostiletext.txt', 100, 260, 500, 425, True)
    app.bossDefaultText.startText = True

    if app.catLevel == 0:
        app.bossTalkText = TextBox(f'texts/bossfriend1.{app.bossBattleText}.txt',
                        100, 260, 500, 425, True)
    else:
        app.bossTalkText = TextBox(f'texts/bosshostneut.txt',
                        100, 260, 500, 425, True)

    app.bossFightBut = Button('images/fightbutton.png', 186, 486, bossFightButFunc)
    app.bossFightBut.appStarted(app)
    app.bossTalkBut = Button('images/talkbutton.png', 412, 486, bossTalkButFunc)
    app.bossTalkBut.appStarted(app)

    # enemy attacks
    attack1 = normalAttack1()
    attack2 = normalAttack2()
    attack3 = normalAttack3()
    enemyAttOptions = [attack1, attack2, attack3]
    
    randindex = random.randint(0, 2)
    app.enemyAttack = enemyAttOptions[randindex]


def bossBattleMode_keyPressed(app, event):
    if not app.bossTalking and not app.bossAttacking and not app.bossDefending:
        if event.key == 'Right' or event.key == "Left":
            if app.bossBattleSelectOption == "fight":
                app.bossBattleSelectOption = "talk"
            else:
                app.bossBattleSelectOption = "fight"
        elif event.key == "z":
            if app.bossBattleSelectOption == "fight":
                app.bossFightBut.funct(app)
            else:
                if app.catLevel == 0:
                    app.bossTalkText = TextBox(f'texts/bossfriend1.{app.bossBattleText}.txt',
                        100, 260, 500, 425, True)
                else:
                    app.bossTalkText = TextBox(f'texts/bosshostneut.txt',
                        100, 260, 500, 425, True)
                app.bossTalkBut.funct(app)
        elif event.key == "x":
            app.bossDefaultText.keyPressed(app, event)
    elif app.bossTalking:
        app.bossTalkText.keyPressed(app, event)
    elif app.bossDefending:
        app.batCat.keyPressed(app, event)

def bossBattleMode_keyReleased(app, event):
    if app.bossDefending:
        app.batCat.keyReleased(app, event)

def bossBattleMode_timerFired(app):
    if app.enemyInBattle.healthLevel <= 0:
        app.enemyInBattle.showing = False
        app.bossBattleText = 0
        app.mode = 'gameMode2'
        app.bossCat.defeated = True
        app.bossDefending = False
        app.catLevel += 3
    if not app.bossTalking and not app.bossAttacking and not app.bossDefending:
        app.bossDefaultText.timerFired(app)
    elif app.bossTalking:
        app.bossTalkText.timerFired(app)
    elif app.bossDefending:
        app.batCat.timerFired(app)
        app.enemyAttack.timerFired(app)

def bossBattleMode_redrawAll(app, canvas):
    canvas.create_image(300, 300, 
            image=ImageTk.PhotoImage(app.battleBg))
    if not app.bossTalking and not app.bossAttacking and not app.bossDefending:
        app.bossDefaultText.redrawAll(app, canvas)

        if app.bossBattleSelectOption == "fight":
            app.bossFightBut.redrawAll(app, canvas)
        elif app.bossBattleSelectOption == "talk":
            app.bossTalkBut.redrawAll(app, canvas)
    elif app.bossTalking:
        app.bossTalkText.redrawAll(app, canvas)
    elif app.bossDefending:
        app.batCat.redrawAll(app, canvas)
        app.enemyAttack.redrawAll(app, canvas)
    
    #enemy health
    canvas.create_text(485, 160, text=f"Enemy Health: {app.enemyInBattle.healthLevel}/100", 
                                        font='Arial 15',
                                        fill='white')
    #player health and level
    canvas.create_text(175, 550, text=f"Your Health: {app.catHealth}/100",
                                        font='Arial 15',
                                        fill='white')
    canvas.create_text(400, 550, text=f"Your Level: {app.catLevel}",
                                        font='Arial 15',
                                        fill='white')
#######################################################
endWalls = [(0, 0, 330, 440),
            (300, 0, 480, 100),
            (480, 0, 1020, 440),
            (1020, 440, 1200, 570),
            (0, 570, 1020, 780)]

mainCatEnd = Cat(600, 600, 'images/bluemap1.png')
bgEnd = Background('images/bluemap1.png', 600, 600, mainCatEnd)

def gameModeEnd_appStarted(app):
    mainCatEnd.appStarted(app)
    bgEnd.appStarted(app)
    # app.scene11Text = TextBox('texts/scene1.1.txt', 20, 400, 580, 580, True)
    # app.scene11Text.startText = True
    # # app.scene1Text.appStarted(app) # appstarted doens't do anything yet
    # app.scene12Text = TextBox('texts/scene1.2.txt', 20, 400, 580, 580, True)
    # app.textOnEndScreen = True #Default is False, only True when textbox displayed

    app.endWallObj = []
    createWalls(endWalls, app, mainCatEnd, bgEnd, app.endWallObj)

def gameModeEnd_keyPressed(app, event):
    # if not app.textOnScreen: 
    mainCatEnd.keyPressed(app, event)
    # if app.scene11Text.startText:
    #     app.scene11Text.keyPressed(app, event)
    # if app.scene12Text.startText:
    #     app.scene12Text.keyPressed(app, event)

def gameModeEnd_keyReleased(app, event):
    # if not app.textOnScreen: 
    mainCatEnd.keyReleased(app, event)

def gameModeEnd_timerFired(app):
    mainCatEnd.timerFired(app)
    # if app.scene11Text.startText:
    #     app.scene11Text.timerFired(app)
    # if app.scene12Text.startText:
    #     app.scene12Text.timerFired(app)

def gameModeEnd_redrawAll(app, canvas):
    bgEnd.redrawAll(app, canvas)
    mainCatEnd.redrawAll(app, canvas)
    app.testDoor.redrawAll(app, canvas)
    # if app.scene11Text.startText:
    #     app.scene11Text.redrawAll(app, canvas)
    # if app.scene12Text.startText:
    #     app.scene12Text.redrawAll(app, canvas)
    for wall in app.endWallObj:
        wall.redrawAll(app, canvas)
    
    canvas.create_text(100, 40, text=f"Your Health: {app.catHealth}/100",
                                        font='Arial 17',
                                        fill='white')

def main():
    print("Running game!")
    runApp(width=600,height=600)

main()