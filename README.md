# <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Blender_logo_no_text.svg/939px-Blender_logo_no_text.svg.png" height="30vh"> Blender Tile Generation Addon
An addon for Blender that allows users to procedurally create tile based maps. You can download the [blender file](https://github.com/ARMN88/2D-Tile-Generation-Plugin/archive/refs/heads/main.zip) attached, or follow the steps below to create your own setup.

## How To Use
### Import The Addon
Download `generation.py`. Open your Blender file, and go to `Edit > Preferences > Addons > Install`. Import `generation.py`.

### Create Tiles
This is a very crucial part that can be easily messed up. You will need to create 11 different tiles in a specific order with a specific shape and orientation. You will need to create 4 different tiles, show below. Yellow represents a wall. **Be sure to make your walls half of a normal wall, as the generators will put two tiles together, creating a full wall.** Front means positive Y, back means negative Y, right means position X, left means negative X. Make 1 floor, rename it to `Tile.000`. When you crate a new tile, copy the previous tile. This will help you later when you have to name the tiles.

**Tiles (in order):**
- An empty space: <img src="https://lh3.googleusercontent.com/d/1tHOqRCMh4RSiRcEiRpEys_RQuQsqlCcV" align="center" height="30vh">
- One Wall Tile (wall to the left): <img src="https://lh3.googleusercontent.com/d/1dP2B2xDiFpB6WmclFfbOWRucZMgVlodN" align="center" height="30vh">
- One Wall Tile (wall to the front): <img src="https://lh3.googleusercontent.com/d/1l6m99_Rd7_X9tA_V8zVNPWODkp_PI47D" align="center" height="30vh">
- One Wall Tile (wall to the back): <img src="https://lh3.googleusercontent.com/d/1zvNQTM449x9f_zCvzzgYQ8Z6PoDzmBnE" align="center" height="30vh">
- One Wall Tile (wall to the right): <img src="https://lh3.googleusercontent.com/d/1A_bQrdtIrURMlVeokBzeyrKkn0GHU_Tb" align="center" height="30vh">
- Parallel Wall Tile (walls on right and left): <img src="https://lh3.googleusercontent.com/d/1XUjgFPi0yvEfDaobO6KMbHLotG5oL3Hn" align="center" height="30vh">
- Parallel Wall Tile (walls on front and back): <img src="https://lh3.googleusercontent.com/d/1qh0vuzp3lniH1F7vO06cZ4oOnEKZpLRX" align="center" height="30vh">
- Two Wall Tile (walls front and left): <img src="https://lh3.googleusercontent.com/d/1TugdnOUbyGLLZBspucMxJ8yHjiQDICF0" align="center" height="30vh">
- Two Wall Tile (walls back and left): <img src="https://lh3.googleusercontent.com/d/1FxYCGy0cB-q8u4uPhynRxP0NK8ZEKmSv" align="center" height="30vh">
- Two Wall Tile (walls back and right): <img src="https://lh3.googleusercontent.com/d/16HZK_xkDMKSns-Yr7o0awZMX660KORbs" align="center" height="30vh">
- Two Wall Tile (walls front and right): <img src="https://lh3.googleusercontent.com/d/1N1_CV2IEpuZuim4iy4fKfxQJIJ8oVNWe" align="center" height="30vh">

After creating your tiles, hit `Ctrl + A` and select `Rotation and Scale`. Also be sure the tile is one object (join the meshes of the wall, ceiling, and tile). Now you will name them. Each tile is named `Tile.` with the number after it. For example, the tiles (in order) will go: `Tile.0`, `Tile.1`, `Tile.2`, `Tile.3`, `Tile.4`, `Tile.5`, `Tile.6`, `Tile.7`, `Tile.8`, `Tile.9`, and `Tile.10`.

Lastly, make a new Collection, and name it `Assets`. Put all your tiles in the collection. You're done!

### Run The Algorithm
After creating your tiles, go to `Object` in the upper right hand corner of the viewport. At the bottom, you will see two generators. Select one, and it will generate a map using its corresponding method. Immediately after generating, you will see a panel in the bottom left corner of the viewport. This will allow you to change the generation to your liking. All generated tiles will be added to a new collection called `Tiles`.

## Contact
Contact me using the methods below if you encounter an error or have questions.

Discord: ARMN88#8281 \
Email: 250189@d230.org
