import bpy
import numpy as np

#Dont forget to put r on the beginning of the string
#It should be in this format: r"C:\Users\mycomputer\files\terrain.raw"
raw_file_path = r"Whatever your path to raw image is"
terrain_size = 1025  

#Controls height scale
height_scale = 2  

subdivision_count = 256

with open(raw_file_path, "rb") as f:
    heightmap = np.fromfile(f, dtype=np.uint16).reshape((terrain_size, terrain_size))

heightmap = heightmap.astype(np.float32) / np.max(heightmap)

bpy.ops.mesh.primitive_plane_add(size=10)
plane = bpy.context.active_object

bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.subdivide(number_cuts=subdivision_count - 1)
bpy.ops.object.mode_set(mode="OBJECT")

plane = bpy.context.active_object
plane.name = "TerrainPlane"
bpy.ops.object.shade_smooth()

mesh = plane.data

for vertex in mesh.vertices:
    x = int((vertex.co.x + 5) / 10 * (terrain_size - 1))
    y = int((vertex.co.y + 5) / 10 * (terrain_size - 1))
    
    x = max(0, min(x, terrain_size - 1))
    y = max(0, min(y, terrain_size - 1))

    vertex.co.z = heightmap[y, x] * height_scale
