import xml.etree.ElementTree as ET
from pathlib import Path

ET.register_namespace("", "http://www.w3.org/2000/svg")
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")


class VectorEditor:
    def __init__(self, filepath: Path):
        self.filepath = filepath
        try:
            self.tree = ET.parse(filepath)
            self.root = self.tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            self.root = ET.Element("svg")
            self.tree = ET.ElementTree(self.root)

    @classmethod
    def create_canvas(cls, filepath: Path, width: int, height: int, units: str = "px"):
        editor = cls(filepath)
        editor.root.set("width", f"{width}{units}")
        editor.root.set("height", f"{height}{units}")
        editor.root.set("xmlns", "http://www.w3.org/2000/svg")
        editor.root.set("xmlns:xlink", "http://www.w3.org/1999/xlink")

        # Add a white background rectangle
        rect_attrs = {
            "x": "0",
            "y": "0",
            "width": "100%",
            "height": "100%",
            "fill": "white",
        }
        ET.SubElement(editor.root, "rect", rect_attrs)

        editor.save()
        return editor

    def add_rect(self, x, y, width, height, fill, stroke, stroke_width):
        rect_attrs = {
            "x": str(x),
            "y": str(y),
            "width": str(width),
            "height": str(height),
            "fill": fill,
            "stroke": stroke,
            "stroke-width": str(stroke_width),
        }
        ET.SubElement(self.root, "rect", rect_attrs)

    def save(self):
        self.tree.write(self.filepath, encoding="utf-8", xml_declaration=True)
