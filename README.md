# PPT-SKILL

> **重要：请先使用 ChatGPT 网页版生成 PPT 原始图片。**  
> 通常是一页 PPT 对应一张高清 PNG/JPG 设计图。这个 skill 的作用不是重新设计页面，而是把这些原始图片还原成可编辑、可移动元素的 PowerPoint/WPS 文件。

## Skill 名称

`editable-ppt-from-images-wps`

## 适用场景

当你已经有 ChatGPT 网页版生成的 PPT 页面图片、设计图或截图，并希望把它们制作成 PPT/WPS 文件时使用。

目标效果：

- 页面视觉效果尽量还原原图
- 文字变成 PPT 文本框，可编辑
- 非文字元素变成独立图片对象，可拖动、替换
- 背景、照片、图标、装饰线条、光效等尽量保留原图效果
- 可按要求统一字体，并把字号调整到最接近的偶数字号
- 可使用 WPS / Computer Use 做人工可编辑性检查

## 典型请求

```text
先用 ChatGPT 网页版生成每页 PPT 原始图片，再拆成可编辑 PPT
把图片中文字和元素拆分，做成 PPT，文字可编辑，元素可拖动
把 PPT 文字统一成指定字体，字号改成最接近的偶数字号
用 WPS 打开检查文字是否可编辑、元素是否可移动
```

## 工作流程

1. 先用 ChatGPT 网页版生成每页 PPT 原始图片。
2. 收集 PNG/JPG 图片，确认页数、顺序、尺寸和比例。
3. 对图片进行 OCR，识别可编辑文字。
4. 人工核对 OCR 结果，重点检查中文标点、日期、专有名词和误识别内容。
5. 为每页建立分层结构：
   - 去掉可编辑文字后的整页底图
   - 可移动/可替换的图片元素
   - 可编辑 PPT 文本框
6. 使用图像修复方式从底图中移除可编辑文字。
7. 从原图中裁切图标、图片、装饰元素等非文字内容。
8. 按原图比例创建 PPT 页面，并按“底图、元素、文字”的顺序叠放。
9. 生成 PPTX 后渲染预览，检查视觉还原度和文字溢出。
10. 如用户要求，打开 WPS 检查文字是否可编辑、元素是否可拖动。

## 字体说明

默认使用开放字体 `Noto Sans CJK SC` 作为公开安全的字体设置。

如果用户指定 `微软雅黑` 等系统字体，skill 只会把字体名称写入 PPTX，不会打包、复制或分发字体文件。用户需要在自己已授权的 Windows / Office / WPS 环境中使用这些字体。

## 文件结构

```text
skills/
  editable-ppt-from-images-wps/
    SKILL.md
    agents/
      openai.yaml
    scripts/
      normalize_ppt_fonts.py
```

## 安装方式

把 skill 文件夹复制到 Codex skills 目录：

```text
~/.codex/skills/editable-ppt-from-images-wps
```

然后重新打开或刷新 Codex，让 skill 被识别。

## License

MIT
