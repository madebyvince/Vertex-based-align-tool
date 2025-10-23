bl_info = {
    "name": "Vertex Based Align Tool",
    "author": "Vince Horlait",
    "version": (3, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Vertex Based Align Tool",
    "description": "Align objects using marked vertices with automatic rotation detection",
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


class OBJECT_OT_align_smart(Operator):
    """Align source to target (automatically detects position only or position + rotation)"""
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
        
        # Get target object
        target_obj_name = context.scene.vertex_align_target_object
        if not target_obj_name or target_obj_name not in bpy.data.objects:
            self.report({'ERROR'}, "No target object marked")
            return {'CANCELLED'}
        
        target_obj = bpy.data.objects[target_obj_name]
        target_vertex_1_index = context.scene.vertex_align_target_vertex_1
        target_vertex_2_index = context.scene.vertex_align_target_vertex_2
        
        # Check if we're doing rotation or position only
        do_rotation = (source_vertex_2_index >= 0 and target_vertex_2_index >= 0)
        
        # Make sure we're in Object mode
        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        
        if do_rotation:
            # POSITION + ROTATION alignment
            # Get source vertices in world space
            source_v1_local = source_obj.data.vertices[source_vertex_1_index].co
            source_v2_local = source_obj.data.vertices[source_vertex_2_index].co
            source_v1_world = source_obj.matrix_world @ source_v1_local
            source_v2_world = source_obj.matrix_world @ source_v2_local
            
            # Get target vertices in world space
            target_v1_local = target_obj.data.vertices[target_vertex_1_index].co
            target_v2_local = target_obj.data.vertices[target_vertex_2_index].co
            target_v1_world = target_obj.matrix_world @ target_v1_local
            target_v2_world = target_obj.matrix_world @ target_v2_local
            
            # Calculate direction vectors
            source_dir = (source_v2_world - source_v1_world).normalized()
            target_dir = (target_v2_world - target_v1_world).normalized()
            
            # Calculate rotation needed
            rotation_quat = source_dir.rotation_difference(target_dir)
            
            # Convert to 4x4 matrix
            rotation_matrix = rotation_quat.to_matrix().to_4x4()
            
            # Create translation matrix to move pivot to source vertex 1
            pivot_to_origin = mathutils.Matrix.Translation(-source_v1_world)
            origin_to_pivot = mathutils.Matrix.Translation(source_v1_world)
            
            # Apply rotation around source vertex 1
            source_obj.matrix_world = origin_to_pivot @ rotation_matrix @ pivot_to_origin @ source_obj.matrix_world
            
            # Now align positions
            # Recalculate source v1 position after rotation
            source_v1_world_new = source_obj.matrix_world @ source_v1_local
            
            # Calculate offset
            offset = target_v1_world - source_v1_world_new
            
            # Move source object
            source_obj.location += offset
            
            self.report({'INFO'}, f"Aligned {source_obj.name} to {target_obj.name} (position + rotation)")
        
        else:
            # POSITION ONLY alignment
            # Calculate world positions
            source_vertex_local = source_obj.data.vertices[source_vertex_1_index].co
            source_vertex_world = source_obj.matrix_world @ source_vertex_local
            
            target_vertex_local = target_obj.data.vertices[target_vertex_1_index].co
            target_vertex_world = target_obj.matrix_world @ target_vertex_local
            
            # Calculate offset
            offset = target_vertex_world - source_vertex_world
            
            # Move source object
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
        context.scene.vertex_align_target_object = ""
        context.scene.vertex_align_target_vertex_1 = -1
        context.scene.vertex_align_target_vertex_2 = -1
        
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
            
            box.label(text=f"  Vertex 1: {v1_index}", icon='CHECKMARK')
            
            if v2_index >= 0:
                box.label(text=f"  Vertex 2: {v2_index}", icon='CHECKMARK')
            else:
                box.label(text="  Vertex 2: Not marked")
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
            
            box.label(text=f"  Vertex 1: {v1_index}", icon='CHECKMARK')
            
            if v2_index >= 0:
                box.label(text=f"  Vertex 2: {v2_index}", icon='CHECKMARK')
            else:
                box.label(text="  Vertex 2: Not marked")
        else:
            box.label(text="  None marked")
        
        layout.separator()
        
        # Mark source vertices
        col = layout.column(align=True)
        col.label(text="1. Mark Source Vertices:", icon='PIVOT_CURSOR')
        col.operator("object.mark_source_vertex_1", text="Mark Source Vertex 1")
        col.operator("object.mark_source_vertex_2", text="Mark Source Vertex 2 (optional)")
        
        layout.separator()
        
        # Mark target vertices
        col = layout.column(align=True)
        col.label(text="2. Mark Target Vertices:", icon='PIVOT_CURSOR')
        col.operator("object.mark_target_vertex_1", text="Mark Target Vertex 1")
        col.operator("object.mark_target_vertex_2", text="Mark Target Vertex 2 (optional)")
        
        layout.separator()
        
        # Alignment operation
        col = layout.column(align=True)
        col.label(text="3. Align objects:", icon='SNAP_ON')
        
        # Check what mode we're in
        source_v2 = context.scene.vertex_align_source_vertex_2
        target_v2 = context.scene.vertex_align_target_vertex_2
        
        if source_v2 >= 0 and target_v2 >= 0:
            col.operator("object.align_smart", text="Align objects (Position + Rotation)", icon='CON_ROTLIKE')
        else:
            col.operator("object.align_smart", text="Align objects (Position Only)", icon='CON_LOCLIKE')
        
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
        box.label(text="• Click 'Align objects'")
        box.separator()
        box.label(text="Position + Rotation:")
        box.label(text="• Mark Source Vertex 1 & 2")
        box.label(text="• Mark Target Vertex 1 & 2")
        box.label(text="• Click 'Align objects'")


# Register properties and classes
def register():
    bpy.utils.register_class(OBJECT_OT_mark_source_vertex_1)
    bpy.utils.register_class(OBJECT_OT_mark_source_vertex_2)
    bpy.utils.register_class(OBJECT_OT_mark_target_vertex_1)
    bpy.utils.register_class(OBJECT_OT_mark_target_vertex_2)
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


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_vertex_align)
    bpy.utils.unregister_class(OBJECT_OT_clear_marked_vertices)
    bpy.utils.unregister_class(OBJECT_OT_align_smart)
    bpy.utils.unregister_class(OBJECT_OT_mark_target_vertex_2)
    bpy.utils.unregister_class(OBJECT_OT_mark_target_vertex_1)
    bpy.utils.unregister_class(OBJECT_OT_mark_source_vertex_2)
    bpy.utils.unregister_class(OBJECT_OT_mark_source_vertex_1)
    
    del bpy.types.Scene.vertex_align_source_object
    del bpy.types.Scene.vertex_align_source_vertex_1
    del bpy.types.Scene.vertex_align_source_vertex_2
    del bpy.types.Scene.vertex_align_target_object
    del bpy.types.Scene.vertex_align_target_vertex_1
    del bpy.types.Scene.vertex_align_target_vertex_2


if __name__ == "__main__":
    register()