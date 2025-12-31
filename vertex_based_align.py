bl_info = {
    "name": "Vertex Based Align Tool",
    "author": "Vince Horlait",
    "version": (4, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Vertex Based Align Tool",
    "description": "Align objects using marked vertices with automatic rotation detection (1, 2, or 3 vertices)",
    "category": "Object",
}

import bpy
import mathutils
from bpy.props import IntProperty, StringProperty
from bpy.types import Operator, Panel


class OBJECT_OT_mark_source_vertex_1(Operator):
    """Mark the selected vertex as source point 1 (origin)"""
    bl_idname = "object.mark_source_vertex_1"
    bl_label = "Mark Source Vertex 1"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "No active mesh object")
            return {'CANCELLED'}
        
        if obj.mode != 'EDIT':
            self.report({'ERROR'}, "Switch to Edit Mode to select a vertex")
            return {'CANCELLED'}
        
        import bmesh
        bm = bmesh.from_edit_mesh(obj.data)
        
        selected_verts = [v for v in bm.verts if v.select]
        
        if len(selected_verts) == 0:
            self.report({'ERROR'}, "No vertex selected")
            return {'CANCELLED'}
        
        if len(selected_verts) > 1:
            self.report({'WARNING'}, "Multiple vertices selected, using the first one")
        
        vertex_index = selected_verts[0].index
        context.scene.vertex_align_source_object = obj.name
        context.scene.vertex_align_source_vertex_1 = vertex_index
        
        self.report({'INFO'}, f"Source vertex 1 marked: {obj.name}, index {vertex_index}")
        
        return {'FINISHED'}


class OBJECT_OT_mark_source_vertex_2(Operator):
    """Mark the selected vertex as source point 2 (direction)"""
    bl_idname = "object.mark_source_vertex_2"
    bl_label = "Mark Source Vertex 2"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "No active mesh object")
            return {'CANCELLED'}
        
        if obj.mode != 'EDIT':
            self.report({'ERROR'}, "Switch to Edit Mode to select a vertex")
            return {'CANCELLED'}
        
        # Check if source vertex 1 is marked
        source_obj_name = context.scene.vertex_align_source_object
        if not source_obj_name or source_obj_name != obj.name:
            self.report({'ERROR'}, "Mark source vertex 1 first on this object")
            return {'CANCELLED'}
        
        import bmesh
        bm = bmesh.from_edit_mesh(obj.data)
        
        selected_verts = [v for v in bm.verts if v.select]
        
        if len(selected_verts) == 0:
            self.report({'ERROR'}, "No vertex selected")
            return {'CANCELLED'}
        
        if len(selected_verts) > 1:
            self.report({'WARNING'}, "Multiple vertices selected, using the first one")
        
        vertex_index = selected_verts[0].index
        
        # Check that it's different from vertex 1
        if vertex_index == context.scene.vertex_align_source_vertex_1:
            self.report({'ERROR'}, "Vertex 2 must be different from vertex 1")
            return {'CANCELLED'}
        
        context.scene.vertex_align_source_vertex_2 = vertex_index
        
        self.report({'INFO'}, f"Source vertex 2 marked: {obj.name}, index {vertex_index}")
        
        return {'FINISHED'}


