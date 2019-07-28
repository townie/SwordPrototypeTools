import IPython
import math
import bpy
from mathutils import Vector, Matrix
import os
from math import radians

############ clean up #############

# Select objects by type
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        o.select = True
    else:
        o.select = False

# Call the operator only once
bpy.ops.object.delete()
# bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
# bpy.ops.wm.open_mainfile(filepath=bpy.data.filepath)
###################################


data_dir = '/home/townie/work/3d/SwordPrototype/train/'
file_loc = 'objs/sword1.obj'

imported_object = bpy.ops.import_scene.obj(filepath=data_dir + file_loc)

obj_object = bpy.context.selected_objects[0]

print('Imported name: ', obj_object.name)


for obj in bpy.data.objects:
    print(obj.name)


# obj = bpy.context.object
obj = obj_object

# Eventually apply transforms (comment if unwanted)
bpy.ops.object.transform_apply(rotation=True, scale=True)

minX = min([vertex.co[0] for vertex in obj.data.vertices])
minY = min([vertex.co[1] for vertex in obj.data.vertices])
minZ = min([vertex.co[2] for vertex in obj.data.vertices])

vMin = Vector([minX, minY, minZ])

maxDim = max(obj.dimensions)

if maxDim != 0:
    for v in obj.data.vertices:
        v.co -= vMin  # Set all coordinates start from (0, 0, 0)
        v.co /= maxDim  # Set all coordinates between 0 and 1
else:
    for v in obj.data.vertices:
        v.co -= vMin


blend_file_path = bpy.data.filepath
directory = os.path.dirname(blend_file_path)



print('finished')

loc, rot, scale = obj.matrix_world.decompose()

orig_loc, orig_rot, orig_scale = obj.matrix_world.decompose()

for axis in 'XYZ':
    for angle_in_degrees in range(0, 360, 30):

        # define the rotation
        # you can also use as axis Y,Z or a custom vector like (x,y,z)
        rot_mat = Matrix.Rotation(radians(angle_in_degrees), 4, axis)

        # decompose world_matrix's components, and from them assemble 4x4 matrices
        orig_loc_mat = Matrix.Translation(orig_loc)
        orig_rot_mat = orig_rot.to_matrix().to_4x4()
        orig_scale_mat = Matrix.Scale(orig_scale[0], 4, (1, 0, 0)) * Matrix.Scale(
            orig_scale[1], 4, (0, 1, 0)) * Matrix.Scale(orig_scale[2], 4, (0, 0, 1))

        # assemble the new matrix
        obj.matrix_world = orig_loc_mat * rot_mat * orig_rot_mat * orig_scale_mat
        # if angle_in_degrees == 180:
        #  IPython.embed()
        outputname = 'test_image{}{:03d}'.format(
            axis, angle_in_degrees)

        target_file = os.path.join(directory, outputname +'.obj')
        bpy.ops.export_scene.obj(filepath=target_file)

        bpy.data.scenes['Scene'].render.filepath = '/home/townie/work/3d/SwordPrototype/tmp/' + outputname + '.jpg'

        bpy.ops.render.render(write_still=True)
        # break
