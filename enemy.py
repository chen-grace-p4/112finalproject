from cmu_112_graphics import * 
from map import *
from ui import *

# (startRow, startCol, endRow, endCol)
REDMAP12PATHS = ((12, 2, 17, 4), (14, 5, 15, 14),
                (11, 9, 13, 10), (9, 4, 10, 10),
                (5, 2, 10, 3), (4, 4, 6, 4),
                (6, 5, 6, 5), (5, 6, 6, 6),
                (4, 5, 4, 6), (2, 4, 3, 12),
                (4, 11, 4, 12), (5, 9, 8, 10),
                (5, 11, 6, 19), (1, 18, 4, 19),
                (11, 13, 13, 14), (7, 15, 12, 16),
                (9, 17, 10, 23), (4, 21, 8, 22),
                (4, 23, 5, 25), (8, 23, 8, 25),
                (10, 24, 10, 24), (9, 25, 10, 25),
                (11, 21, 14, 22), (14, 19, 17, 20),
                (17, 21, 17, 21), (15, 22, 17, 22))
NORTH = (-1, 0)
SOUTH = (1, 0)
EAST = (0, 1)
WEST = (0, -1)
class GraphCreator():
    def __init__(self, mapName, rows, cols):
        # False means can't walk there
        # True means there is a path there
        self.graph2dList = self.defaultGraph(rows, cols)
        # print(self.graph2dList)
        self.rows = rows
        self.cols = cols
        if mapName == 'redmap21':
            self.createAllPaths(REDMAP12PATHS)

    # returns array of False with rows and cols
    def defaultGraph(self, rows, cols):
        return [ ([False] * cols) for row in range(rows)]
    
    # modifies values in default graph to be True (become paths)
    # works like creating a rectangle 
    def pathCreator(self, stRow, stCol, edRow, edCol):
        for r in range(stRow, edRow+1):
            for c in range(stCol, edCol+1):
                self.graph2dList[r][c] = True
    
    # takes self.mapName and creates paths for that map
    # goes through tuples of all paths for that map 
    # calls pathCreator 
    def createAllPaths(self, mapPathList):
        for path in mapPathList:
            self.pathCreator(path[0], path[1], path[2], path[3])
    
    # maybe not needed
    # returns self.graph2dList
    def getGraph(self):
        pass
    
    # returns row and col of something 
    # based on their cx and cy location on entire map
    def getGraphLocation(self, cx, cy):
        rowLoc = cy // 64
        colLoc = cx // 64
        return (rowLoc, colLoc)

