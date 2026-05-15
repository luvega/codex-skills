# Nature Figure Requirements

Source basis: Nature research figure guide website checked on 2026-05-13, plus local requirement PDFs listed in `source_discussion_notes.md`.

## Main Figure Geometry

| Item | Requirement |
| --- | --- |
| Single-column width | 89 mm |
| Double-column width | 183 mm |
| Maximum Nature figure height | 170 mm |
| Panel arrangement | Neat, space-efficient, minimal white space, alphabetical panel order where possible |
| Panel labels | Lowercase `a`, `b`, `c`; bold, upright, 8 pt |

## Graphs

Require:

- Axis lines and tick marks.
- Axis labels with units in parentheses where units exist.
- Accessible color palette.
- Legible text, minimum 5 pt.
- Standard fonts, preferably Arial or Helvetica.

Avoid:

- Background gridlines unless they carry necessary quantitative meaning.
- Decorative icons, drop shadows, patterns, and chart effects.
- Text on busy images or low-contrast backgrounds.
- Overlapping labels.
- Colored text; use black text with colored boxes, keys, or keylines instead.
- Red-green-only color logic and rainbow scales.

## Text and Fonts

- Use sans-serif text, preferably Arial or Helvetica.
- Keep editable text; do not outline text.
- Embed fonts as TrueType 2 or 42. For matplotlib PDF output, set `pdf.fonttype = 42`.
- Text size should be 5 pt minimum and 7 pt maximum, except panel labels at 8 pt.
- Use Courier or another monospaced font for amino-acid one-letter sequences.
- Use Symbol font for Greek glyphs when needed.

## Images

- Use RGB color space for submitted artwork.
- Photographic image data must be at least 300 dpi; for final main-figure image elements, target 450 dpi where possible because the online proof maximum is 450 dpi.
- Do not artificially upsample low-resolution images as a substitute for real resolution.
- Keep scale bars and scale-bar text on editable layers; use scale bars instead of magnification factors.

## Export and File Formats

Main figures:

- Preferred vector formats: `.ai`, `.eps`, `.pdf` with editing capabilities retained.
- Other acceptable editable formats include layered Photoshop files, plain `.svg`, Excel, and postscript when components are embedded.
- Do not submit main figures as `.jpeg`, `.tiff`, `.png`, Canvas, DeltaGraph, TeX, ChemDraw, SigmaPlot, or CorelDraw final files.
- Keep main figure files below 50 MB where possible and embed, not link, components.

Extended Data:

- Use up to 10 Extended Data display items.
- Maximum page dimensions: 180 mm wide by 170 mm tall.
- Center each figure on its page.
- Line and stroke weights should be 0.25 to 1 pt.
- Export each Extended Data figure as `.jpg`/`.jpeg` preferred, `.tif`/`.tiff`, or `.eps`.
- Keep each Extended Data file below 10 MB.
- Naming convention: `CorrespondingAuthorSurname_EDfig1.jpg` or `CorrespondingAuthorSurname_EDtable1.jpg`.

## Tables

- Use horizontal rules above and below column headings and at the bottom of the table.
- Use spacing rather than excessive rules to separate blocks of data.
- Avoid color unless scientifically necessary.
- Keep tables on one page when possible.
- Use 7 pt sans-serif text; use alphabetical superscript letters for footnotes.

## Accessibility Palette

Use distinctive hue, lightness, and saturation. A safe categorical palette includes:

| Name | Hex |
| --- | --- |
| Black | `#000000` |
| Orange | `#e69f00` |
| Sky blue | `#56b4e9` |
| Bluish green | `#009e73` |
| Yellow | `#f0e442` |
| Blue | `#0072b2` |
| Vermillion | `#d55e00` |
| Reddish purple | `#cc79a7` |

For fluorescence-style overlays, do not rely on red-green contrast. Prefer red-to-magenta replacement or green-to-turquoise alternatives when the biology allows it, and provide keys.
