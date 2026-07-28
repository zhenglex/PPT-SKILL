---
name: editable-ppt-from-images-wps
description: Convert PNG/JPG design images or screenshots into layered PowerPoint/WPS decks where the slide visually matches the source image, text is editable, and non-text visual elements are separate movable/replaceable picture objects. Use when the user asks to split image text and elements, separate base image/elements/text, place images into PPT with editable text and draggable elements, replace one slide with a new image using the same method, use WPS/Computer Use for verification, or normalize deck fonts to a user-specified or open CJK font with nearest even font sizes.
---

# Editable PPT From Images WPS

## Objective

Reconstruct each source image as a PPT slide made from three layer types:

- Full-slide base image with editable text removed.
- Separate image crops for non-text elements that should be movable or replaceable.
- PPT text boxes for readable page text.

Prioritize visual fidelity. If tiny UI labels, screenshot interface text, icon glyphs, or texture-like marks would look worse as editable text, keep them embedded in the relevant image layer and document that choice.

## Workflow

1. Prepare a task folder under the current project, for example `work/presentations/<slug>/tmp`, and put finished decks in `outputs/`.
2. Collect source images in slide order. Verify count, dimensions, aspect ratio, and the specific slides the user wants replaced.
3. Run OCR on each image with RapidOCR or the best available local OCR. Treat OCR as a starting point, not ground truth; inspect Chinese punctuation, dates, and product terms manually.
4. Build a layer manifest per slide:
   - `source`: original image path.
   - `width`, `height`: source pixel dimensions.
   - `base`: full-slide image after text removal.
   - `elements`: cropped non-text picture objects with exact `x`, `y`, `w`, `h`.
   - `texts`: editable text boxes with `text`, `x`, `y`, `w`, `h`, font size, color, bold/weight, and alignment.
5. Remove editable text from the base image. Create a mask from OCR polygons with small padding, then use OpenCV inpainting. Exclude tiny micro-text, UI screenshots, icon labels, and any text that must remain part of an image element for fidelity.
6. Crop movable visual elements from the original image or the textless image, depending on which preserves the intended look. In the base layer, cover or inpaint those element regions so the slide does not show duplicate objects.
7. Assemble the PPT using a slide size that matches the image aspect ratio exactly. Add layers in this order: base image, element picture crops, editable text boxes. Use pixel-derived coordinates consistently across all layers.
8. For replacement pages, process only the new image for that slide, update that slide entry in the manifest, and export to a new deck name instead of overwriting the previous output unless the user explicitly asks.
9. Normalize fonts when requested. Use `scripts/normalize_ppt_fonts.py` to set all OOXML font declarations to an open or user-specified CJK font and snap every text size to the nearest even point size.
10. Verify visually and interactively. Render slide previews/contact sheets, compare against sources, run any available PPT validation, then use WPS/Computer Use when requested to confirm text boxes are editable and element crops can be selected or moved.

## Layering Rules

- Preserve the original image as the authority for color, shadows, icons, diagrams, photos, and decorative geometry.
- Make major headings, bullets, body copy, numbers, labels, and captions editable unless fidelity clearly requires embedding them.
- Use the original source image for element crops when the element includes gradients, glows, photo detail, or icons. Use the textless image only when the crop would otherwise duplicate editable text.
- Keep element boxes coarse enough for easy user manipulation but tight enough that moving or replacing one object does not drag unrelated background.
- Avoid rebuilding complex illustrations from vector primitives unless the user specifically wants vector redraws. Cropped original elements are usually more faithful.
- Keep a manifest so a changed slide can be regenerated without rebuilding the whole deck by hand.

## PPT Assembly

Use the bundled workspace runtimes for Python/Node when system runtimes are missing. For PPT creation, prefer the presentation tooling already available in the environment, such as `@oai/artifact-tool`, because it exports editable text and image objects reliably.

Implementation pattern:

- Create one slide per manifest entry.
- Set slide dimensions from the source image ratio, not from arbitrary defaults.
- Add the full-slide base image first.
- Add each `elements[]` crop at its exact pixel-mapped location.
- Add each `texts[]` item as an editable text box after image layers so text remains selectable.
- Export a PPTX plus preview images/contact sheet for QA.

## WPS Verification

When the user explicitly asks to use WPS or Computer Use, also use the `computer-use:computer-use` skill before controlling Windows apps.

In WPS:

1. Open the exported PPTX.
2. Check representative slides, including any replaced page.
3. Click a heading/body text box and confirm it is editable. If font normalization was requested, confirm the toolbar shows the requested font and an even font size close to the original.
4. Click a major non-text element crop and confirm it selects as a picture object that can be moved/replaced. Undo any test movement.
5. Save once in WPS if the user needs WPS-compatible output.

## Font Normalization

Run the bundled script after deck generation when the user asks for all text to use one font family and nearest even sizes:

```bash
python scripts/normalize_ppt_fonts.py input.pptx output.pptx --font "Noto Sans CJK SC"
```

The script rewrites PPTX XML font declarations (`latin`, `ea`, `cs`, theme typefaces, run properties) and rounds each `sz` value to the closest even point size, choosing the lower even size on ties.

Do not bundle or redistribute proprietary font files with the skill. If the user requests a proprietary system font such as `微软雅黑`, only write the font family name into the PPTX and rely on the user's licensed local environment to render it.

## QA Checklist

- Source images are in the intended slide order.
- OCR text has been manually checked against the image.
- Textless base images do not leave obvious ghosts or holes.
- Movable element crops align perfectly over the base.
- Rendered PPT previews visually match the originals.
- Replaced slides use the same layer strategy as the rest of the deck.
- All requested fonts and even sizes are applied after normalization.
- WPS confirms both editable text and movable image elements.

## Final Response

Return the final PPTX path, mention any slides that were replaced, and briefly state what was verified. If small screenshot/UI text was intentionally left embedded for fidelity, say that plainly.
