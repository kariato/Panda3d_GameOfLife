from panda3d.core import Point3, Vec3
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
#import direct.directbase.DirectStart
#from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *

from panda3d.core import TextNode
from panda3d.core import ClockObject

import random
import sys

class GameOfLife3D(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)        
        self.grid_size = 10
        self.cube_size = 0.5
        self.time_counter = 0
        self.update_rate = 10
        self.cursorX = 5
        self.cursorY = 5
        self.cursorZ = 5
        self.cursorpoint = Point3(self.cursorX, self.cursorY, self.cursorZ)
        self.birthrate = 2
        self.deathrate = 4
        self.population_rate = 0.7
        self.grid = self.initialize_grid()
        self.cubes = []
        self.create_cubes()
        self.runlife=False
        bk_text = "This is my Demo"
        self.startbutton = DirectButton( text="Start", scale=0.1,  pos=(0.95, 0.96, 0.9), command=self.buttonClicked )
        self.resetbutton = DirectButton( text="Reset", scale=0.1,  pos=(0.95, 0.96, 0.8), command=self.buttonReset )
        self.clearbutton = DirectButton( text="Clear", scale=0.1,  pos=(0.95, 0.96, 0.7), command=self.buttonClear)
        self.leftbutton = DirectButton( text="<-", scale=0.1,  pos=(0.85, 0.93, -0.6), command=self.buttonRightClicked )
        self.rightbutton = DirectButton( text="->", scale=0.1,  pos=(1.05, 0.96, -0.6), command=self.buttonLeftClicked ) 
        self.leftbutton = DirectButton( text="<-", scale=0.1,  pos=(0.85, 0.93, -0.7), command=self.buttonForwardClicked )
        self.rightbutton = DirectButton( text="->", scale=0.1,  pos=(1.05, 0.96, -0.7), command=self.buttonBackwardClicked ) 
        self.upbutton = DirectButton( text="^", scale=0.1,  pos=(0.95, 0.94, -0.55), command=self.buttonUpClicked ) 
        self.downbutton = DirectButton( text="v", scale=0.1,  pos=(0.95, 0.94, -0.7), command=self.buttonDownClicked )   
        self.togglebutton = DirectButton( text="x", scale=0.1,  pos=(0.95, 0.96, -0.6), command=self.buttonClicked )    
        self.togglebutton = DirectButton( text="Rotation", scale=0.07,  pos=(0.6, 0.96, -0.83), command=self.buttonClicked )    
        self.quitbutton = DirectScrollBar(  range=(0,10), value=5,  scale=0.4, pos=(0.95, 0.95, -0.8), command=self.buttonClicked )
        self.optionbutton = DirectOptionMenu(text="options", scale=0.1, command=self.buttonClicked,
                        items=["glider", "pulsar", "blinker"], initialitem=2,  pos=(-0.95, 0.96, -0.6),
                        highlightColor=(0.65, 0.55, 0.65, 1))
        self.optionbutton = DirectOptionMenu(text="birth", scale=0.1, command=self.buttonBirth, 
                                             items=["1","2", "3", "4","5","6","7","8","9"], initialitem=1,  
                                             pos=(-0.95, 0.96, -0.6), highlightColor=(0.65, 0.65, 0.65, 1))
        self.optionbutton = DirectOptionMenu(text="death", scale=0.1, command=self.buttonDeath, 
                                             items=["1","2", "3", "4","5","6","7","8","9"], initialitem=1,  
                                             pos=(-0.95, 0.86, -0.7), highlightColor=(0.65, 0.65, 0.75, 1))
        self.optionbutton = DirectOptionMenu(text="population", scale=0.1, command=self.buttonPopulation, 
                                             items=["0.1","0.2", "0.3", "0.4","0.5","0.6","0.7","0.8","0.9"], 
                                             initialitem=1,  pos=(-0.95, 0.96, -0.8), 
                                             highlightColor=(0.65, 0.65, 0.85, 1))
        
        
        
        self.taskMgr.add(self.update, "update")
        self.adjust_camera()
    
    def buttonUpClicked(self):
        print("Button Up clicked")
        self.cursorY += 1
        self.cursorpoint = Point3(self.cursorX, self.cursorY, self.cursorZ)
        self.update_cubes()
    
    def buttonDownClicked(self):
        print("Button Down clicked")
        self.cursorY -= 1
        self.cursorpoint = Point3(self.cursorX, self.cursorY, self.cursorZ)
        self.update_cubes()

    def buttonLeftClicked(self):
        print("Button Left clicked")
        self.cursorX -= 1
        self.cursorpoint = Point3(self.cursorX, self.cursorY, self.cursorZ)
        self.update_cubes()

    def buttonRightClicked(self):
        print("Button Right clicked")
        self.cursorX += 1
        self.cursorpoint = Point3(self.cursorX, self.cursorY, self.cursorZ)
        self.update_cubes()
    
    def buttonForwardClicked(self):
        print("Button Forward clicked")
        self.cursorZ += 1
        self.cursorpoint = Point3(self.cursorX, self.cursorY, self.cursorZ)
        self.update_cubes()

    def buttonBackwardClicked(self):
        print("Button Backward clicked")
        self.cursorZ -= 1
        self.cursorpoint = Point3(self.cursorX, self.cursorY, self.cursorZ)
        self.update_cubes()

    def buttonToggleClicked(self):
        print("Button Toggle clicked")
        self.grid[self.cursorX][self.cursorY][self.cursorZ] = 1 - self.grid[self.cursorX][self.cursorY][self.cursorZ]
        self.update_cubes()


    def buttonClear(self):
        print("Button Clear clicked")
        self.grid = self.ClearGrid()
        self.update_cubes()

    def buttonPopulation(self, value):  
        print("Button Population clicked")
        print(value)
        self.population_rate = float(value)

    def buttonBirth(self, value):
        print("Button Birth clicked")
        print(value)
        self.birthrate = int(value)
    
    def buttonDeath(self, value):
        print("Button Death clicked")
        print(value)
        self.deathrate = int(value)

    def buttonReset(self):  
        print("Button Reset clicked")
        self.grid = self.initialize_grid()
        self.update_cubes()

    def buttonClicked(self):
        self.runlife = not self.runlife
        self.startbutton["text"] = "Stop" if self.runlife else "Start"
        print("Button clicked")
        print(self.runlife)
    
    def ClearGrid(self):
        return [[[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)] for _ in range(self.grid_size)]

    
    def initialize_grid(self):
        return [[[self.random_population() for _ in range(self.grid_size)] for _ in range(self.grid_size)] for _ in range(self.grid_size)]

    def create_cubes(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                for z in range(self.grid_size):
                    if self.grid[x][y][z] == 1:
                        cube = self.loader.loadModel("models/box")
                        cube.setScale(self.cube_size)
                        cube.setPos(Point3(x, y, z) * self.cube_size * 2)
                        cube.setColor(1, 0, 0, 1)  # Set cube color to red
                        cube.reparentTo(self.render)
                        self.cubes.append(cube)
        cursorcube = self.loader.loadModel("models/box")
        cursorcube.setScale(self.cube_size)
        cursorcube.setPos(self.cursorpoint * self.cube_size * 2)
        cursorcube.setColor(0, 1, 0, 1)  # Set cube color to red
        self.cursorcube = cursorcube
        cursorcube.reparentTo(self.render)

    def update(self, Task):
        self.time_counter += 1
        if self.runlife and self.time_counter % self.update_rate == 0:
            new_grid = self.ClearGrid()
            for x in range(self.grid_size):
                for y in range(self.grid_size):
                    for z in range(self.grid_size):
                        alive_neighbors = self.count_alive_neighbors(x, y, z)
                        if self.grid[x][y][z] == 1:
                            if alive_neighbors < self.birthrate or alive_neighbors >= self.deathrate:
                                new_grid[x][y][z] = 0
                            else:
                                new_grid[x][y][z] = 1
                        else:
                            if alive_neighbors >= self.birthrate and alive_neighbors < self.deathrate:
                                new_grid[x][y][z] = 1
            self.grid = new_grid
            self.update_cubes()
        return Task.cont

    def count_alive_neighbors(self, x, y, z):
        directions = [Vec3(dx, dy, dz) for dx in [-1, 0, 1] for dy in [-1, 0, 1] for dz in [-1, 0, 1] if not (dx == dy == dz == 0)]
        count = 0
        for direction in directions:
            nx, ny, nz = x + direction.x, y + direction.y, z + direction.z
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and 0 <= nz < self.grid_size:
                count += self.grid[int(nx)][int(ny)][int(nz)]
        return count

    def update_cubes(self):
        for cube in self.cubes:
            cube.removeNode()
        self.cursorcube.removeNode()
        self.cubes = []
        self.create_cubes()

    def adjust_camera(self):
        self.cam.setPos(self.grid_size*3, self.grid_size*3, self.grid_size*3)
        self.cam.lookAt(Point3(self.grid_size / 2, 
                               self.grid_size / 2, 
                               self.grid_size / 2))
        
    def random_population(self):
        return int(random.uniform(0, 1) >= self.population_rate)

game = GameOfLife3D()
game.run()