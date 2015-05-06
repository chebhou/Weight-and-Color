# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    "name": "Modifiers Linker",
    "author": "Chebhou",
    "version": (1, 0),
    "blender": (2, 74, 0),
    "location": "Space bar -> \"weight & color\" ",
    "description": "convert weight paint to/from vertex color",
    "category": "Object",
}

import bpy
from bpy.types import Operator
from bpy.props import EnumProperty, BoolProperty
from mathutils import Color


S = scene   = bpy.context.scene
C = context = bpy.context
D = data    = bpy.data
O = ops     = bpy.ops

obj = bpy.context.active_object
obj_data = obj.data

def convert(value, method):
    if method == 'BW2W':
        return  (value.r + value.g+ value.b)/3
    elif method == 'W2BW':
        col = Color((value, value, value))
        return col
    elif method == 'HSV2W':
        return  1-(value.h / 0.66)
    elif method == 'W2HSV':
        col = Color()
        col.hsv = (0.66*(1-value), 1, 1)
        return  col

          
def vert_col2weight(color,zero_weight):    
    color_maps = obj_data.vertex_colors
    for color_map in color_maps :
        group_name = color_map.name
        
        #check for existing group with the same name
        if None == obj.vertex_groups.get(group_name): 
            obj.vertex_groups.new( name = group_name)  
            
        group_ind = obj.vertex_groups[group_name].index

        for poly in obj_data.polygons:
                    for loop_ind in poly.loop_indices:
                        vert_ind =obj_data.loops[loop_ind].vertex_index  
                        col = color_map.data[loop_ind].color
                        if color == 'BW':
                            weight = convert(col, 'BW2W')
                        else :
                            weight = convert(col, 'HSV2W')
                            
                        if zero_weight or (weight != 0):
                            obj.vertex_groups[group_ind].add([vert_ind], weight,'REPLACE')

                                       
def weight2vert_col(color):               
    vert_groups = obj.vertex_groups
    col = Color()
    for vert_g in vert_groups:
        group_name = vert_g.name  
        
        #check for existing group with the same name
        if None == obj_data.vertex_colors.get(group_name): 
            obj_data.vertex_colors.new(name=group_name)
        
        color_map =  obj_data.vertex_colors[group_name]
        
        for poly in obj_data.polygons:
                    for loop_ind in poly.loop_indices:
                        vert_ind =obj_data.loops[loop_ind].vertex_index 
                        
                        #check if the vertex belong to the group
                        weight = 0
                        for g in obj_data.vertices[vert_ind].groups:
                            if g.group == vert_groups[group_name].index:
                                weight = vert_groups[group_name].weight(vert_ind) 
                                     
                        #convert weight to vert_col          
                        if color == 'BW':
                            col = convert(weight, 'W2BW')
                        else :
                            col = convert(weight, 'W2HSV')
                        #assign to the color map
                        color_map.data[loop_ind].color = col
                                           
    
class   weight_color(Operator):  
    
    """weight from&to vert_color"""        
    bl_idname = "object.weight_color"  
    bl_label = "weight & color"     
    bl_options = {'REGISTER', 'UNDO'}    #should remove undo ? 
    
    #parameters and variables
    convert = EnumProperty(
                name="Convert",
                description="Choose conversion",
                items=(('W2C', "Weight to vertex color", "convert weight to vertex color"),
                       ('C2W', "Vertex color to weight", "convert vertex color to weight")),
                default='W2C',
                )
    color = EnumProperty(
                name="Color type",
                description="Choose a color system",
                items=(('BW', "Gray scale", "map weight to grayscale"),
                       ('HSV', "RGB color", "map weight to rgb colors")),
                default='HSV',
                )
    zero_weight = BoolProperty(
                    name = "use zero weight",
                    description="add vertices with 0 weight to vertex groups",
                    default = 0,
                    )
    #main function
    def execute(self, context): 
        bpy.ops.object.mode_set(mode = 'OBJECT')
        if self.convert == 'W2C':
            weight2vert_col(self.color)
            bpy.ops.object.mode_set(mode = 'VERTEX_PAINT')
        else:
            vert_col2weight(self.color, self.zero_weight)
            bpy.ops.object.mode_set(mode = 'WEIGHT_PAINT')
            
        context.active_object.data.update()
        self.report({'INFO'},"Conversion is Done")
        return {'FINISHED'}
    #get inputs 
    def invoke(self, context, event):
            wm = context.window_manager
            return wm.invoke_props_dialog(self)
          

def addObject(self, context): 
    self.layout.operator(
    weight_color.bl_idname,
    text = weight_color.__doc__,
    icon = 'VPAINT_HLT')
    
def register():
    bpy.utils.register_class(weight_color)      
    bpy.types.VIEW3D_MT_object.append(addObject)

def unregister(): 
    bpy.types.VIEW3D_MT_object.remove(addObject)
    bpy.utils.unregister_class(weight_color)

if __name__ == "__main__":  
    register()


