from panda3d.core import Point3, Vec3
"""
This module defines a 3D Game of Life using Panda3D and PyQt6 for GUI elements.
Classes:
    GameOfLife3D: Main class for the 3D Game of Life, inheriting from ShowBase.
Functions:
    __init__(self): Initializes the game, sets up the grid, GUI elements, and tasks.
    ButtonSaveClicked(self): Handles the save button click event.
    ButtonLoadClicked(self): Handles the load button click event.
    buttonUpClicked(self): Moves the cursor up in the grid.
    buttonDownClicked(self): Moves the cursor down in the grid.
    buttonLeftClicked(self): Moves the cursor left in the grid.
    buttonRightClicked(self): Moves the cursor right in the grid.
    buttonForwardClicked(self): Moves the cursor forward in the grid.
    buttonBackwardClicked(self): Moves the cursor backward in the grid.
    buttonToggleClicked(self): Toggles the state of the cell at the cursor position.
    buttonClear(self): Clears the grid.
    buttonPopulation(self, value): Sets the population rate.
    buttonBirth(self, value): Sets the birth rate.
    buttonDeath(self, value): Sets the death rate.
    buttonStep(self): Advances the game by one step.
    buttonReset(self): Resets the grid to its initial state.
    buttonClicked(self): Toggles the running state of the game.
    ClearGrid(self): Returns a cleared grid.
    initialize_grid(self): Initializes the grid with random population.
    create_cubes(self): Creates cubes in the grid based on the current state.
    step(self): Advances the game by one step, updating the grid.
    update(self, Task): Updates the game state periodically.
    count_alive_neighbors(self, x, y, z): Counts the alive neighbors of a cell.
    update_cubes(self): Updates the cubes in the grid based on the current state.
    adjust_camera(self): Adjusts the camera position and orientation.
    random_population(self): Returns a random population value based on the population rate.
    openFileDialog(self): Opens a file dialog to load a file using PyQt.
    saveFileDialog(self): Opens a file dialog to save a file using PyQt.
"""
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
#import direct.directbase.DirectStart
#from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *

from panda3d.core import TextNode
from panda3d.core import ClockObject

from PyQt6.QtWidgets import QApplication, QFileDialog
import sys
import math 
import random
import sys
import json

