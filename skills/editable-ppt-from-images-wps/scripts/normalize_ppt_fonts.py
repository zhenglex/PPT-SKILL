from __future__ import annotations

import argparse
import math
import shutil
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}

PROP_TAGS = {
    f"{{{NS['a']}}}rPr",
    f"{{{NS['a']}}}defRPr",
    f"{{{NS['a']}}}endParaRPr",
}

for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


def nearest_even_point(size_hundredths: str) -> str:
    size = int(size_hundredths)
    pt = size / 100.0
    lower = math.floor(pt / 2.0) * 2
    upper = math.ceil(pt / 2.0) * 2
    chosen = lower if abs(pt - lower) <= abs(upper - pt) else upper
    return str(max(2, int(chosen)) * 100)


def ensure_font_child(run_props: ET.Element, child_name: str, font_name: str) -> bool:
    child = run_props.find(f"a:{child_name}", NS)
    changed = False
    if child is None:
        child = ET.SubElement(run_props, f"{{{NS['a']}}}{child_name}")
        changed = True
    if child.get("typeface") != font_name:
        child.set("typeface", font_name)
        changed = True
    return changed


def normalize_xml(xml_bytes: bytes, font_name: str) -> tuple[bytes, int, int]:
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return xml_bytes, 0, 0

    font_changes = 0
    size_changes = 0

    for elem in root.iter():
        if "typeface" in elem.attrib and elem.get("typeface") != font_name:
            elem.set("typeface", font_name)
            font_changes += 1

        if elem.tag not in PROP_TAGS:
            continue

        if "sz" in elem.attrib:
            new_size = nearest_even_point(elem.attrib["sz"])
            if elem.attrib["sz"] != new_size:
                elem.set("sz", new_size)
                size_changes += 1

        for child_name in ("latin", "ea", "cs"):
            if ensure_font_child(elem, child_name, font_name):
                font_changes += 1

    if font_changes or size_changes:
        return ET.tostring(root, encoding="utf-8", xml_declaration=True), font_changes, size_changes
    return xml_bytes, 0, 0


def normalize_pptx(src: Path, out: Path, font_name: str) -> None:
    if not src.exists():
        raise FileNotFoundError(src)

    out.parent.mkdir(parents=True, exist_ok=True)
    total_font_changes = 0
    total_size_changes = 0
    processed_xml = 0

    with tempfile.TemporaryDirectory() as tmp:
        tmp_out = Path(tmp) / out.name
        with zipfile.ZipFile(src, "r") as zin, zipfile.ZipFile(tmp_out, "w", zipfile.ZIP_DEFLATED) as zout:
            for info in zin.infolist():
                data = zin.read(info.filename)
                if info.filename.startswith("ppt/") and info.filename.endswith(".xml"):
                    data, font_changes, size_changes = normalize_xml(data, font_name)
                    total_font_changes += font_changes
                    total_size_changes += size_changes
                    if font_changes or size_changes:
                        processed_xml += 1
                zout.writestr(info, data)
        shutil.move(str(tmp_out), out)

    print(out)
    print(f"processed_xml={processed_xml}")
    print(f"font_changes={total_font_changes}")
    print(f"size_changes={total_size_changes}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize PPTX font family and snap sizes to nearest even points.")
    parser.add_argument("input", type=Path, help="Source .pptx")
    parser.add_argument("output", type=Path, help="Output .pptx")
    parser.add_argument("--font", default="Noto Sans CJK SC", help="Font family to apply to all text")
    args = parser.parse_args()

    normalize_pptx(args.input, args.output, args.font)


if __name__ == "__main__":
    main()
