# Images

- Supply artwork with suitable resolution and color profiles for the supported displays. Prefer scalable vectors for applicable 2D graphics.
- Balance raster quality with memory and rendering cost; inspect assets on actual devices where possible.
- For tvOS layered artwork, use meaningful foreground and background separation, an opaque background, restrained depth, and safe zones for focus movement.
- For spatial imagery, preserve visual comfort, place related text carefully, and use immersive presentation for appropriate moments.
- Verify platform-specific formats and scale factors before export.

Do not assume cropping, transparency, or a single bitmap variant works everywhere. Preview the final presentation, including parallax, masks, enlarged display, and overlays that can change readability.

Source: [Apple HIG — Images](https://developer.apple.com/design/human-interface-guidelines/images). Checked 2026-09-08.