# maybe don't inherit from object and do collision by graph
class Enemy(Object):
    # give it a spawning point on map
    def __init__(self, image, x0, y0, x1, y1, cat, bgHeight, graph):
        self.healthLevel = 100
        self.hostilityLevel = 4

        self.showing = True

        self.image = image
        super().__init__(x0, y0, x1, y1, cat, bgHeight)

        self.graph = graph
        self.bgY0 = y0 
        self.bgY1 = y1 

        self.cx = self.x0 + 32
        self.cy = self.bgY0 + 32

        graphLocation = graph.getGraphLocation(self.cx, self.cy)
        self.spawnRow = graphLocation[0]
        self.spawnCol = graphLocation[1]

        self.currentRow = self.spawnRow 
        self.currentCol = self.spawnCol

        self.timePassed = 0

        catLoca = self.cat.getCatLocation()
        self.prevCatX = catLoca[0]
        self.prevCatY = catLoca[1]
        self.currCatX = catLoca[0]
        self.currCatY = catLoca[1]
    
    def appStarted(self, app):
        objImage = app.loadImage(self.image)
        self.objImage = objImage.crop((0, 0, 64, 64))
        if self.catInRange:
            self.path = self.pathToCat(app)
        else: self.path = []
    
    # determines if cat is in range and whether it should move to cat
    # returns direction enemy should move to cat
    # backtrack that direction first
    def catInRange(self):
        catLoca = self.cat.getCatLocation()
        catX = catLoca[0]
        catY = catLoca[1]
        if abs(self.cx - catX) <= 250 and abs(self.cy - catY) <= 250:
            # cat is further horizontally than vertically
            if abs(self.cx - catX) > abs(self.cy - catY):
                if self.cx < catX:
                    return "east" 
                else: #self.cx > catX
                    return "west"
            else: # cat is further vertically than horizontally
                if self.cy < catY:
                    return "south"
                else: #self.cy > catY
                    return "north"
        return None

    def spawnDirection(self):
        spawnY = self.spawnRow * 64
        spawnX = self.spawnCol * 64

        if abs(self.cx - spawnX) > abs(self.cy - spawnY):
            if self.cx < spawnX:
                return "east" 
            else: #self.cx > catX
                return "west"
        else: # cat is further vertically than horizontally
            if self.cy < spawnY:
                return "south"
            else: #self.cy > catY
                return "north"

    # referenced https://www.cs.cmu.edu/~112/notes/maze-solver.py
    # read https://en.wikipedia.org/wiki/Depth-first_search 
    def pathToCat(self, app):
        visited = set()
        path = []
        return self.findPath(app, path, visited, 
                    self.currentRow, self.currentCol)

    def findPath(self, app, path, visited, row, col):
        targetRow = 0
        targetCol = 0
        
        firstDir = "south"
        if self.catInRange() != None:
            catLoca = self.cat.getCatLocation()
            catGraphLoca = self.graph.getGraphLocation(catLoca[0], catLoca[1])
            targetRow = catGraphLoca[0]
            targetCol = catGraphLoca[1]
            firstDir = self.catInRange()
        else: # if cat is not in range, go to spawn instead
            targetRow = self.spawnRow
            targetCol = self.spawnCol
            firstDir = self.spawnDirection()

        if (row, col) in visited:
            return None 
        
        visited.add((row, col))
        path.append((row,col))

        if (row, col) == (targetRow, targetCol):
            if self.catNearObj():
                app.mode = 'battleMode'
                app.enemyInBattle = self
            return path
        
        else:
            dirlist = []
            if firstDir == "south":
                dirlist = [SOUTH, WEST, EAST, NORTH]
            elif firstDir == "west":
                dirlist = [WEST, SOUTH, NORTH, EAST]
            elif firstDir == "east":
                dirlist = [EAST, SOUTH, NORTH, WEST]
            elif firstDir == "north":
                dirlist = [NORTH, WEST, EAST, SOUTH]
            for drow, dcol in dirlist:
                if self.isValid(app, row, col, (drow, dcol)):
                    result = self.findPath(app, path, visited, row+drow, col+dcol)
                    if result != None:
                        return result 
        path.pop()
        return None

    def isValid(self, app, row, col, dir):
        if not (0<=row<self.graph.rows and 0<=col<self.graph.cols): 
            return False
        if not (0<=(row+dir[0])<self.graph.rows and 0<=(col+dir[1])<self.graph.cols): 
            return False
        return self.graph.graph2dList[row+dir[0]][col+dir[1]]

    def catNearObj(self):
        return (abs(self.currCatX - self.cx) <= 64 and 
                abs(self.currCatY - self.cy) <= 64)
    
    def moveEnemyToNode(self, app, targRow, targCol):
        if not self.catNearObj():
            if (targRow > self.currentRow):
                self.y0 += 5
                self.y1 += 5
                self.bgY0 += 5
            elif (targRow < self.currentRow):
                self.y0 -= 5
                self.y1 -= 5
                self.bgY0 -= 5
            elif (targCol > self.currentCol):
                self.x0 += 5
                self.x1 += 5
            elif (targCol < self.currentCol):
                self.x0 -= 5
                self.x1 -= 5

    @staticmethod
    # contains information for enemy1
    def enemy1(app):
        pass

    def keyPressed(self, app, event):
        if self.showing:
            if (self.catNearObj() and event.key == 'z'):
                # activate textbox
                pass

    def timerFired(self, app):
        if self.showing:
            self.timePassed += 1
            # print(app.timePassed)
            
            if self.timePassed == 5:
                catLoca = self.cat.getCatLocation()
                catX = catLoca[0]
                catY = catLoca[1]
                self.currCatX = catX 
                self.currCatY = catY
            elif self.timePassed > 5:
                self.timePassed = 0
                self.prevCatX = self.currCatX
                self.prevCatY = self.currCatY

            self.cx = self.x0 + 32
            self.cy = self.bgY0 + 32

            # print(self.cx, self.cy)
            # catLoca = self.cat.getCatLocation()
            # catX = catLoca[0]
            # catY = catLoca[1]
            # print(catX, catY)
            currentGraphLoca = self.graph.getGraphLocation(self.cx, self.cy)
            self.currentRow = currentGraphLoca[0]
            self.currentCol = currentGraphLoca[1]

            if self.prevCatX != self.currCatX or self.prevCatY != self.currCatY:
                # print("cat moved!")
                self.path = self.pathToCat(app)
                # print(self.path)

            if len(self.path) > 0:
                move = self.path[0]
                self.moveEnemyToNode(app, move[0], move[1])
                if self.currentRow == move[0] and self.currentCol == move[1]:
                    self.path.pop(0)

    def redrawAll(self, app, canvas):
        if (self.showing):
            cx = self.x0 + (self.objImage.width/2)
            cy = self.y0 + (self.objImage.height/2)
            cx -= self.cat.scrollX
            cy -= self.cat.scrollY
            
            # x0 = self.x0 
            # x1 = self.x1
            # y0 = self.y0
            # y1 = self.y1

            # x0 -= self.cat.scrollX
            # x1 -= self.cat.scrollX
            # y0 -= self.cat.scrollY
            # y1 -= self.cat.scrollY

            # canvas.create_rectangle(x0, y0, x1, y1, fill='yellow')
            canvas.create_image(cx, cy,   
                image=ImageTk.PhotoImage(self.objImage))
            self.checkCollision()

