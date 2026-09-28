"""Match the standard score camera to a monotonic note-cloud reading path.

This intentionally does not chase every evaluated note-cloud bounding-box jump.
Run with Blender:
  blender -b -P match_camera_track.py -- --source in.blend --output out.blend
"""

import argparse
import math
import sys
from pathlib import Path

import bpy
import numpy as np
from mathutils import Quaternion, Vector


def cli_args():
    values = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--camera", default="chase_cam")
    parser.add_argument("--note-object", default="note_cloud")
    parser.add_argument("--camera-y", type=float, default=-3.4)
    parser.add_argument("--look-ahead", type=float, default=44.0)
    parser.add_argument("--smooth-window", type=int, default=601)
    parser.add_argument("--lens", type=float, default=200.0)
    parser.add_argument("--height", type=float, default=13.0)
    parser.add_argument("--roll-degrees", type=float, default=2.0)
    parser.add_argument("--preview-dir")
    parser.add_argument("--preview-frames", default="120,1000,2000")
    return parser.parse_args(values)


def clear_action(obj):
    obj.animation_data_clear()


def write_location_action(obj, frames, x_values, y_value, name):
    clear_action(obj)
    obj.animation_data_create()
    action = bpy.data.actions.new(name)
    obj.animation_data.action = action
    try:
        slot = action.slots.new("OBJECT", obj.name)
        obj.animation_data.action_slot = slot
    except Exception:
        pass
    for index, values in ((0, x_values), (1, np.full(len(frames), y_value))):
        curve = action.fcurve_ensure_for_datablock(obj, "location", index=index)
        curve.keyframe_points.add(len(frames))
        coords = np.empty(len(frames) * 2, dtype=np.float64)
        coords[0::2] = frames
        coords[1::2] = values
        curve.keyframe_points.foreach_set("co", coords)
        curve.keyframe_points.foreach_set("interpolation", [1] * len(frames))
        curve.update()


def sample_center_x(scene, obj, frame, depsgraph):
    scene.frame_set(int(frame))
    depsgraph.update()
    evaluated = obj.evaluated_get(depsgraph)
    points = [evaluated.matrix_world @ Vector(corner) for corner in evaluated.bound_box]
    xs = np.array([point.x for point in points], dtype=np.float64)
    if len(xs) == 0 or not np.all(np.isfinite(xs)) or np.max(np.abs(xs)) < 1e-5:
        return math.nan
    return float((xs.min() + xs.max()) * 0.5)


opts = cli_args()
bpy.ops.wm.open_mainfile(filepath=str(Path(opts.source).resolve()))
scene = bpy.context.scene
camera = bpy.data.objects.get(opts.camera)
note_object = bpy.data.objects.get(opts.note_object)
if camera is None or note_object is None:
    raise RuntimeError(f"Missing camera '{opts.camera}' or note object '{opts.note_object}'")

frames = np.arange(scene.frame_start, scene.frame_end + 1, dtype=np.float64)
depsgraph = bpy.context.evaluated_depsgraph_get()
centers = np.array([sample_center_x(scene, note_object, frame, depsgraph) for frame in frames])
valid = np.isfinite(centers)
if valid.sum() < 2:
    raise RuntimeError("The note object did not produce enough valid evaluated frames")
centers = np.interp(frames, frames[valid], centers[valid])

linear = np.polyval(np.polyfit(frames, centers, 1), frames)
residual = centers - linear
window = max(3, int(opts.smooth_window) | 1)
half = window // 2
padded = np.pad(residual, (half, half), mode="edge")
smoothed = np.convolve(padded, np.ones(window) / window, mode="valid")
camera_x = linear + smoothed - opts.look_ahead

camera.location.y = opts.camera_y
camera.location.z = opts.height
camera.data.lens = opts.lens
camera.rotation_mode = "QUATERNION"
direction = Vector((opts.look_ahead, 0.0, -opts.height))
camera.rotation_quaternion = direction.to_track_quat("-Z", "Y") @ Quaternion(
    (0.0, 0.0, 1.0), math.radians(opts.roll_degrees)
)
camera.data.dof.use_dof = True
camera.data.dof.focus_object = None
camera.data.dof.focus_distance = direction.length
camera.data.dof.aperture_fstop = min(camera.data.dof.aperture_fstop or 4.0, 0.65)
write_location_action(camera, frames, camera_x, opts.camera_y, "matched_score_axis_camera")

steps = np.diff(camera_x)
print("CAMERA_TRACK", {
    "frames": len(frames),
    "valid_samples": int(valid.sum()),
    "step_min": float(steps.min()),
    "step_max": float(steps.max()),
    "step_mean": float(steps.mean()),
})

if opts.preview_dir:
    preview_dir = Path(opts.preview_dir).resolve()
    preview_dir.mkdir(parents=True, exist_ok=True)
    scene.render.image_settings.file_format = "PNG"
    for raw_frame in opts.preview_frames.split(","):
        frame = int(raw_frame.strip())
        if scene.frame_start <= frame <= scene.frame_end:
            scene.frame_set(frame)
            scene.render.filepath = str(preview_dir / f"camera_{frame:04d}.png")
            bpy.ops.render.render(write_still=True)

scene.frame_set(scene.frame_start)
bpy.ops.wm.save_as_mainfile(filepath=str(Path(opts.output).resolve()))
print("SAVED", opts.output)
