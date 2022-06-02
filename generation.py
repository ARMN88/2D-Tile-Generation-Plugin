"""
- clean code
- turn to addon
"""

bl_info = {
    "name": "Tile Generation",
    "blender": (3, 1, 2),
    "category": "Object",
}

# Importing the library
import bpy
import math
import random
from bpy.props import *

# Variables
cells = []
collection = None

# Cell Class
class Cell:
  def __init__(self, x, y, tileNum):
    self.x = x
    self.y = y
    self.tileNum = tileNum
    self.mesh = None

    self.neighborLists = {
      "posX": [],
      "posY": [],
      "negX": [],
      "negY": []
    }

    self.sides = Cell.tiles[tileNum]

    for index in range(len(Cell.tiles)):
      tile = Cell.tiles[index]
      if self.sides["negX"] == tile["posX"]:
        self.neighborLists["negX"].append(index)
      if self.sides["negY"] == tile["posY"]:
        self.neighborLists["negY"].append(index)
      if self.sides["posX"] == tile["negX"]:
        self.neighborLists["posX"].append(index)
      if self.sides["posY"] == tile["negY"]:
        self.neighborLists["posY"].append(index)
      
  def draw(self):
    self.mesh = bpy.data.objects.new("Tile" + str(self.tileNum), blenderObjects[self.tileNum].data)
    bpy.data.collections["Tiles"].objects.link(self.mesh)
    self.mesh.location = (self.x, self.y, 0)
  size = 2
  tiles = [
    {"posX": 0, "negX": 0, "posY": 0, "negY": 0}, # 0
    {"posX": 0, "negX": 1, "posY": 0, "negY": 0}, # 1
    {"posX": 0, "negX": 0, "posY": 1, "negY": 0}, # 2
    {"posX": 1, "negX": 0, "posY": 0, "negY": 0}, # 3
    {"posX": 0, "negX": 0, "posY": 0, "negY": 1}, # 4
    {"posX": 1, "negX": 1, "posY": 0, "negY": 0}, # 5
    {"posX": 0, "negX": 0, "posY": 1, "negY": 1}, # 6
    {"posX": 0, "negX": 1, "posY": 1, "negY": 0}, # 7
    {"posX": 0, "negX": 1, "posY": 0, "negY": 1}, # 8
    {"posX": 1, "negX": 0, "posY": 0, "negY": 1}, # 9
    {"posX": 1, "negX": 0, "posY": 1, "negY": 0} # 10
  ]

def getDistance(x1, y1, x2, y2):
  return math.sqrt(
    (x2-x1) * (x2-x1) + 
    (y2-y1) * (y2-y1)
  )

def getNearestCells(a, b):
  global cells
  index = 0
  nearest = []
  for row in cells:
    for cell in row:
      if getDistance(cell.x, cell.y, a, b) == Cell.size:
        nearest.append(cell)
        index += 1
        if index >= 4:
          return nearest
  return nearest

def getDirection(x1, y1, x2, y2):
  distance = getDistance(x1, y1, x2, y2)
  normalizedVector = {
    "x": (x2-x1)/distance,
    "y": (y2-y1)/distance,
  }
  if normalizedVector["x"] == 0:
    if normalizedVector["y"] == 1:
      return "posY"
    elif normalizedVector["y"] == -1:
      return "negY"
  elif normalizedVector["y"] == 0:
    if normalizedVector["x"] == 1:
      return "posX"
    elif normalizedVector["x"] == -1:
      return "negX"
  return None
  
def randomGenerator(roomSize, whiteSpace):
  if "Tiles" not in bpy.data.collections:
    collection = bpy.data.collections.new("Tiles")
    bpy.context.scene.collection.children.link(collection)
  global cells
  cells = []
  for x in range(roomSize):
    cells.append([])
    for y in range(roomSize):
      # create cell position
      cellPos = {
        "x": ((x-roomSize/2)*Cell.size)+Cell.size/2,
        "y": ((y-roomSize/2)*Cell.size)+Cell.size/2
      }
      # pick random cell
      avaliable = list(range(len(Cell.tiles)))
      for _ in range(whiteSpace):
          avaliable.append(0)
      # add cell
      cells[x].append(Cell(cellPos["x"], cellPos["y"], random.choice(avaliable)))
      cells[x][y].draw()