# enemy that you can talk with outside of battle
# starts battle by dialogue, not by contact
# boss enemy spawns in a given location 
class BossEnemy(Object):
    def __init__(self, image, x0, y0, x1, y1, cat, bgHeight):
        self.healthLevel = 100
        self.hostilityLevel = 4

        self.showing = True

        self.image = image
        super().__init__(x0, y0, x1, y1, cat, bgHeight)

        self.bgY0 = y0 
        self.bgY1 = y1 

        self.cx = self.x0 + 32
        self.cy = self.bgY0 + 32

        self.timePassed = 0

        catLoca = self.cat.getCatLocation()
        self.currCatX = catLoca[0]
        self.currCatY = catLoca[1]

        self.defeated = False

    def appStarted(self, app):
        objImage = app.loadImage(self.image)
        self.objImage = objImage.crop((0, 0, 64, 64))

    def catInRange(self):
        return (abs(self.currCatX - self.cx) <= 100 and 
                abs(self.currCatY - self.cy) <= 100)

    # if user is neutral or hostile, talking to the boss is useless
    # there will only be friendly responses if user has been friendly

    def timerFired(self, app):
        if (self.showing):
            catLoca = self.cat.getCatLocation()
            self.currCatX = catLoca[0]
            self.currCatY = catLoca[1]
            self.timePassed += 1

            if self.timePassed == 50:
                if (not self.defeated and self.catInRange() and not app.textOnScreen2):
                    # print("cat in range")
                    if (app.catInventory >= 7):
                        bossFile = "texts/bfbossneutral.txt"
                        if (app.catLevel >= 3):
                            bossFile = "texts/bfbosshostile.txt"
                        elif (app.catLevel == 0):
                            bossFile = "texts/bfbossfriendly.txt"
                        app.bossText = TextBox(bossFile, 20, 400, 580, 580, True)
                    app.bossText.startText = True
                    app.textOnScreen2 = True
            elif self.timePassed > 50:
                self.timePassed = 0
        # print("cat not in range")
    
    def redrawAll(self, app, canvas):
        if (self.showing):
            cx = self.x0 + (self.objImage.width/2)
            cy = self.y0 + (self.objImage.height/2)
            cx -= self.cat.scrollX
            cy -= self.cat.scrollY
    
            canvas.create_image(cx, cy,   
                image=ImageTk.PhotoImage(self.objImage))
            self.checkCollision()