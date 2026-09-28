# Materials And Composition

## Paper

- Base color: pale warm ivory/yellow, not white.
- Emission: `0`.
- Roughness: high enough to keep the paper matte.
- Noise texture: very low contrast, used for roughness and a subtle bump/normal response.
- Scale the backing or use a crop-safe layout so no rectangular paper edge is visible.

## Engraving

- Staff lines remain part of the flat score surface.
- Non-staff black regions can use a clean extruded curve or mesh with a dark metallic Principled material.
- Keep extrusion small; the black notation should read as a printed/engraved surface, not thick floating blocks.
- If the user requests flat notation, keep the contour objects at paper height and disable the height offset.

## Balls and trails

- Use a small ball radius, approximately 0.13 scene units in the validated scene.
- Drive glow through emission nodes and keep the paper unlit by emission.
- Keep the comet tail behind the ball and short enough that it does not obscure noteheads.
- Preserve convergence when voice count changes: old balls travel toward new targets before being removed.

## Camera

- Use 16:9 output.
- Start around 85 mm and increase toward 200 mm only when required to hide the score edge.
- Enable DOF explicitly and verify focus distance/aperture in a rendered frame; a DOF setting alone is not proof that the effect is visible.
- Slight roll and downward tilt are acceptable, but do not animate roll or yaw for a stable score-axis shot.
