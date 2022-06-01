# Importing the library
import bpy
import math
import random

# Variables
roomSize = 10
whiteSpace = 4
cells = []
collections = None

if "Tiles" in bpy.data.collections:
    collection = bpy.data.collections["Tiles"]
    for object in bpy.data.collections["Tiles"].objects:
        object.select_set(True)
    bpy.ops.object.delete()
else:
    collection = bpy.data.collections.new("Tiles")
    bpy.context.scene.collection.children.link(collection)

blenderObjects = []

for i in range(11):
    blenderObjects.append(bpy.data.collections["Assets"].objects["Tile."+str(i)])
bpy.context.view_layer.objects.active = blenderObjects[4]
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
    collection.objects.link(self.mesh)
    self.mesh.location = (self.x, self.y, 0)
  size = 2
  tiles = [
    {"posX": 0, "negX": 0, "posY": 0, "negY": 0}, # 0
    {"posX": 0, "negX": 0, "posY": 1, "negY": 0}, # 1
    {"posX": 1, "negX": 0, "posY": 0, "negY": 0}, # 2
    {"posX": 0, "negX": 0, "posY": 0, "negY": 1}, # 3
    {"posX": 0, "negX": 1, "posY": 0, "negY": 0}, # 4
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
  
def randomGenerator():
  global cells
  cells = []
  for x in range(roomSize):
    cells.append([])
    for y in range(roomSize):
      cells[x].append(Cell(x*Cell.size, y*Cell.size, random.randint(0, len(Cell.tiles)-1)))
      cells[x][y].draw()

# wave function collapse
def waveFunctionCollapseGenerator():
  global cells
  cells = []
  # create cells
  for x in range(roomSize):
    cells.append([])
    for y in range(roomSize):
      # make avaliable list of all possible tiles
      avaliable = list(range(len(Cell.tiles)))
      removedCells = list(range(len(Cell.tiles)))
      # get neighbor cells
      nearestCells = getNearestCells(x*Cell.size, y*Cell.size)
      for nearCell in nearestCells:
        # get direction of neighbor
        dir = getDirection(nearCell.x, nearCell.y, x*Cell.size, y*Cell.size)
        # remove numbers that are not in the neighbor list
        for num in avaliable:
          if not (num in nearCell.neighborLists[dir]):
            removedCells.remove(num)
        avaliable = removedCells.copy()
      # add a cell with a random choice of the avaliable cells
      if 0 in avaliable:
        for _ in range(whiteSpace):
          avaliable.append(0)
      cells[x].append(Cell(x*Cell.size, y*Cell.size, random.choice(avaliable)))
      cells[x][y].draw()

waveFunctionCollapseGenerator()
#randomGenerator()
