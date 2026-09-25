# Right to left

- Prefer system components and directional layout semantics so the interface mirrors appropriately.
- Reverse navigation and ordered-progress relationships when their meaning follows reading direction. Do not reverse digits within a number.
- Keep controls that indicate a real physical direction faithful to that direction.
- Preserve logos, photographs, and nondirectional real-world symbols. Localize text-bearing or directional icons deliberately instead of mirroring every asset.
- Handle mixed scripts carefully: align longer paragraphs according to their language, and maintain consistent alignment within lists.

Test with actual Arabic or Hebrew content, numbers, directional controls, and mixed-language labels. Mirroring the entire screenshot can alter meaning and is not a valid substitute for bidirectional layout behavior.

Source: [Apple HIG — Right to left](https://developer.apple.com/design/human-interface-guidelines/right-to-left). Checked 2026-09-08.
