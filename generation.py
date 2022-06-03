# Addon Information
bl_info = {
    "name": "Tile Generator",
    "author": "ARMN88",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Object",
    "description": "Procedurally generates tiles.",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

# Importing the library
import bpy
import math
import random
from bpy.props import *
from bpy.types import (
  AddonPreferences,
  Operator,
  Panel,
  PropertyGroup
)

# Variables
cells = []
collection = None
blenderObjects = []

# Cell Class
class Cell:
  def __init__(self, x, y, tileNum):
    self.x = x
    self.y = y
    self.tileNum = tileNum
    self.mesh = None
    self.z = 0

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
    self.mesh = bpy.data.objects.new("Tile" + str(self.tileNum), bpy.data.collections["Assets"].objects["Tile."+str(self.tileNum)].data)
    bpy.data.collections["Tiles"].objects.link(self.mesh)
    self.mesh.location = (self.x, self.y, self.z)
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
  
# Random Generation Algorithm
def randomGenerator(roomSize, whiteSpace, offset):
  # Create Tiles Collection
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
        "x": (((x-roomSize/2)*Cell.size)+Cell.size/2)+offset[0],
        "y": (((y-roomSize/2)*Cell.size)+Cell.size/2)+offset[1]
      }
      # pick random cell
      avaliable = list(range(len(Cell.tiles)))
      for _ in range(whiteSpace):
          avaliable.append(0)
      # add cell
      cells[x].append(Cell(cellPos["x"], cellPos["y"], random.choice(avaliable)))
      cells[x][y].z = offset[2]
      cells[x][y].draw()

# Wave Function Collapse Algorithm
def waveFunctionCollapseGenerator(roomSize, whiteSpace, offset):
  # create cell position
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
        "x": (((x-roomSize/2)*Cell.size)+Cell.size/2)+offset[0],
        "y": (((y-roomSize/2)*Cell.size)+Cell.size/2)+offset[1]
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
      cells[x][y].z = offset[2]
      cells[x][y].draw()

# Random Generation Operator
class OBJECT_OT_random_generation(Operator):
    
    bl_label = "Random Generation"
    bl_idname = "object.random_generation"
    bl_description = "Procedurally generates tiles in a random fashion."
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"REGISTER", "UNDO"}
    
    size : IntProperty(
        name = "Size",
        default = 5,
        min = 1,
        description = "Area size of the generation."
    )
    
    space : IntProperty(
        name = "Open Space",
        default = 1,
        min = 0,
        description = "Amount of open area."
    )
    
    offset : FloatVectorProperty(
        name = "Generation Offset",
        default = (0.0, 0.0, 0.0)
    )

    def execute(self, context):
        randomGenerator(self.size, self.space, self.offset)
        return {"FINISHED"}
    
def random_generation_menu_func(self, context):
    self.layout.operator(OBJECT_OT_random_generation.bl_idname)

# Wave Function Collapse Operator
class OBJECT_OT_wave_function_collapse(Operator):
    
    bl_label = "Wave Function Collapse"
    bl_idname = "object.wave_function_collapse"
    bl_description = "Procedurally generates tiles using the wave function collapse algorithm."
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"REGISTER", "UNDO"}
    
    size : IntProperty(
        name = "Size",
        default = 5,
        min = 1,
        description = "Area size of the generation."
    )
    
    space : IntProperty(
        name = "Open Space",
        default = 1,
        min = 0,
        description = "Amount of open area."
    )
    
    offset : FloatVectorProperty(
        name = "Generation Offset",
        default = (0.0, 0.0, 0.0)
    )

    def execute(self, context):
        waveFunctionCollapseGenerator(self.size, self.space, self.offset)
        return {"FINISHED"}
    
def wave_function_collapse_menu_func(self,context):
    self.layout.operator(OBJECT_OT_wave_function_collapse.bl_idname)
    
def register():
    bpy.utils.register_class(OBJECT_OT_random_generation)
    bpy.types.VIEW3D_MT_object.append(random_generation_menu_func)
    bpy.utils.register_class(OBJECT_OT_wave_function_collapse)
    bpy.types.VIEW3D_MT_object.append(wave_function_collapse_menu_func)
    
def unregister():
    bpy.utils.unregister_class(OBJECT_OT_random_generation)
    bpy.types.VIEW3D_MT_object.remove(random_generation_menu_func)
    bpy.utils.unregister_class(OBJECT_OT_wave_function_collapse)
    bpy.types.VIEW3D_MT_object.remove(wave_function_collapse_menu_func)
    
if __name__ == "__main__":
    register()