# wave function collapse
def waveFunctionCollapseGenerator(roomSize, whiteSpace):
  if "Tiles" not in bpy.data.collections:
    collection = bpy.data.collections.new("Tiles")
    bpy.context.scene.collection.children.link(collection)
  global cells
  cells = []
  # create cells
  for x in range(roomSize):
    cells.append([])
    for y in range(roomSize):
      # create cell position
      cellPos = {
        "x": ((x-roomSize/2)*Cell.size)+Cell.size/2,
        "y": ((y-roomSize/2)*Cell.size)+Cell.size/2
      }
      # make avaliable list of all possible tiles
      avaliable = list(range(len(Cell.tiles)))
      removedCells = list(range(len(Cell.tiles)))
      # get neighbor cells
      nearestCells = getNearestCells(cellPos["x"], cellPos["y"])
      for nearCell in nearestCells:
        # get direction of neighbor
        dir = getDirection(nearCell.x, nearCell.y, cellPos["x"], cellPos["y"])
        # remove numbers that are not in the neighbor list
        for num in avaliable:
          if not (num in nearCell.neighborLists[dir]):
            removedCells.remove(num)
        avaliable = removedCells.copy()
      # add a cell with a random choice of the avaliable cells
      if 0 in avaliable:
        for _ in range(whiteSpace):
          avaliable.append(0)
      cells[x].append(Cell(cellPos["x"], cellPos["y"], random.choice(avaliable)))
      cells[x][y].draw()

# Wave Function Collapse #
class WaveFunctionCollapse(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "scene.wave_function_collapse"
    bl_label = "Wave Function Collapse Generator"
    bl_options = {"REGISTER", "UNDO"}
    
    # try hard min and hard max, or soft
    size : IntProperty(
      name = "Room Size",
      description = "Room dimensions",
      default = 6,
      min = 1
    )

    space : IntProperty(
      name = "Whitespace",
      description = "Amount of open area.",
      default = 1,
      min = 0,
      max = 15
    )

    def execute(self, context):
      waveFunctionCollapseGenerator(self.size, self.space)
      return {'FINISHED'}

# RANDOM #
class randomOps(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "scene.random_generator"
    bl_label = "Random Generator"
    bl_options = {"REGISTER", "UNDO"}
    
    # try hard min and hard max, or soft
    size : IntProperty(
    name = "Room Size",
    description = "Room dimensions",
    default = 5,
    min = 1
    )

    space : IntProperty(
      name = "Whitespace",
      description = "Amount of open area.",
      default = 1,
      min = 0,
      max = 15
    )

    def execute(self, context):
      randomGenerator(self.size, self.space)
      return {'FINISHED'}
  

def menu_func1(self, context):
    self.layout.operator(randomOps.bl_idname, text=randomOps.bl_label)

def register1():
    bpy.utils.register_class(randomOps)
    bpy.types.VIEW3D_MT_object.append(menu_func1)
  
def menu_func2(self, context):
    self.layout.operator(WaveFunctionCollapse.bl_idname, text=WaveFunctionCollapse.bl_label)

def register2():
    bpy.utils.register_class(WaveFunctionCollapse)
    bpy.types.VIEW3D_MT_object.append(menu_func2)

if __name__ == "__main__":
    if "Tiles" not in bpy.data.collections:
      collection = bpy.data.collections.new("Tiles")
      bpy.context.scene.collection.children.link(collection)

    blenderObjects = []

    for i in range(11):
      blenderObjects.append(bpy.data.collections["Assets"].objects["Tile."+str(i)])
      bpy.context.view_layer.objects.active = blenderObjects[4]
    register1()
    register2()
