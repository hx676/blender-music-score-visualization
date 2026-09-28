param(
    [Parameter(Mandatory = $true)] [string]$FramesDir,
    [Parameter(Mandatory = $true)] [string]$Output,
    [Parameter(Mandatory = $true)] [string]$Audio,
    [string]$Ffmpeg = 'C:\ffmpeg\bin\ffmpeg.exe',
    [int]$Fps = 30,
    [int]$StartNumber = 1,
    [int]$EndNumber = 0,
    [ValidateSet('png', 'jpg', 'jpeg')] [string]$Extension = 'png'
)

$firstFrame = Join-Path $FramesDir ("frame_{0:D4}.{1}" -f $StartNumber, $Extension)
if (-not (Test-Path -LiteralPath $firstFrame)) {
    throw "No input frames found at $FramesDir"
}
if ($EndNumber -gt 0) {
    $lastFrame = Join-Path $FramesDir ("frame_{0:D4}.{1}" -f $EndNumber, $Extension)
    if (-not (Test-Path -LiteralPath $lastFrame)) {
        throw "Input sequence is incomplete; missing $lastFrame"
    }
}

$pattern = Join-Path $FramesDir ("frame_%04d.{0}" -f $Extension)
& $Ffmpeg -y -framerate $Fps -start_number $StartNumber -i $pattern -i $Audio `
    -map 0:v:0 -map 1:a:0 -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p `
    -c:a aac -b:a 192k -shortest -movflags +faststart $Output
if ($LASTEXITCODE -ne 0) {
    throw "FFmpeg failed with exit code $LASTEXITCODE"
}
