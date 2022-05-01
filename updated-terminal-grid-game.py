# this is the python file we are using to simulate the grid
# By using python we have simulated a grid
# it is a 10 x 10 grid 
# the rules are you can only mode up down left and right
# you can only see an obstacle if you move next to an obstacle
# the goal is to get to a given coordinate
# there will be a way to record the decisions a player made so we can use this to compare it against the IBL model
# the obstacles are not at random location. 

import random as random    
import pygame as pygame # Installed pygame in order to create grid and game
import time # Having a timer to determine the arm or agent to reach to its location
import csv # Writing result to file

pygame.init()                                 #Start up the pygame
clock = pygame.time.Clock()                   #Needed for framerate not to sure
Screen = pygame.display.set_mode([250, 250])  #Making the window
Done = False                                  #Variable to keep track if window is open
MapSize = 10                                  #How many tiles in either direction of grid
DEFAULT_OUTPUT_FILE = "result.txt"            #Using file to record decision from player

TileWidth = 20                                #Pixel sizes for grid squares
TileHeight = 20
TileMargin = 4

BLACK = (0, 0, 0)                             #Some color definitions
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class MapTile(object):                       #The main class for stationary things that inhabit the grid (field, obstacles, and stuff).
    def __init__(self, Name, Column, Row):
        self.Name = Name
        self.Column = Column
        self.Row = Row


class Player(object):                    #Players can move around and can do cool stuff
    def __init__(self, Name, Column, Row):
        self.Name = Name
        self.Column = Column
        self.Row = Row
        
    def Move(self, Direction):              #This function is how a player moves around in a certain direction

        if Direction == "UP":
            if self.Row > 0:                #If within boundaries of grid
                if self.CollisionCheck("UP") == False:       #And nothing in the way
                   self.Row -= 1            #Go ahead and move

        elif Direction == "LEFT":
            if self.Column > 0:
                if self.CollisionCheck("LEFT") == False:
                    self.Column -= 1

        elif Direction == "RIGHT":
            if self.Column < MapSize-1:
                if self.CollisionCheck("RIGHT") == False:
                         self.Column += 1

        elif Direction == "DOWN":
            if self.Row < MapSize-1:
                if self.CollisionCheck("DOWN") == False:
                    self.Row += 1

        Map.update()       

    def CollisionCheck(self, Direction): #Checks if anything is on top of the field in the direction that the player wants to move 
                                         #(used in the move function)
        if Direction == "UP":
            if len(Map.Grid[self.Column][(self.Row)-1]) > 1:
                return True
        elif Direction == "LEFT":
            if len(Map.Grid[self.Column-1][(self.Row)]) > 1:
                return True
        elif Direction == "RIGHT":
            if len(Map.Grid[self.Column+1][(self.Row)]) > 1:
                return True
        elif Direction == "DOWN":
            if len(Map.Grid[self.Column][(self.Row)+1]) > 1:
                return True
        return False

    def Location(self):
        print("Coordinates: " + str(self.Column) + ", " + str(self.Row))


class Map(object):              #The main class where the action happens
    global MapSize

    Grid = []

    for Row in range(MapSize):     #Creating grid
        Grid.append([])
        for Column in range(MapSize):
            Grid[Row].append([])

    for Row in range(MapSize):     #Filling grid with field
        for Column in range(MapSize):
            TempTile = MapTile("Field", Column, Row)
            Grid[Column][Row].append(TempTile)
    
    for Row in range(MapSize):     #Placing lumber near edge on top
        for Column in range(1):
            TempTile = MapTile("Lumber", Column, Row)
            if Row == 0:
                Grid[Column][Row].append(TempTile)

    for Row in range(MapSize):     #Putting some obstacles near the top
        for Column in range(4):
            TempTile = MapTile("Obstacles", Column, Row)
            if Row == 4:
                Grid[Column][Row].append(TempTile)
            elif Row == 3 & Column == 3:
                Grid[Column][Row].append(TempTile)
    
    for Row in range(MapSize):     #Dropping Arm (Agent) in the bottom left corner
        for Column in range(1):
            Arm = Player("Arm", Column, Row)
            if Row == 8:
                Grid[Column][Row].append(Arm)
     
    def update(self):        #Very important function
                             #This function goes through the entire grid
                             #And checks to see if any object's internal coordinates
                             #Disagree with its current position in the grid
                             #If they do, it removes the objects and places it 
                             #On the grid according to its internal coordinates 

        for Column in range(MapSize):      
            for Row in range(MapSize):
                for i in range(len(Map.Grid[Column][Row])):
                    if Map.Grid[Column][Row][i].Column != Column:
                        Map.Grid[Column][Row].remove(Map.Grid[Column][Row][i])
                    elif Map.Grid[Column][Row][i].Name == "Arm":
                        Map.Grid[Column][Row].remove(Map.Grid[Column][Row][i])
        Map.Grid[int(Map.Arm.Column)][int(Map.Arm.Row)].append(Map.Arm)

