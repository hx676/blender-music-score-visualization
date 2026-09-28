# Preview And Final Export

## Preview gate

1. Save a new review `.blend`.
2. Render three representative stills.
3. Render the first 5 seconds with the actual audio.
4. Check dimensions, both balls, score-edge crop, camera stability, and audio duration.

## Full export

When Blender's `image_settings.file_format` does not expose `FFMPEG`, render a numbered image sequence and use FFmpeg. A reliable final command is:

```powershell
ffmpeg -y -framerate 30 -start_number 1 -i "frame_%04d.png" -i "performance.wav" `
  -map 0:v:0 -map 1:a:0 -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p `
  -c:a aac -b:a 192k -shortest -movflags +faststart "final.mp4"
```

Use 1920x1080 for the final 16:9 output unless the user requests another size. Verify with `ffprobe` that the final file has H.264 video, AAC audio, the expected duration, and the requested dimensions.

## Long jobs

For a long Cycles render, start Blender detached with stdout/stderr redirected to log files. Do not continuously poll. If the user requests delayed checking, schedule one delayed check or use a detached monitor that waits for the Blender PID, verifies the last frame, and then invokes FFmpeg. Never merge a partial sequence silently.