class GameOfLife3D(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)  
        # Initialize PyQt application
        self.qt_app = QApplication.instance()
        if not self.qt_app:
            self.qt_app = QApplication(sys.argv)      
        self.grid_size = 10
        self.radius=self.grid_size*3
        self.cube_size = 0.5
        self.time_counter = 0
        self.update_rate = 10
        self.cursorX = 5
        self.cursorY = 5
        self.cursorZ = 5
        self.x = -30.0
        self.y = 7.96
        self.cursorpoint = Point3(self.cursorX, self.cursorY, self.cursorZ)
        self.birthrate = 3
        self.deathrate = 4
        self.aliverate = 2
        self.population_rate = 10
        self.sliderscale = 10
        self.tilt = 0
        self.population_rate = 0.7
        self.grid = self.ClearGrid()
        self.birthgrid = self.ClearGrid()
        self.cubes = []
        self.create_cubes()
        self.runlife=False
        bk_text = "This is my Demo"
        self.startbutton = DirectButton( text="Start", scale=0.1,  pos=(0.95, 0.96, 0.9), command=self.buttonClicked )
        self.stepbutton = DirectButton( text="Step", scale=0.1,  pos=(0.95, 0.96, 0.8), command=self.buttonStep )
        self.resetbutton = DirectButton( text="Reset", scale=0.1,  pos=(0.95, 0.96, 0.7), command=self.buttonReset )
        self.clearbutton = DirectButton( text="Clear", scale=0.1,  pos=(0.95, 0.96, 0.6), command=self.buttonClear)
        self.clearbutton = DirectButton( text="Load", scale=0.1,  pos=(0.95, 0.96, 0.5), command=self.ButtonLoadClicked )
        self.clearbutton = DirectButton( text="Save", scale=0.1,  pos=(0.95, 0.96, 0.4), command=self.ButtonSaveClicked )
        self.leftbutton = DirectButton( text="<-", scale=0.1,  pos=(0.85, 0.93, -0.6), command=self.buttonRightClicked )
        self.rightbutton = DirectButton( text="->", scale=0.1,  pos=(1.05, 0.96, -0.6), command=self.buttonLeftClicked ) 
        self.leftbutton = DirectButton( text="<-", scale=0.1,  pos=(0.85, 0.93, -0.7), command=self.buttonForwardClicked )
        self.rightbutton = DirectButton( text="->", scale=0.1,  pos=(1.05, 0.96, -0.7), command=self.buttonBackwardClicked ) 
        self.upbutton = DirectButton( text="^", scale=0.1,  pos=(0.95, 0.94, -0.55), command=self.buttonUpClicked ) 
        self.downbutton = DirectButton( text="v", scale=0.1,  pos=(0.95, 0.94, -0.7), command=self.buttonDownClicked )   
        self.togglebutton = DirectButton( text="x", scale=0.1,  pos=(0.95, 0.96, -0.6), command=self.buttonToggleClicked )    
        self.RotateLabel = DirectButton( text="Rotation", scale=0.07,  pos=(0.6, 0.96, -0.83), command=self.ButtonRotateClicked )    
        self.RotateSlider = DirectScrollBar(  range=(0,self.sliderscale), value=5,  scale=0.4, pos=(0.95, 0.95, -0.8), command=self.ButtonRotateClicked )
        self.TiltLabel = DirectButton( text="Tilt", scale=0.07,  pos=(0.6, 0.96, -0.93), command=self.ButtonRotateClicked )    
        self.TiltSlider = DirectScrollBar(  range=(-self.sliderscale,self.sliderscale), value=0,  scale=0.4, pos=(0.95, 0.95, -0.9), command=self.ButtonRotateClicked )
        self.optionbutton = DirectOptionMenu(text="options", scale=0.1, command=self.buttonClicked,
                        items=["glider", "pulsar", "blinker"], initialitem=2,  pos=(-0.95, 0.96, -0.5),
                        highlightColor=(0.65, 0.55, 0.65, 1))
        self.optionBirthbutton = DirectOptionMenu(text="birth", scale=0.1, command=self.buttonBirth, 
                                             items=["1","2", "3", "4","5","6","7","8","9"], initialitem="3",  
                                             pos=(-0.95, 0.96, -0.6), highlightColor=(0.65, 0.65, 0.65, 1))
        self.optionDeathbutton = DirectOptionMenu(text="death", scale=0.1, command=self.buttonDeath, 
                                             items=["1","2", "3", "4","5","6","7","8","9"], initialitem="4",  
                                             pos=(-0.95, 0.86, -0.7), highlightColor=(0.65, 0.65, 0.75, 1))
        self.optionAlivebutton = DirectOptionMenu(text="alive", scale=0.1, command=self.buttonAlive, 
                                             items=["1","2", "3", "4","5","6","7","8","9"], initialitem="2",   
                                             pos=(-0.95, 0.96, -0.8), 
                                             highlightColor=(0.65, 0.65, 0.85, 1))
        self.optionRatebutton = DirectOptionMenu(text="population", scale=0.1, command=self.buttonPopulation, 
                                             items=["5","10", "15", "50","100","150","250","400","750","1000"], 
                                             initialitem="10",  pos=(-0.95, 0.96, -0.87), 
                                             highlightColor=(0.65, 0.65, 0.88, 1)) 
        self.optionSizebutton = DirectOptionMenu(text="size", scale=0.1, command=self.buttonSize, 
                                             items=["10", "50","100","250","500","1000"], 
                                             initialitem="10",  pos=(-0.95, 0.96, -0.97), 
                                             highlightColor=(0.65, 0.65, 0.9, 1)) 
        
        self.optionSizebutton.set(str(self.grid_size))
        self.optionRatebutton.set(self.population_rate)
        self.optionAlivebutton.set(self.aliverate)      
        self.optionDeathbutton.set(self.deathrate)
        self.optionBirthbutton.set(self.birthrate)
        
        self.taskMgr.add(self.update, "update")
        self.adjust_camera()

    def ButtonRotateClicked(self):
        #print("Button Rotate clicked")
        #print(self.RotateSlider["value"])
        self.rotate = self.RotateSlider["value"]
        self.tilt = self.TiltSlider["value"]
        print(self.tilt)
        self.calculate_circle(self.rotate)
        self.adjust_camera()

    def calculate_circle(self, place):
        """
        Calculate the x and y coordinates of points on a circle.

        Args:
            radius (float): The radius of the circle.
            num_points (int): The number of points to calculate on the circle.

        Returns:
            list: A list of tuples containing the x and y coordinates of the points.
        """
        points = []
        
        angle = 2 * 3.14159 * place / self.sliderscale
        self.x = self.radius * math.cos(angle)
        self.y = self.radius * math.sin(angle)
        #print(self.x, self.y)


    def ButtonSaveClicked(self):
        """
        Handles the event when the save button is clicked.
        
        This method prints a message indicating that the save button was clicked
        and then calls the saveFileDialog method to open a save file dialog.
        """
        print("Button Save clicked")
        self.saveFileDialog()
        

    def ButtonLoadClicked(self):
        print("Button Load clicked")
        self.openFileDialog()
    
    def buttonUpClicked(self):
        print("Button Up clicked")
        self.cursorZ += 1
        self.cursorpoint = Point3(self.cursorX, self.cursorY, self.cursorZ)
        self.update_cubes()
    
    def buttonDownClicked(self):
        print("Button Down clicked")
        self.cursorZ -= 1
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
        self.cursorY += 1
        self.cursorpoint = Point3(self.cursorX, self.cursorY, self.cursorZ)
        self.update_cubes()

    def buttonBackwardClicked(self):
        print("Button Backward clicked")
        self.cursorY -= 1
        self.cursorpoint = Point3(self.cursorX, self.cursorY, self.cursorZ)
        self.update_cubes()

    def buttonToggleClicked(self):
        print("Button Toggle clicked")
        pos= f"{self.cursorX}-{self.cursorY}-{self.cursorZ}" 
        if pos in self.grid:
            if self.grid[pos] > 1:
                self.grid[pos] = 1
            self.grid[pos] = 1 - self.grid[pos]
        else:
            self.grid[pos] = 1
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

    def buttonAlive(self, value):
        print("Button Death clicked")
        print(value)
        self.aliverate = int(value)

    def buttonSize(self, value):
        print("Button Size clicked")
        print(value)
        self.grid_size = int(value)
        self.radius=self.grid_size*3
        self.grid = self.ClearGrid()
        self.update_cubes()
        self.adjust_camera()
        
    def buttonStep(self):  
        print("Button Step clicked")
        self.step()

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
        return {}

    
    def initialize_grid(self):
        return 

    def create_cubes(self):
        for ii,jj in self.grid.items():
            x,y,z=self.convert_string_to_grid(ii)
            cube = self.loader.loadModel("models/box")
            cube.setScale(self.cube_size)
            cube.setPos(Point3(x, y, z) * self.cube_size * 2)
            if jj == 1:
                cube.setColor(0, 1, 0, 1)  # Set cube color to green
            elif jj == -1:
                cube.setColor(1, 0, 0, 1)
            else:
                cube.setColor(0, 0, 1, 1)
            cube.reparentTo(self.render)
            self.cubes.append(cube)
        cursorcube = self.loader.loadModel("models/box")
        cursorcube.setScale(self.cube_size)
        cursorcube.setPos(self.cursorpoint * self.cube_size * 2)
        cursorcube.setColor(1, 1, 1, 1)  # Set cube color to white
        self.cursorcube = cursorcube
        cursorcube.reparentTo(self.render)

    def step(self):
        new_grid = self.ClearGrid()
        self.birthgrid = self.ClearGrid()
        for ii,jj in self.grid.items():
            x,y,z=self.convert_string_to_grid(ii)
            alive_neighbors = self.count_alive_neighbors(x, y, z, True)
            print(f"{x}-{y}-{z}",jj,alive_neighbors)
            if alive_neighbors>= self.aliverate and alive_neighbors < self.deathrate:
                new_grid[f"{int(x)}-{int(y)}-{int(z)}"] = jj+1
        for ii,jj in self.birthgrid.items():
            x,y,z=self.convert_string_to_grid(ii)
            if jj>= self.birthrate and jj < self.deathrate:
                new_grid[f"{int(x)}-{int(y)}-{int(z)}"] = 1
        self.grid = new_grid
        for ii,jj in self.grid.items():
            x,y,z=self.convert_string_to_grid(ii)
            if self.count_alive_neighbors(x, y, z) >= self.deathrate:
                self.grid[ii]=-1
        self.update_cubes()

    def update(self, Task):
        self.time_counter += 1
        if self.runlife and self.time_counter % self.update_rate == 0:
            self.step()
        return Task.cont

    def count_alive_neighbors(self, x, y, z,mature=False):
        directions = [Vec3(dx, dy, dz) for dx in [-1, 0, 1] for dy in [-1, 0, 1] for dz in [-1, 0, 1] if not (dx == dy == dz == 0)]
        count = 0
        for direction in directions:
            nx, ny, nz = x + direction.x, y + direction.y, z + direction.z
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and 0 <= nz < self.grid_size:
                grid_key = f"{int(nx)}-{int(ny)}-{int(nz)}"
                if grid_key in self.grid:
                    count += 1
                elif mature:
                    self.birthgrid[grid_key] = self.count_alive_neighbors(nx, ny, nz, False)
        return count

    def update_cubes(self):
        for cube in self.cubes:
            cube.removeNode()
        self.cursorcube.removeNode()
        self.cubes = []
        self.create_cubes()

    def adjust_camera(self):
        self.cam.setPos(self.x, self.y, self.tilt*3)
        self.cam.lookAt(Point3(self.grid_size / 2, 
                               self.grid_size / 2, 
                               self.grid_size / 2))
        
    def random_population(self):
        return int(random.uniform(0, 1) >= self.population_rate)
    
    def openFileDialog(self):
        # Open file dialog using PyQt
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "Choose a life file",
            "",
            "Life Files (*.lif);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    json_string = file.read()
                    # Update the display text
                    gridlist = json.loads(json_string)["grid"]
                    print(gridlist)
                    self.grid=self.ClearGrid()
                    for x,y,z in gridlist:
                        self.grid[f"{int(x)}-{int(y)}-{int(z)}"] = 1
                    self.update_cubes()
            except Exception as e:
                self.textDisplay.setText(f"Error reading file: {str(e)}")

    def convert_string_to_grid(self, grid_string):
        print(grid_string)
        grid_items = [int(i) for i in grid_string.split("-")]
        return grid_items[0], grid_items[1], grid_items[2]

    def saveFileDialog(self):
        # Open save file dialog using PyQt
        file_path, _ = QFileDialog.getSaveFileName(
            None,
            "Save life file",
            "",
            "Life Files (*.lif);;All Files (*)"
        )
        
        # Save the grid to the file
        gridlist = []

        for ii,jj in self.grid.items():
            x,y,z=self.convert_string_to_grid(ii)
            gridlist.append((x,y,z))
        json_string = json.dumps({"grid": gridlist})
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(json_string)
            except Exception as e:
                self.textDisplay.setText(f"Error saving file: {str(e)}")

game = GameOfLife3D()
game.run()