Map = Map()

start_time = time.time() # starting time

while not Done:     #Main pygame loop
    
    elapsed_time = time.time() - start_time  # Getting elapsed time
    for event in pygame.event.get():         #Catching events
        if event.type == pygame.QUIT:
            Done = True       

        elif event.type == pygame.MOUSEBUTTONDOWN:
            Pos = pygame.mouse.get_pos()
            Column = Pos[0] // (TileWidth + TileMargin)  #Translating the position of the mouse into rows and columns
            Row = Pos[1] // (TileHeight + TileMargin)
            f = open(DEFAULT_OUTPUT_FILE, "a") 
            for i in range(len(Map.Grid[Column][Row])):
                #Printing out location on where the arm is at when mouse clicks anywhere on the grid
                print("\nRow: " + str(Row) + ", Column: " + str(Column) + ", Square: " + str(Map.Grid[Column][Row][i].Name))
                #Writing to file the path of the arm when moving around the grid while pushing the mouse button
                path = ("\nRow: " + str(Row) + ", Column: " + str(Column) + ", Square: " + str(Map.Grid[Column][Row][i].Name))
                f.write(path)
                    
        elif event.type == pygame.KEYDOWN:
            Pos = pygame.mouse.get_pos()
            Column = Pos[0] // (TileWidth + TileMargin) 
            Row = Pos[1] // (TileHeight + TileMargin)
            f = open(DEFAULT_OUTPUT_FILE, "a")       
            for i in range(len(Map.Grid[Column][Row])):
                #Writing to file the path of the arm when moving around the grid while pushing the key button
                path = ("\nRow: " + str(Map.Arm.Row) + ", Column: " + str(Map.Arm.Column) + ", Square: " + str(Map.Grid[Column][Row][i].Name))
                if event.key == pygame.K_LEFT:
                    Map.Arm.Move("LEFT")
                    f.write(path)
                    print(path) 
                if event.key == pygame.K_RIGHT:
                    Map.Arm.Move("RIGHT")
                    f.write(path)
                    print(path) 
                if event.key == pygame.K_UP:
                    Map.Arm.Move("UP")
                    f.write(path)
                    print(path)
                if event.key == pygame.K_DOWN:
                    Map.Arm.Move("DOWN")
                    f.write(path)
                    print(path)
            f.close()
                        
    Screen.fill(BLACK)

    for Row in range(MapSize):           #Drawing grid
        for Column in range(MapSize):
            for i in range(0, len(Map.Grid[Column][Row])):
                #if len(Map.Grid[Column][Row]) == 2:
                Color = WHITE
                if Map.Grid[Column][Row][i].Name == "Obstacles":
                    if(Map.Arm.Row == Row - 1 and Map.Arm.Column == Column) or (Map.Arm.Row == Row + 1 and Map.Arm.Column == Column) or (Map.Arm.Column == Column - 1 and Map.Arm.Row == Row) or (Map.Arm.Column == Column + 1 and Map.Arm.Row == Row):
                        Color = RED # This is obstacles
                    else:
                        Color = WHITE
                if Map.Grid[Column][Row][i].Name == "Lumber":
                    Color = BLUE
                if Map.Grid[Column][Row][i].Name == "Arm":
                    Color = GREEN


            pygame.draw.rect(Screen, Color, [(TileMargin + TileWidth) * Column + TileMargin,
                                             (TileMargin + TileHeight) * Row + TileMargin,
                                             TileWidth,
                                             TileHeight])

    clock.tick(60)      #Limit to 60 fps or something similiar

    pygame.display.flip()     #Need this (not sure what it is used for, it breaks if removed)
    Map.update()
    
pygame.quit()

print("\nThe time it took to reach lumber is: " + str(elapsed_time)) # Printing out timer
f = open(DEFAULT_OUTPUT_FILE, "a") 
total_timer = ("\nResult: " + str(elapsed_time)) # Having total timer when reaching lumber
f.write(total_timer) # Writing to file
f.close()
