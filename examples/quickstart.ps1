param(
    [Parameter(Mandatory = $true)] [string]$Blender,
    [Parameter(Mandatory = $true)] [string]$Skill,
    [Parameter(Mandatory = $true)] [string]$Source,
    [Parameter(Mandatory = $true)] [string]$Audio,
    [Parameter(Mandatory = $true)] [string]$WorkDir,
    [int]$LastFrame = 4664
)

$Matched = Join-Path $WorkDir 'scene_matched.blend'
$Stills = Join-Path $WorkDir 'camera-stills'
$PreviewFrames = Join-Path $WorkDir 'preview_frames'
$Preview = Join-Path $WorkDir 'preview_5s.mp4'
$FullFrames = Join-Path $WorkDir 'full_1080p_frames'
$Final = Join-Path $WorkDir 'score_visualization_1080p.mp4'

& $Blender -b -P (Join-Path $Skill 'scripts\inspect_scene.py') -- --blend $Source
if ($LASTEXITCODE -ne 0) { throw 'Scene inspection failed.' }

& $Blender -b -P (Join-Path $Skill 'scripts\match_camera_track.py') -- `
    --source $Source `
    --output $Matched `
    --preview-dir $Stills `
    --preview-frames '120,1000,2000'
if ($LASTEXITCODE -ne 0) { throw 'Camera matching failed.' }

& $Blender -b -P (Join-Path $Skill 'scripts\render_sequence.py') -- `
    --blend $Matched `
    --frames-dir $PreviewFrames `
    --start 1 --end 150 `
    --width 1280 --height 720 --fps 30
if ($LASTEXITCODE -ne 0) { throw 'Preview rendering failed.' }

& (Join-Path $Skill 'scripts\merge_sequence.ps1') `
    -FramesDir $PreviewFrames `
    -EndNumber 150 `
    -Audio $Audio `
    -Output $Preview
if ($LASTEXITCODE -ne 0) { throw 'Preview encoding failed.' }

Write-Host "Review the five-second preview: $Preview"
Read-Host 'Press Enter after approving the preview to start the full 1080p render'

& $Blender -b -P (Join-Path $Skill 'scripts\render_sequence.py') -- `
    --blend $Matched `
    --frames-dir $FullFrames `
    --width 1920 --height 1080 --fps 30
if ($LASTEXITCODE -ne 0) { throw 'Full render failed.' }

& (Join-Path $Skill 'scripts\merge_sequence.ps1') `
    -FramesDir $FullFrames `
    -EndNumber $LastFrame `
    -Audio $Audio `
    -Output $Final
if ($LASTEXITCODE -ne 0) { throw 'Final encoding failed.' }

Write-Host "Final video: $Final"
