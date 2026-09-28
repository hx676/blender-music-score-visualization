"""Render a Blender file to a numbered image sequence.

Example:
  blender -b -P render_sequence.py -- --blend scene.blend --frames-dir out/frames --width 1920 --height 1080
"""

import argparse
import sys
from pathlib import Path

import bpy


def args_after_separator():
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


parser = argparse.ArgumentParser()
parser.add_argument("--blend", required=True)
parser.add_argument("--frames-dir", required=True)
parser.add_argument("--start", type=int, default=None)
parser.add_argument("--end", type=int, default=None)
parser.add_argument("--width", type=int, default=1920)
parser.add_argument("--height", type=int, default=1080)
parser.add_argument("--fps", type=float, default=30)
parser.add_argument("--format", choices=("PNG", "JPEG"), default="PNG")
opts = parser.parse_args(args_after_separator())

bpy.ops.wm.open_mainfile(filepath=str(Path(opts.blend).resolve()))
scene = bpy.context.scene
scene.frame_start = scene.frame_start if opts.start is None else opts.start
scene.frame_end = scene.frame_end if opts.end is None else opts.end
scene.render.resolution_x = opts.width
scene.render.resolution_y = opts.height
scene.render.resolution_percentage = 100
scene.render.fps = opts.fps

frames_dir = Path(opts.frames_dir).resolve()
frames_dir.mkdir(parents=True, exist_ok=True)
scene.render.image_settings.file_format = opts.format
scene.render.filepath = str(frames_dir / "frame_")

print("RENDER_SEQUENCE", scene.render.engine, scene.frame_start, scene.frame_end, opts.width, opts.height, opts.fps)
bpy.ops.render.render(animation=True)
print("RENDER_SEQUENCE_DONE", frames_dir)