class OBJECT_OT_mark_source_vertex_3(Operator):
    """Mark the selected vertex as source point 3 (plane)"""
    bl_idname = "object.mark_source_vertex_3"
    bl_label = "Mark Source Vertex 3"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "No active mesh object")
            return {'CANCELLED'}
        
        if obj.mode != 'EDIT':
            self.report({'ERROR'}, "Switch to Edit Mode to select a vertex")
            return {'CANCELLED'}
        
        # Check if source vertices 1 and 2 are marked
        source_obj_name = context.scene.vertex_align_source_object
        if not source_obj_name or source_obj_name != obj.name:
            self.report({'ERROR'}, "Mark source vertex 1 and 2 first on this object")
            return {'CANCELLED'}
        
        if context.scene.vertex_align_source_vertex_2 < 0:
            self.report({'ERROR'}, "Mark source vertex 2 first")
            return {'CANCELLED'}
        
        import bmesh
        bm = bmesh.from_edit_mesh(obj.data)
        
        selected_verts = [v for v in bm.verts if v.select]
        
        if len(selected_verts) == 0:
            self.report({'ERROR'}, "No vertex selected")
            return {'CANCELLED'}
        
        if len(selected_verts) > 1:
            self.report({'WARNING'}, "Multiple vertices selected, using the first one")
        
        vertex_index = selected_verts[0].index
        
        # Check that it's different from vertices 1 and 2
        if vertex_index == context.scene.vertex_align_source_vertex_1:
            self.report({'ERROR'}, "Vertex 3 must be different from vertex 1")
            return {'CANCELLED'}
        if vertex_index == context.scene.vertex_align_source_vertex_2:
            self.report({'ERROR'}, "Vertex 3 must be different from vertex 2")
            return {'CANCELLED'}
        
        context.scene.vertex_align_source_vertex_3 = vertex_index
        
        self.report({'INFO'}, f"Source vertex 3 marked: {obj.name}, index {vertex_index}")
        
        return {'FINISHED'}


class OBJECT_OT_mark_target_vertex_1(Operator):
    """Mark the selected vertex as target point 1 (origin)"""
    bl_idname = "object.mark_target_vertex_1"
    bl_label = "Mark Target Vertex 1"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "No active mesh object")
            return {'CANCELLED'}
        
        if obj.mode != 'EDIT':
            self.report({'ERROR'}, "Switch to Edit Mode to select a vertex")
            return {'CANCELLED'}
        
        import bmesh
        bm = bmesh.from_edit_mesh(obj.data)
        
        selected_verts = [v for v in bm.verts if v.select]
        
        if len(selected_verts) == 0:
            self.report({'ERROR'}, "No vertex selected")
            return {'CANCELLED'}
        
        if len(selected_verts) > 1:
            self.report({'WARNING'}, "Multiple vertices selected, using the first one")
        
        vertex_index = selected_verts[0].index
        context.scene.vertex_align_target_object = obj.name
        context.scene.vertex_align_target_vertex_1 = vertex_index
        
        self.report({'INFO'}, f"Target vertex 1 marked: {obj.name}, index {vertex_index}")
        
        return {'FINISHED'}


class OBJECT_OT_mark_target_vertex_2(Operator):
    """Mark the selected vertex as target point 2 (direction)"""
    bl_idname = "object.mark_target_vertex_2"
    bl_label = "Mark Target Vertex 2"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "No active mesh object")
            return {'CANCELLED'}
        
        if obj.mode != 'EDIT':
            self.report({'ERROR'}, "Switch to Edit Mode to select a vertex")
            return {'CANCELLED'}
        
        # Check if target vertex 1 is marked
        target_obj_name = context.scene.vertex_align_target_object
        if not target_obj_name or target_obj_name != obj.name:
            self.report({'ERROR'}, "Mark target vertex 1 first on this object")
            return {'CANCELLED'}
        
        import bmesh
        bm = bmesh.from_edit_mesh(obj.data)
        
        selected_verts = [v for v in bm.verts if v.select]
        
        if len(selected_verts) == 0:
            self.report({'ERROR'}, "No vertex selected")
            return {'CANCELLED'}
        
        if len(selected_verts) > 1:
            self.report({'WARNING'}, "Multiple vertices selected, using the first one")
        
        vertex_index = selected_verts[0].index
        
        # Check that it's different from vertex 1
        if vertex_index == context.scene.vertex_align_target_vertex_1:
            self.report({'ERROR'}, "Vertex 2 must be different from vertex 1")
            return {'CANCELLED'}
        
        context.scene.vertex_align_target_vertex_2 = vertex_index
        
        self.report({'INFO'}, f"Target vertex 2 marked: {obj.name}, index {vertex_index}")
        
        return {'FINISHED'}


