# <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Blender_logo_no_text.svg/939px-Blender_logo_no_text.svg.png" height="30vh"> Blender Tile Generation Addon
An addon for Blender that allows users to procedurally create tile based maps. You can download the [blender file](https://github.com/ARMN88/2D-Tile-Generation-Plugin/archive/refs/heads/main.zip) attached, or follow the steps below to create your own setup.

## How To Use
### Import The Addon
Download `generation.py`. Open your Blender file, and go to `Edit > Preferences > Addons > Install`. Import `generation.py`.

### Create Tiles
This is a very crucial part that can be easily messed up. You will need to create 11 different tiles in a specific order with a specific shape and orientation. You will need to create 4 different tiles, show below. Yellow represents a wall. **Be sure to make your walls half of a normal wall, as the generators will put two tiles together, creating a full wall.**

### Run The Algorithm
After creating your tiles, go to `Object` in the upper right hand corner of the viewport. At the bottom, you will see two generators. Select one, and it will generate a map using its corresponding method. Immediately after generating, you will see a panel in the bottom left corner of the viewport. This will allow you to change the generation to your liking. All generated tiles will be added to a new collection called `Tiles`.

## Contact
Contact me using the methods below if you encounter an error or have questions.

Discord: ARMN88#8281 \
Email: 250189@d230.org
