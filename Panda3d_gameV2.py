from panda3d.core import Point3, Vec3
"""

This module defines a 3D Game of Life using Panda3D and PyQt6 for GUI elements.
Classes:
    GameOfLife3D: Main class for the 3D Game of Life, inheriting from ShowBase.


"""
from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from direct.gui.DirectGui import *
from random import randrange
from panda3d.core import TextNode
from panda3d.core import ClockObject

from PyQt6.QtWidgets import QApplication, QFileDialog
import sys
import math 
import random
import sys
import json
import os

class GameOfLife3D(ShowBase):
    """
    This module defines a 3D Game of Life using Panda3D and PyQt6 for GUI elements.
    Classes:
    GameOfLife3D: Main class for the 3D Game of Life, inheriting from ShowBase.
    A 3D implementation of Conway's Game of Life using Panda3D and PyQt.
    Attributes:
        qt_app (QApplication): The PyQt application instance.
        grid_size (int): The size of the grid.
        radius (int): The radius of the grid.
        cube_size (float): The size of each cube in the grid.
        time_counter (int): A counter to keep track of time.
        update_rate (int): The rate at which the grid updates.
        cursorX (int): The X coordinate of the cursor.
        cursorY (int): The Y coordinate of the cursor.
        cursorZ (int): The Z coordinate of the cursor.
        x (float): The X coordinate of the camera.
        y (float): The Y coordinate of the camera.
        cursorpoint (Point3): The position of the cursor.
        birthrate (int): The birth rate for the game.
        deathrate (int): The death rate for the game.
        aliverate (int): The alive rate for the game.
        population_rate (int): The population rate for the game.
        sliderscale (int): The scale of the sliders.
        tilt (int): The tilt of the camera.
        grid (dict): The grid representing the game state.
        birthgrid (dict): The grid representing the birth state.
        cubes (list): A list of cubes in the grid.
        runlife (bool): A flag to indicate if the game is running.
        startbutton (DirectButton): The start button.
        stepbutton (DirectButton): The step button.
        resetbutton (DirectButton): The reset button.
        clearbutton (DirectButton): The clear button.
        leftbutton (DirectButton): The left button.
        rightbutton (DirectButton): The right button.
        upbutton (DirectButton): The up button.
        downbutton (DirectButton): The down button.
        togglebutton (DirectButton): The toggle button.
        RotateLabel (DirectButton): The rotation label.
        RotateSlider (DirectScrollBar): The rotation slider.
        TiltLabel (DirectButton): The tilt label.
        TiltSlider (DirectScrollBar): The tilt slider.
        optionbutton (DirectOptionMenu): The options menu.
        optionBirthbutton (DirectOptionMenu): The birth options menu.
        optionDeathbutton (DirectOptionMenu): The death options menu.
        optionAlivebutton (DirectOptionMenu): The alive options menu.
        optionRatebutton (DirectOptionMenu): The population rate options menu.
        optionSizebutton (DirectOptionMenu): The size options menu.
        TiltLabel (dict): A dictionary of tilt labels.
        taskMgr (TaskManager): The task manager for updating the game.
        cam (Camera): The camera for viewing the game.
        cursorcube (NodePath): The cube representing the cursor.
    Methods:
        __init__(): Initializes the GameOfLife3D instance.
        buttonOptionClicked(value): Handles the event when an option button is clicked.
        ButtonNothingClicked(): Handles the event when a button with no action is clicked.
        find_lif_files(directory): Finds .lif files in the specified directory.
        ButtonRotateClicked(): Handles the event when the rotate button is clicked.
        calculate_circle(place): Calculates the x and y coordinates of points on a circle.
        ButtonSaveClicked(): Handles the event when the save button is clicked.
        ButtonLoadClicked(): Handles the event when the load button is clicked.
        buttonUpClicked(): Handles the event when the up button is clicked.
        buttonDownClicked(): Handles the event when the down button is clicked.
        buttonLeftClicked(): Handles the event when the left button is clicked.
        buttonRightClicked(): Handles the event when the right button is clicked.
        buttonForwardClicked(): Handles the event when the forward button is clicked.
        buttonBackwardClicked(): Handles the event when the backward button is clicked.
        buttonToggleClicked(): Handles the event when the toggle button is clicked.
        buttonClear(): Handles the event when the clear button is clicked.
        buttonPopulation(value): Handles the event when the population button is clicked.
        buttonBirth(value): Handles the event when the birth button is clicked.
        buttonDeath(value): Handles the event when the death button is clicked.
        buttonAlive(value): Handles the event when the alive button is clicked.
        buttonSize(value): Handles the event when the size button is clicked.
        buttonStep(): Handles the event when the step button is clicked.
        buttonReset(): Handles the event when the reset button is clicked.
        buttonClicked(): Handles the event when the start/stop button is clicked.
        ClearGrid(): Clears the grid.
        initialize_grid(): Initializes the grid.
        create_cubes(): Creates the cubes in the grid.
        step(): Advances the game by one step.
        update(Task): Updates the game state.
        count_alive_neighbors(x, y, z, mature=False): Counts the alive neighbors of a cell.
        update_cubes(): Updates the cubes in the grid.
        adjust_camera(): Adjusts the camera position.
        openFileDialog(): Opens a file dialog to load a .lif file.
        convert_string_to_grid(grid_string): Converts a grid string to coordinates.
        saveFileDialog(): Opens a file dialog to save a .lif file.
    """

    def __init__(self):
        """
        Initializes the GameOfLife3D instance.
        """
        ShowBase.__init__(self)  # Initialize the ShowBase class
        # Initialize PyQt application
        self.qt_app = QApplication.instance()
        if not self.qt_app:
            self.qt_app = QApplication(sys.argv)      
        self.grid_size = 10
        self.radius=self.grid_size*3
        self.cube_size = 0.5
        self.time_counter = 0
        self.update_rate = 10
        self.cursorX = self.grid_size // 2
        self.cursorY = self.grid_size // 2
        self.cursorZ = self.grid_size // 2
        self.x = -30.0
        self.y = 7.96
        self.cursorpoint = Point3(self.cursorX, self.cursorY, self.cursorZ)
        self.birthrate = 3
        self.deathrate = 4
        self.aliverate = 2
        self.population_rate = 10
        self.sliderscale = 10
        self.tilt = 0
        self.grid = self.ClearGrid()
        self.birthgrid = self.ClearGrid()
        self.cubes = []
        self.create_cubes()
        self.runlife=False

        # Get library of shapes
        current_directory = os.path.dirname(os.path.abspath(__file__))
        lif_files = self.find_lif_files(current_directory)
        print("LIF files in current directory:", lif_files)

        # Create GUI elements using DirectGui
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
        self.optionbutton = DirectOptionMenu(text="options", scale=0.1, command=self.buttonOptionClicked,
                        items=lif_files, initialitem=0,  pos=(-0.95, 0.96, -0.5),
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
                                             items=["10", "20","30","50","100","500","1000"], 
                                             initialitem="10",  pos=(-0.95, 0.96, -0.97), 
                                             highlightColor=(0.65, 0.65, 0.9, 1)) 
        self.TiltLabel={}
        labels=["Presets","Birth","Death","Alive","Population","Size"]
        for i in range(0,len(labels)):
            self.TiltLabel[i] = DirectButton( text=labels[i], scale=0.07,
                                               
                                             pos=(-1.15, 0.96, -0.5-i*0.095), command=self.ButtonNothingClicked)
        
        self.optionSizebutton.set(str(self.grid_size))
        self.optionRatebutton.set(str(self.population_rate))
        self.optionAlivebutton.set(self.aliverate)      
        self.optionDeathbutton.set(self.deathrate)
        self.optionBirthbutton.set(self.birthrate)
        
        # Set up the task manager in Pandas Game Engine
        self.taskMgr.add(self.update, "update")
        # Set up the camera
        self.adjust_camera()

    def buttonOptionClicked(self, value):
        # Handle the event when an option button is clicked
        # Loads a .lif file passed in the dropped down and updates the grid
        print("Button Option clicked")
        print(value)
        self.grid = self.ClearGrid()
        with open(value+'.lif', 'r', encoding='utf-8') as file:
            json_string = file.read()
            # Update the display text
            gridlist = json.loads(json_string)["grid"]
            print(gridlist)
            self.grid=self.ClearGrid()
            for x,y,z in gridlist:
                self.grid[f"{int(x)}-{int(y)}-{int(z)}"] = 1
            self.update_cubes()

    def ButtonNothingClicked(self):
        # Handle the event when a button with no action is clicked
        # Label and others that do nothing
        print("Button Nothing clicked")

    def find_lif_files(self,directory):
        # Find .lif files in the specified directory to load into dropdown
        lif_files = [f[:-4] for f in os.listdir(directory) if f.endswith('.lif')]
        return lif_files


    def ButtonRotateClicked(self):
        # Handle the event when the rotate button is clicked
        # This rotates the camera based on the slider value
        #print("Button Rotate clicked")
        #print(self.RotateSlider["value"])
        self.rotate = self.RotateSlider["value"]
        self.tilt = self.TiltSlider["value"]
        #print(self.tilt)
        self.calculate_circle(self.rotate)
        self.adjust_camera()

    def calculate_circle(self, place):
        # Calculate the x and y coordinates of points on a circle
        # based on the place on the slider to rotate the camera
        points = []
        
        angle = 2 * 3.14159 * place / self.sliderscale
        self.x = self.radius * math.cos(angle)
        self.y = self.radius * math.sin(angle)


    def ButtonSaveClicked(self):
        # Handle the event when the save button is clicked
        # This calls the saveFileDialog method to open a file dialog
        # to save a .lif file with the current grid
        print("Button Save clicked")
        self.saveFileDialog()
        

    def ButtonLoadClicked(self):
        # Handle the event when the load button is clicked
        # This calls the openFileDialog method to open a file dialog
        # to load a .lif file
        # Then updates the grid with the loaded file
        print("Button Load clicked")
        self.openFileDialog()
    
    def buttonUpClicked(self):
        # Handle the event when the up button is clicked
        # This moves the cursor up
        print("Button Up clicked")
        self.cursorZ += 1
        self.cursorpoint = Point3(self.cursorX, self.cursorY, self.cursorZ)
        self.update_cubes()
    
    def buttonDownClicked(self):
        # Handle the event when the down button is clicked
        # This moves the cursor down
        print("Button Down clicked")
        self.cursorZ -= 1
        self.cursorpoint = Point3(self.cursorX, self.cursorY, self.cursorZ)
        self.update_cubes()

    def buttonLeftClicked(self):
        # Handle the event when the left button is clicked
        # This moves the cursor to the left
        print("Button Left clicked")
        self.cursorX -= 1
        self.cursorpoint = Point3(self.cursorX, self.cursorY, self.cursorZ)
        self.update_cubes()

    def buttonRightClicked(self):
        # Handle the event when the right button is clicked
        # This moves the cursor to the right
        print("Button Right clicked")
        self.cursorX += 1
        self.cursorpoint = Point3(self.cursorX, self.cursorY, self.cursorZ)
        self.update_cubes()
    
    def buttonForwardClicked(self):
        # Handle the event when the forward button is clicked
        # This moves the cursor forward
        print("Button Forward clicked")
        self.cursorY += 1
        self.cursorpoint = Point3(self.cursorX, self.cursorY, self.cursorZ)
        self.update_cubes()

    def buttonBackwardClicked(self):
        # Handle the event when the backward button is clicked
        # This moves the cursor backward        
        print("Button Backward clicked")
        self.cursorY -= 1
        self.cursorpoint = Point3(self.cursorX, self.cursorY, self.cursorZ)
        self.update_cubes()

    def buttonToggleClicked(self):
        # Handle the event when the toggle button is clicked
        # This toggles the state of the cube at the cursor position
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
        # Handle the event when the clear button is clicked
        # This clears the grid
        # The update the display
        print("Button Clear clicked")
        self.grid = self.ClearGrid()
        self.update_cubes()

    def buttonPopulation(self, value): 
        # Handle the event when the population button is clicked
        # This sets the population of cubes generated if the rest button is clicked
        print("Button Population clicked")
        print(value)
        self.population_rate = int(value)

    def buttonBirth(self, value):
        # Handle the event when the birth button is clicked
        # This sets the birth rate for the game
        print("Button Birth clicked")
        print(value)
        self.birthrate = int(value)
    
    def buttonDeath(self, value):
        # Handle the event when the death button is clicked
        # This sets the death rate for the game
        print("Button Death clicked")
        print(value)
        self.deathrate = int(value)

    def buttonAlive(self, value):
        # Handle the event when the alive button is clicked
        # This sets the alive rate for the game
        print("Button Alive clicked")
        print(value)
        self.aliverate = int(value)

    def buttonSize(self, value):
        # Handle the event when the size button is clicked
        # This sets the size of the grid
        # The update the display and camera and cursor position
        print("Button Size clicked")
        print(value)
        self.grid_size = int(value)
        self.radius=self.grid_size*3
        self.cursorX = self.grid_size // 2
        self.cursorY = self.grid_size // 2
        self.cursorZ = self.grid_size // 2
        self.grid = self.ClearGrid()
        self.update_cubes()
        self.adjust_camera()
        
    def buttonStep(self):  
        # Handle the event when the step button is clicked
        # This advances the game by one step
        print("Button Step clicked")
        self.step()

    def buttonReset(self):  
        # Handle the event when the reset button is clicked
        # This resets the grid to a random state based on the population rate
        print("Button Reset clicked")
        self.grid = self.initialize_grid()
        for i in range(self.population_rate):
            self.grid[f"{randrange(self.grid_size)}-{randrange(self.grid_size)}-{randrange(self.grid_size)}"]=1
        self.update_cubes()

    def buttonClicked(self):
        # Handle the event when the start/stop button is clicked
        # This run the model until the button is clicked again 
        self.runlife = not self.runlife
        self.startbutton["text"] = "Stop" if self.runlife else "Start"
        print("Button clicked")
        print(self.runlife)
    
    def ClearGrid(self):
        # Clear the grid by create a new empty dictionary
        return {}

    
    def initialize_grid(self):
        # Initialize the grid by creating a new empty dictionary
        return {}

    def create_cubes(self):
        # Create the cubes in the grid
        # This creates a cube for each cell in the grid dictionary
        for ii,jj in self.grid.items():
            # Convert the grid string (dictionary key) to coordinates
            x,y,z=self.convert_string_to_grid(ii)
            # Create a cube at the coordinates
            cube = self.loader.loadModel("models/box")
            cube.setScale(self.cube_size)
            cube.setPos(Point3(x, y, z) * self.cube_size * 2)
            # Set the color of the cube based on the value in the grid
            # 1 is alive, -1 is dead next cycle. greater than 1 is alive and mature
            if jj == 1:
                cube.setColor(0, 1, 0, 1)  # Set cube color to green
            elif jj == -1:
                cube.setColor(1, 0, 0, 1)
            else:
                cube.setColor(0, 0, 1, 1)
            # add the cube to the render engine
            cube.reparentTo(self.render)
            self.cubes.append(cube)
        # Create a cursor cube at the cursor position            
        cursorcube = self.loader.loadModel("models/box")
        cursorcube.setScale(self.cube_size)
        cursorcube.setPos(self.cursorpoint * self.cube_size * 2)
        cursorcube.setColor(1, 1, 1, 1)  # Set cube color to white
        self.cursorcube = cursorcube
        cursorcube.reparentTo(self.render)

    def step(self):
        # Advance the game by one step
        new_grid = self.ClearGrid()
        # create a grid of possible new births
        self.birthgrid = self.ClearGrid()
        # loop through the grid dictionary update the state of each cell by the rules of the game 
        # which is the number of alive neighbors
        for ii,jj in self.grid.items():
            # Convert the grid string (dictionary key) to coordinates
            x,y,z=self.convert_string_to_grid(ii)
            # Count the number of alive neighbors for the cell
            alive_neighbors = self.count_alive_neighbors(x, y, z, True)
            #print(f"{x}-{y}-{z}",jj,alive_neighbors)
            # If the cell is alive and has the right number of alive neighbors, keep it alive
            if alive_neighbors>= self.aliverate and alive_neighbors < self.deathrate:
                new_grid[f"{int(x)}-{int(y)}-{int(z)}"] = jj+1

        # loop through the birthgrid dictionary update the state of each cell by the rules of the game
        for ii,jj in self.birthgrid.items():
            # Convert the grid string (dictionary key) to coordinates
            x,y,z=self.convert_string_to_grid(ii)
            # Check the number of alive neighbors for the cell to see if it should be born         
            if jj>= self.birthrate and jj < self.deathrate:
                new_grid[f"{int(x)}-{int(y)}-{int(z)}"] = 1

        # Update the grid with the new state        
        self.grid = new_grid

        # loop through the grid dictionary to check if any cells should die next cycle
        for ii,jj in self.grid.items():
            x,y,z=self.convert_string_to_grid(ii)
            if self.count_alive_neighbors(x, y, z) >= self.deathrate:
                self.grid[ii]=-1

        # Update the display
        self.update_cubes()

    def update(self, Task):
        # Since the frame rate is much higher than the update rate, we need to keep track of time so that we can update the game at the correct
        # rate. We do this by incrementing the time counter and checking if it is time to update the game.
        self.time_counter += 1
        if self.runlife and self.time_counter % self.update_rate == 0:
            self.step()
        return Task.cont

    def count_alive_neighbors(self, x, y, z,mature=False):
        # Count the number of alive neighbors for a cell
        # This checks the 26 neighbors of the cell in the grid
        # and returns the number of alive neighbors
        # If mature is True, it also checks if the neighbors so we keep track of possibe birth locations
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
        # Update the cubes in the game engine
        for cube in self.cubes:
            cube.removeNode()
        self.cursorcube.removeNode()
        self.cubes = []
        self.create_cubes()

    def adjust_camera(self):
        # Adjust the camera position based upon the grid size and direction of the rotation
        self.cam.setPos(self.x, self.y, self.tilt*3)
        self.cam.lookAt(Point3(self.grid_size / 2, 
                               self.grid_size / 2, 
                               self.grid_size / 2))
        
    
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
        #print(grid_string)
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

# Create an instance of the GameOfLife3D class and run the game
game = GameOfLife3D()
game.run()