class OBJECT_OT_mark_target_vertex_3(Operator):
    """Mark the selected vertex as target point 3 (plane)"""
    bl_idname = "object.mark_target_vertex_3"
    bl_label = "Mark Target Vertex 3"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "No active mesh object")
            return {'CANCELLED'}
        
        if obj.mode != 'EDIT':
            self.report({'ERROR'}, "Switch to Edit Mode to select a vertex")
            return {'CANCELLED'}
        
        # Check if target vertices 1 and 2 are marked
        target_obj_name = context.scene.vertex_align_target_object
        if not target_obj_name or target_obj_name != obj.name:
            self.report({'ERROR'}, "Mark target vertex 1 and 2 first on this object")
            return {'CANCELLED'}
        
        if context.scene.vertex_align_target_vertex_2 < 0:
            self.report({'ERROR'}, "Mark target vertex 2 first")
            return {'CANCELLED'}
        
        import bmesh
        bm = bmesh.from_edit_mesh(obj.data)
        
        selected_verts = [v for v in bm.verts if v.select]
        
        if len(selected_verts) == 0:
            self.report({'ERROR'}, "No vertex selected")
            return {'CANCELLED'}
        
        if len(selected_verts) > 1:
            self.report({'WARNING'}, "Multiple vertices selected, using the first one")
        
        vertex_index = selected_verts[0].index
        
        # Check that it's different from vertices 1 and 2
        if vertex_index == context.scene.vertex_align_target_vertex_1:
            self.report({'ERROR'}, "Vertex 3 must be different from vertex 1")
            return {'CANCELLED'}
        if vertex_index == context.scene.vertex_align_target_vertex_2:
            self.report({'ERROR'}, "Vertex 3 must be different from vertex 2")
            return {'CANCELLED'}
        
        context.scene.vertex_align_target_vertex_3 = vertex_index
        
        self.report({'INFO'}, f"Target vertex 3 marked: {obj.name}, index {vertex_index}")
        
        return {'FINISHED'}


