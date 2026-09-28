# Camera Synchronization

## Symptom diagnosis

If the balls move from a stable middle region to the top or bottom of the frame, compare the evaluated ball position and the camera target at the same frame. A long lens magnifies even a small score-axis offset. If the balls jump sideways, inspect camera Y and rotation curves before changing the ball animation.

## Correct strategy

The score reading axis is one-dimensional. Build a camera X track from the score-time path, not from the instantaneous bounding box of all active geometry:

```text
linear_score_x = fit(score_progress_x, frame)
slow_correction = long_window_average(actual_reference_x - linear_score_x)
camera_target_x = linear_score_x + slow_correction
camera_x = camera_target_x - fixed_look_ahead
```

Use a long correction window (hundreds of frames) only to absorb broad timing drift. The correction must be monotonic and must not follow individual note entrances. Keep camera Y fixed for a two-voice composition unless a deliberate register-following pan has been approved. Keep camera rotation fixed when the goal is stable framing.

## Validation

Measure:

- no negative camera X steps;
- no large one-frame jumps;
- camera and note animation use the same FPS and frame range;
- both balls remain visible in representative early, dense-middle, and late frames;
- the active ball group does not touch the frame edge unless deliberately staged.

Render three frames such as 120, 1000, and 2000 for a 4664-frame scene, but choose equivalent normalized positions for other durations.

## Blender 5.1 note

Blender 5.1 uses layered Actions. Create an object slot and use `action.fcurve_ensure_for_datablock(...)`; do not assume `action.fcurves.new(...)` is available.
