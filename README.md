
# Weight-and-Color
blender addon to convert weight paint to/from vertex color could be useful for external editing.

Note from Neop: This plugin works with Blender 3.0 now, versions before that don't seem to load it. The original code works up to 2.79.

install the addon :
 
- Download the Zip file
- Extract and move the .py file to your addon directory

Using the Addon :

![how to use](http://i.stack.imgur.com/iE5Nr.gif)

- Select the objec t of interest
- Hit <kbd>Space</kbd> and type "weight & color"
- choose th right setting from what follows :

- select the conversion you want to do :
 
   * Weight paint to Vertex color.
   * Vertex color to Weight paint.

- Select Color conversin method :
  - RGB : convert colored vertex color to/from wheight paint
  - B&W : convert a grayscale Vertex color to/from Weght paint
- Use Zero weight :
  - include the verticies that have a zero weight in the vertex groups
  
- A new Vertex color/group will be created with the same name as the old one