class OBJECT_OT_align_smart(Operator):
    """Align source to target (automatically detects position only, partial rotation, or full rotation)"""
    bl_idname = "object.align_smart"
    bl_label = "Align objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Get source object
        source_obj_name = context.scene.vertex_align_source_object
        if not source_obj_name or source_obj_name not in bpy.data.objects:
            self.report({'ERROR'}, "No source object marked")
            return {'CANCELLED'}
        
        source_obj = bpy.data.objects[source_obj_name]
        source_vertex_1_index = context.scene.vertex_align_source_vertex_1
        source_vertex_2_index = context.scene.vertex_align_source_vertex_2
        source_vertex_3_index = context.scene.vertex_align_source_vertex_3
        
        # Get target object
        target_obj_name = context.scene.vertex_align_target_object
        if not target_obj_name or target_obj_name not in bpy.data.objects:
            self.report({'ERROR'}, "No target object marked")
            return {'CANCELLED'}
        
        target_obj = bpy.data.objects[target_obj_name]
        target_vertex_1_index = context.scene.vertex_align_target_vertex_1
        target_vertex_2_index = context.scene.vertex_align_target_vertex_2
        target_vertex_3_index = context.scene.vertex_align_target_vertex_3
        
        # Determine alignment mode
        has_3_vertices = (source_vertex_2_index >= 0 and target_vertex_2_index >= 0 and 
                         source_vertex_3_index >= 0 and target_vertex_3_index >= 0)
        has_2_vertices = (source_vertex_2_index >= 0 and target_vertex_2_index >= 0)
        
        # Make sure we're in Object mode
        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        
        if has_3_vertices:
            # FULL ROTATION alignment (3 vertices) - Sequential approach
            # STEP 1: Align with 2 vertices (this code works perfectly)
            source_v1_local = source_obj.data.vertices[source_vertex_1_index].co
            source_v2_local = source_obj.data.vertices[source_vertex_2_index].co
            source_v3_local = source_obj.data.vertices[source_vertex_3_index].co
            source_v1_world = source_obj.matrix_world @ source_v1_local
            source_v2_world = source_obj.matrix_world @ source_v2_local
            
            target_v1_local = target_obj.data.vertices[target_vertex_1_index].co
            target_v2_local = target_obj.data.vertices[target_vertex_2_index].co
            target_v3_local = target_obj.data.vertices[target_vertex_3_index].co
            target_v1_world = target_obj.matrix_world @ target_v1_local
            target_v2_world = target_obj.matrix_world @ target_v2_local
            target_v3_world = target_obj.matrix_world @ target_v3_local
            
            # Calculate direction vectors
            source_dir = (source_v2_world - source_v1_world).normalized()
            target_dir = (target_v2_world - target_v1_world).normalized()
            
            # Calculate rotation needed
            rotation_quat = source_dir.rotation_difference(target_dir)
            rotation_matrix = rotation_quat.to_matrix().to_4x4()
            
            # Create translation matrix to move pivot to source vertex 1
            pivot_to_origin = mathutils.Matrix.Translation(-source_v1_world)
            origin_to_pivot = mathutils.Matrix.Translation(source_v1_world)
            
            # Apply rotation around source vertex 1
            source_obj.matrix_world = origin_to_pivot @ rotation_matrix @ pivot_to_origin @ source_obj.matrix_world
            
            # Align positions
            source_v1_world_new = source_obj.matrix_world @ source_v1_local
            offset = target_v1_world - source_v1_world_new
            source_obj.location += offset
            
            # STEP 2: Rotate around axis 1→2 to align vertex 3
            # Recalculate positions after step 1
            source_v1_world = source_obj.matrix_world @ source_v1_local
            source_v2_world = source_obj.matrix_world @ source_v2_local
            source_v3_world = source_obj.matrix_world @ source_v3_local
            
            # The rotation axis (now aligned between source and target)
            axis = (target_v2_world - target_v1_world).normalized()
            
            # Project v3 onto plane perpendicular to axis
            # Source v3 projection
            v1_to_v3_source = source_v3_world - source_v1_world
            proj_on_axis_source = v1_to_v3_source.dot(axis) * axis
            perp_source = v1_to_v3_source - proj_on_axis_source
            
            # Target v3 projection
            v1_to_v3_target = target_v3_world - target_v1_world
            proj_on_axis_target = v1_to_v3_target.dot(axis) * axis
            perp_target = v1_to_v3_target - proj_on_axis_target
            
            # Calculate rotation angle
            if perp_source.length > 0.0001 and perp_target.length > 0.0001:
                perp_source_norm = perp_source.normalized()
                perp_target_norm = perp_target.normalized()
                
                # Angle between projections
                cos_angle = perp_source_norm.dot(perp_target_norm)
                cos_angle = max(-1.0, min(1.0, cos_angle))  # Clamp to avoid numerical errors
                angle = mathutils.Vector.angle(perp_source_norm, perp_target_norm)
                
                # Determine sign of rotation
                cross = perp_source_norm.cross(perp_target_norm)
                if cross.dot(axis) < 0:
                    angle = -angle
                
                # Create rotation around axis
                rotation_quat_v3 = mathutils.Quaternion(axis, angle)
                rotation_matrix_v3 = rotation_quat_v3.to_matrix().to_4x4()
                
                # Apply rotation around vertex 1
                pivot_to_origin = mathutils.Matrix.Translation(-source_v1_world)
                origin_to_pivot = mathutils.Matrix.Translation(source_v1_world)
                
                source_obj.matrix_world = origin_to_pivot @ rotation_matrix_v3 @ pivot_to_origin @ source_obj.matrix_world
                
                # STEP 3: Realign position (vertex 1 may have moved slightly during rotation)
                source_v1_world_final = source_obj.matrix_world @ source_v1_local
                final_offset = target_v1_world - source_v1_world_final
                source_obj.location += final_offset
            
            self.report({'INFO'}, f"Aligned {source_obj.name} to {target_obj.name} (position + full rotation)")
        
        elif has_2_vertices:
            # POSITION + ROTATION alignment (2 vertices - original working code)
            source_v1_local = source_obj.data.vertices[source_vertex_1_index].co
            source_v2_local = source_obj.data.vertices[source_vertex_2_index].co
            source_v1_world = source_obj.matrix_world @ source_v1_local
            source_v2_world = source_obj.matrix_world @ source_v2_local
            
            target_v1_local = target_obj.data.vertices[target_vertex_1_index].co
            target_v2_local = target_obj.data.vertices[target_vertex_2_index].co
            target_v1_world = target_obj.matrix_world @ target_v1_local
            target_v2_world = target_obj.matrix_world @ target_v2_local
            
            # Calculate direction vectors
            source_dir = (source_v2_world - source_v1_world).normalized()
            target_dir = (target_v2_world - target_v1_world).normalized()
            
            # Calculate rotation needed
            rotation_quat = source_dir.rotation_difference(target_dir)
            rotation_matrix = rotation_quat.to_matrix().to_4x4()
            
            # Create translation matrix to move pivot to source vertex 1
            pivot_to_origin = mathutils.Matrix.Translation(-source_v1_world)
            origin_to_pivot = mathutils.Matrix.Translation(source_v1_world)
            
            # Apply rotation around source vertex 1
            source_obj.matrix_world = origin_to_pivot @ rotation_matrix @ pivot_to_origin @ source_obj.matrix_world
            
            # Now align positions
            source_v1_world_new = source_obj.matrix_world @ source_v1_local
            offset = target_v1_world - source_v1_world_new
            source_obj.location += offset
            
            self.report({'INFO'}, f"Aligned {source_obj.name} to {target_obj.name} (position + rotation)")
        
        else:
            # POSITION ONLY alignment
            source_vertex_local = source_obj.data.vertices[source_vertex_1_index].co
            source_vertex_world = source_obj.matrix_world @ source_vertex_local
            
            target_vertex_local = target_obj.data.vertices[target_vertex_1_index].co
            target_vertex_world = target_obj.matrix_world @ target_vertex_local
            
            offset = target_vertex_world - source_vertex_world
            source_obj.location += offset
            
            self.report({'INFO'}, f"Aligned {source_obj.name} to {target_obj.name} (position only)")
        
        return {'FINISHED'}


