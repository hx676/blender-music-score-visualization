# Pipeline Reference

## Recommended order

1. Discover the input directory and identify the MIDI/MusicXML, score image or PDF, audio, and existing Blender project.
2. Convert or reuse score data with stable fields such as `start`, `dur`, `x`, `y`, `staff`, `voice`, `pitch`, and velocity. Keep score coordinates in one coordinate system; the reading axis should be Blender X and the score's vertical axis should be Blender Y.
3. Build or resume the scene with the existing geometry-node note cloud and ball source. Preserve the scene's audio strip and time base.
4. Build the printed score as paper slices or a wide backing surface. Keep staff lines flat and generate only the non-staff black notation as clean contour geometry when a raised engraving is requested.
5. Tune materials and camera before rendering. Render representative frames before changing the whole scene.
6. Save a review `.blend`, render a short preview, then render the full image sequence and encode it.

## Scene contract

The common project uses these names:

- `chase_cam`: active camera.
- `cam_aim`, `cam_focus`: optional helpers; do not depend on them when the camera uses a fixed quaternion.
- `note_cloud`: geometry-node output for live note balls.
- `ball_src`: source mesh instanced by the note geometry node group.
- `jumping_ball_shadows`: contact shadow geometry.
- `score_mat_00` ... `score_mat_11`: score slice materials.
- `paper_backing`: paper/background material.
- `ball_mat_energy`: glowing ball material.

If names differ, inspect the scene and adapt instead of creating duplicate objects.

## Current successful composition

The validated composition is a 16:9 Cycles scene with a warm paper surface, no visible outer score edge, two voice balls, a short comet tail, subtle DOF, and a dark restrained environment. The latest project used a 200 mm lens as a crop-safe compromise; 85 mm is acceptable only when the backing surface and crop are large enough to hide its edge.

## Failure patterns

- Full-sheet displacement relief creates spikes and fragmented black islands. Use clean contours for the engraved notation.
- Moving all black pixels upward makes staff lines float and destroys readability. Staff lines should remain flat.
- A paper material with emission makes the whole frame bright and removes ball contrast. Set paper emission to zero.
- A raw active-note bounding box is not a camera target. It changes discontinuously as notes enter and leave the active window.
- Changing the scene FPS without retiming note attributes or the audio strip causes animation/audio mismatch.
