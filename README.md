# PPT-SKILL

> **Start here:** First use ChatGPT web (ChatGPT 网页版) to generate the original PPT design images, usually one high-resolution image per slide. This skill then reconstructs those images into a PPT/WPS deck with editable text and movable visual layers.

Reusable Codex skill for reconstructing design images as editable, layered PowerPoint/WPS decks.

## Included Skill

### `editable-ppt-from-images-wps`

Use this skill when a user provides PNG/JPG design images or screenshots and wants a PowerPoint/WPS deck that visually restores the source image while keeping:

- text editable as PPT text boxes
- non-text visual elements movable or replaceable as image objects
- the original background, photos, icons, effects, and decorative elements preserved from the source image
- selected replacement pages regenerated without changing the rest of the deck
- optional font normalization, using an open CJK font by default and snapping sizes to the nearest even point size
- optional WPS/Computer Use verification for editability

Typical prompts that should trigger the skill:

- "先用 ChatGPT 网页版生成每页 PPT 原始图片，再拆成可编辑 PPT"
- "把图片中文字和元素拆分，做成 PPT，文字可编辑，元素可拖动"
- "这页 PPT 换成这张图片，要求底图、元素、文字分开"
- "最后一页按同样方法替换，其他页不要动"
- "把 PPT 文字统一成指定字体，字号改成最接近的偶数字号"
- "用 WPS 打开检查文字是否可编辑、元素是否可移动"

## Workflow Summary

1. Use ChatGPT web first to generate the original PPT design images in slide order, then collect the PNG/JPG files and confirm dimensions/aspect ratio.
2. Run OCR to identify candidate editable text.
3. Manually review OCR output for Chinese punctuation, dates, product names, and false positives.
4. Build a per-slide layer manifest containing:
   - full-slide textless base image
   - cropped movable image elements
   - editable text boxes with coordinates and styling
5. Inpaint editable text out of the base image while preserving image-only content.
6. Crop visual elements from the original or textless image depending on fidelity.
7. Assemble the deck with `@oai/artifact-tool`, keeping slide dimensions aligned with the source image.
8. For replacement slides, regenerate only the affected slide and export a new PPTX.
9. Run QA: render previews, check overflow, compare unchanged slides, and inspect object counts.
10. When requested, open in WPS and verify that text boxes and image elements are selectable/editable.

## Publishing And Privacy

This repository contains only reusable skill instructions and a generic font-normalization script. It does not include user PPT files, source images, output decks, local workspace paths, API keys, tokens, or personal account credentials.

## Font Licensing Note

The skill does not bundle or redistribute any font files. The font-normalization script only writes a font family name into PPTX XML. The public default is `Noto Sans CJK SC`, an open font family. If a user chooses a proprietary system font such as `微软雅黑`, they should rely on their own licensed Windows/Office/WPS environment and should not redistribute or bundle the actual font file unless their license allows it.

## Installation

Copy the skill folder into your Codex skills directory:

```text
~/.codex/skills/editable-ppt-from-images-wps
```

Then start a new Codex session or refresh skill discovery.

## Files

```text
skills/
  editable-ppt-from-images-wps/
    SKILL.md
    agents/openai.yaml
    scripts/normalize_ppt_fonts.py
```