class OBJECT_OT_clear_marked_vertices(Operator):
    """Clear all marked vertices"""
    bl_idname = "object.clear_marked_vertices"
    bl_label = "Clear All"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        context.scene.vertex_align_source_object = ""
        context.scene.vertex_align_source_vertex_1 = -1
        context.scene.vertex_align_source_vertex_2 = -1
        context.scene.vertex_align_source_vertex_3 = -1
        context.scene.vertex_align_target_object = ""
        context.scene.vertex_align_target_vertex_1 = -1
        context.scene.vertex_align_target_vertex_2 = -1
        context.scene.vertex_align_target_vertex_3 = -1
        
        self.report({'INFO'}, "All marked vertices cleared")
        
        return {'FINISHED'}


class VIEW3D_PT_vertex_align(Panel):
    """Panel in the sidebar for Vertex Align tool"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vertex Based Align Tool"
    bl_label = "Vertex Based Align Tool"
    
    def draw(self, context):
        layout = self.layout
        
        # Source object information
        box = layout.box()
        box.label(text="Source Object:", icon='OBJECT_DATA')
        
        source_obj_name = context.scene.vertex_align_source_object
        if source_obj_name and source_obj_name in bpy.data.objects:
            box.label(text=f"  {source_obj_name}")
            
            v1_index = context.scene.vertex_align_source_vertex_1
            v2_index = context.scene.vertex_align_source_vertex_2
            v3_index = context.scene.vertex_align_source_vertex_3
            
            box.label(text=f"  Vertex 1: {v1_index}", icon='CHECKMARK')
            
            if v2_index >= 0:
                box.label(text=f"  Vertex 2: {v2_index}", icon='CHECKMARK')
            else:
                box.label(text="  Vertex 2: Not marked")
            
            if v3_index >= 0:
                box.label(text=f"  Vertex 3: {v3_index}", icon='CHECKMARK')
            else:
                box.label(text="  Vertex 3: Not marked")
        else:
            box.label(text="  None marked")
        
        # Target object information
        box = layout.box()
        box.label(text="Target Object:", icon='OBJECT_DATA')
        
        target_obj_name = context.scene.vertex_align_target_object
        if target_obj_name and target_obj_name in bpy.data.objects:
            box.label(text=f"  {target_obj_name}")
            
            v1_index = context.scene.vertex_align_target_vertex_1
            v2_index = context.scene.vertex_align_target_vertex_2
            v3_index = context.scene.vertex_align_target_vertex_3
            
            box.label(text=f"  Vertex 1: {v1_index}", icon='CHECKMARK')
            
            if v2_index >= 0:
                box.label(text=f"  Vertex 2: {v2_index}", icon='CHECKMARK')
            else:
                box.label(text="  Vertex 2: Not marked")
            
            if v3_index >= 0:
                box.label(text=f"  Vertex 3: {v3_index}", icon='CHECKMARK')
            else:
                box.label(text="  Vertex 3: Not marked")
        else:
            box.label(text="  None marked")
        
        layout.separator()
        
        # Mark source vertices
        col = layout.column(align=True)
        col.label(text="1. Mark Source Vertices:", icon='PIVOT_CURSOR')
        col.operator("object.mark_source_vertex_1", text="Mark Source Vertex 1")
        col.operator("object.mark_source_vertex_2", text="Mark Source Vertex 2 (optional)")
        col.operator("object.mark_source_vertex_3", text="Mark Source Vertex 3 (optional)")
        
        layout.separator()
        
        # Mark target vertices
        col = layout.column(align=True)
        col.label(text="2. Mark Target Vertices:", icon='PIVOT_CURSOR')
        col.operator("object.mark_target_vertex_1", text="Mark Target Vertex 1")
        col.operator("object.mark_target_vertex_2", text="Mark Target Vertex 2 (optional)")
        col.operator("object.mark_target_vertex_3", text="Mark Target Vertex 3 (optional)")
        
        layout.separator()
        
        # Alignment operation
        col = layout.column(align=True)
        col.label(text="3. Align objects:", icon='SNAP_ON')
        
        # Check what mode we're in
        source_v2 = context.scene.vertex_align_source_vertex_2
        source_v3 = context.scene.vertex_align_source_vertex_3
        target_v2 = context.scene.vertex_align_target_vertex_2
        target_v3 = context.scene.vertex_align_target_vertex_3
        
        if source_v2 >= 0 and target_v2 >= 0 and source_v3 >= 0 and target_v3 >= 0:
            col.operator("object.align_smart", text="Align (Pos + Full Rotation)", icon='ORIENTATION_GLOBAL')
        elif source_v2 >= 0 and target_v2 >= 0:
            col.operator("object.align_smart", text="Align (Pos + Partial Rotation)", icon='CON_ROTLIKE')
        else:
            col.operator("object.align_smart", text="Align (Position Only)", icon='CON_LOCLIKE')
        
        layout.separator()
        
        # Clear button
        layout.operator("object.clear_marked_vertices", icon='X')
        
        # Instructions
        layout.separator()
        box = layout.box()
        box.label(text="Quick Guide:", icon='INFO')
        box.label(text="Position Only:")
        box.label(text="• Mark Source Vertex 1")
        box.label(text="• Mark Target Vertex 1")
        box.separator()
        box.label(text="Partial Rotation:")
        box.label(text="• Mark Source Vertex 1 & 2")
        box.label(text="• Mark Target Vertex 1 & 2")
        box.separator()
        box.label(text="Full Rotation:")
        box.label(text="• Mark Source Vertex 1, 2 & 3")
        box.label(text="• Mark Target Vertex 1, 2 & 3")


# Register properties and classes
def register():
    bpy.utils.register_class(OBJECT_OT_mark_source_vertex_1)
    bpy.utils.register_class(OBJECT_OT_mark_source_vertex_2)
    bpy.utils.register_class(OBJECT_OT_mark_source_vertex_3)
    bpy.utils.register_class(OBJECT_OT_mark_target_vertex_1)
    bpy.utils.register_class(OBJECT_OT_mark_target_vertex_2)
    bpy.utils.register_class(OBJECT_OT_mark_target_vertex_3)
    bpy.utils.register_class(OBJECT_OT_align_smart)
    bpy.utils.register_class(OBJECT_OT_clear_marked_vertices)
    bpy.utils.register_class(VIEW3D_PT_vertex_align)
    
    bpy.types.Scene.vertex_align_source_object = StringProperty(
        name="Source Object",
        description="Name of the source object",
        default=""
    )
    bpy.types.Scene.vertex_align_source_vertex_1 = IntProperty(
        name="Source Vertex 1",
        description="Index of source vertex 1 (origin)",
        default=-1
    )
    bpy.types.Scene.vertex_align_source_vertex_2 = IntProperty(
        name="Source Vertex 2",
        description="Index of source vertex 2 (direction)",
        default=-1
    )
    bpy.types.Scene.vertex_align_source_vertex_3 = IntProperty(
        name="Source Vertex 3",
        description="Index of source vertex 3 (plane)",
        default=-1
    )
    bpy.types.Scene.vertex_align_target_object = StringProperty(
        name="Target Object",
        description="Name of the target object",
        default=""
    )
    bpy.types.Scene.vertex_align_target_vertex_1 = IntProperty(
        name="Target Vertex 1",
        description="Index of target vertex 1 (origin)",
        default=-1
    )
    bpy.types.Scene.vertex_align_target_vertex_2 = IntProperty(
        name="Target Vertex 2",
        description="Index of target vertex 2 (direction)",
        default=-1
    )
    bpy.types.Scene.vertex_align_target_vertex_3 = IntProperty(
        name="Target Vertex 3",
        description="Index of target vertex 3 (plane)",
        default=-1
    )


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_vertex_align)
    bpy.utils.unregister_class(OBJECT_OT_clear_marked_vertices)
    bpy.utils.unregister_class(OBJECT_OT_align_smart)
    bpy.utils.unregister_class(OBJECT_OT_mark_target_vertex_3)
    bpy.utils.unregister_class(OBJECT_OT_mark_target_vertex_2)
    bpy.utils.unregister_class(OBJECT_OT_mark_target_vertex_1)
    bpy.utils.unregister_class(OBJECT_OT_mark_source_vertex_3)
    bpy.utils.unregister_class(OBJECT_OT_mark_source_vertex_2)
    bpy.utils.unregister_class(OBJECT_OT_mark_source_vertex_1)
    
    del bpy.types.Scene.vertex_align_source_object
    del bpy.types.Scene.vertex_align_source_vertex_1
    del bpy.types.Scene.vertex_align_source_vertex_2
    del bpy.types.Scene.vertex_align_source_vertex_3
    del bpy.types.Scene.vertex_align_target_object
    del bpy.types.Scene.vertex_align_target_vertex_1
    del bpy.types.Scene.vertex_align_target_vertex_2
    del bpy.types.Scene.vertex_align_target_vertex_3


if __name__ == "__main__":
    register()