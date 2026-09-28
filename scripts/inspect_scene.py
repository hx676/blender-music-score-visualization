"""Print the scene contract before editing a score visualization.

Run with Blender:
  blender -b -P inspect_scene.py -- --blend path/to/scene.blend
"""

import argparse
import sys
from pathlib import Path

import bpy


def args_after_separator():
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


parser = argparse.ArgumentParser()
parser.add_argument("--blend", required=True)
opts = parser.parse_args(args_after_separator())

bpy.ops.wm.open_mainfile(filepath=str(Path(opts.blend).resolve()))
scene = bpy.context.scene
print("SCENE", {
    "engine": scene.render.engine,
    "fps": scene.render.fps,
    "frame_start": scene.frame_start,
    "frame_end": scene.frame_end,
    "resolution": (scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage),
})

for name in ("chase_cam", "cam_aim", "cam_focus", "note_cloud", "ball_src", "jumping_ball_shadows"):
    obj = bpy.data.objects.get(name)
    if obj is None:
        print("MISSING_OBJECT", name)
        continue
    print("OBJECT", name, obj.type, "location", tuple(round(v, 4) for v in obj.location))
    if obj.animation_data and obj.animation_data.action:
        print(" ACTION", obj.animation_data.action.name)

camera = bpy.data.objects.get("chase_cam")
if camera and camera.type == "CAMERA":
    print("CAMERA", {
        "lens": camera.data.lens,
        "dof_enabled": camera.data.dof.use_dof,
        "focus_distance": camera.data.dof.focus_distance,
        "fstop": camera.data.dof.aperture_fstop,
    })

if scene.sequence_editor:
    for strip in scene.sequence_editor.strips:
        if strip.type == "SOUND":
            print("AUDIO", strip.name, strip.sound.filepath, strip.frame_start, strip.frame_final_duration)
