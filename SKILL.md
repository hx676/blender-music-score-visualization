---
name: blender-music-score-visualization
description: Build and refine Blender music-score visualizations from MIDI, MusicXML, or score assets, including synchronized hopping balls, multi-note convergence, comet trails, readable notation, stable camera tracking, Cycles materials, previews, and final MP4 export. Use when a user wants a complete animated visualization driven by a musical score.
---

# Blender Music Score Visualization

Use this skill for an end-to-end score visualization in Blender. The deliverable is a saved `.blend`, one or more review renders, and an encoded video when requested.

## Workflow

1. **Inspect inputs and project state.** Locate the MIDI/MusicXML, score image or PDF, audio, Blender executable, existing `.blend` files, and any local score data. Read the active scene before editing. Prefer an existing project and its scripts over rebuilding a parallel scene. Confirm Blender version, render engine, frame rate, frame range, resolution, audio strips, camera, and the objects `chase_cam`, `cam_aim`, `cam_focus`, `note_cloud`, and `ball_src` when present.
2. **Establish timing authority.** Use the MIDI or the score-data timing as the source of note starts and durations. Make scene time, audio time, and note animation use the same FPS. Verify duration from the audio and frame range before rendering; do not assume that a 60 FPS source should remain 60 FPS after a later scene conversion.
3. **Build the score surface.** Keep five-line staff geometry visible and flat. Treat the black notation outside the staff lines as the engraved score artwork: noteheads, stems, beams, flags, clefs, accidentals, rests, and brackets. Prefer clean contour geometry or masks with controlled extrusion over a full-sheet displacement relief, which tends to produce spikes and fragmented edges. If the user asks for no raised notation, flatten the contour objects while preserving the printed score.
4. **Build the musical motion.** Use one animated ball per voice or hop segment. When several notes become fewer notes, animate the old balls into the new target positions so they converge instead of disappearing in place. Keep the bounce and handoff continuous. Add a small comet particle tail behind each ball, but do not let the tail become the timing driver.
5. **Solve camera motion from score time.** The camera advances monotonically along the score reading axis. Use the same timing map as the musical animation. Do not chase the evaluated `note_cloud` bounding box frame by frame: notes entering and leaving the active window create false jumps. Use a linear score-axis base path plus a long-window correction only when needed. Keep the lateral axis locked unless the composition explicitly calls for a deliberate pan; this avoids left/right wobble and preserves both voice balls.
6. **Apply the visual treatment.** Keep the paper edge outside the camera crop. Use a pale warm paper with low-strength noise/bump texture and paper emission set to zero. Keep scene lighting restrained, use brighter ball emission for readability, and use Cycles when requested. For the current look, use a long lens around 85-200 mm, a slight camera roll/tilt, and shallow DOF without blurring the active balls or the nearby notation.
7. **Review before the full render.** Render at least three representative frames from the beginning, middle, and a dense passage. Check that both balls are present, score edges are absent, staff lines remain readable, the camera has no lateral oscillation, and the balls stay within a stable screen region. Then render a short preview with the actual audio before committing to the full output.
8. **Export the final video.** Prefer 1920x1080, 30 FPS, unless the source explicitly requires another format. Some Blender Windows builds expose no `FFMPEG` image format; in that case render a numbered PNG or JPEG sequence and use external FFmpeg to encode H.264 video with AAC audio. Keep the source `.blend` untouched and save a new output file.

## Project-specific references

- Read [references/pipeline.md](references/pipeline.md) when setting up or resuming the score scene.
- Read [references/camera-sync.md](references/camera-sync.md) when the balls drift, the camera wobbles, or the playback timing looks mismatched.
- Read [references/materials-and-composition.md](references/materials-and-composition.md) when adjusting paper, engraving, glow, lens, DOF, or score-edge framing.
- Read [references/export.md](references/export.md) for preview rendering, long background jobs, frame sequences, and MP4 encoding.

## Reusable helpers

- `scripts/inspect_scene.py` prints the scene contract before edits.
- `scripts/match_camera_track.py` writes a Blender 5.1-compatible monotonic score-axis camera track for the standard object names.
- `scripts/render_sequence.py` renders a `.blend` to a numbered image sequence at a requested resolution and frame range.
- `scripts/merge_sequence.ps1` encodes an image sequence plus optional audio into an MP4.

## Constraints

- Use absolute paths supplied by the user or discovered from the current workspace; do not invent input files.
- Save a new `.blend` for each meaningful revision. Do not overwrite the user's source scene without explicit permission.
- Preserve unrelated user changes and do not delete old renders or frames merely to make the folder tidy.
- Do not call a render complete until the expected last frame and the encoded video have been verified.
