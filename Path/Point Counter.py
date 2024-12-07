# MenuTitle: Point Counter
# -*- coding: utf-8 -*-

__doc__ = """
Point Counter.
"""

from GlyphsApp import Glyphs
import vanilla

font = Glyphs.font

# Initialize a list to store the results
results = []

# Iterate through selected layers in the font
for selection in font.selectedLayers:
    # Iterate through layers of the selected glyph
    for layer in selection.parent.layers:
        # Process only master layers
        if not layer.isMasterLayer:
            continue

        # Initialize counters
        countPaths = len(layer.paths)
        countOffcurves = 0
        countCurves = 0
        countLines = 0

        # Iterate through paths in the layer
        for path in layer.paths:
            for node in path.nodes:
                if node.type == "offcurve":
                    countOffcurves += 1
                elif node.type == "curve":
                    countCurves += 1
                elif node.type == "line":
                    countLines += 1

        # Calculate total points and nodes
        countPoints = countCurves + countOffcurves + countLines
        countNodes = countPoints - countOffcurves

        # Append the result to the list
        results.append(f"Layer: {layer.name}\nTotal: {countPoints} Points - {countOffcurves} Handles, {countNodes} Nodes, {countPaths} Paths\n")


# Open the window
w = vanilla.Window((400, 300), "Point Counter")
w.textBox = vanilla.TextEditor((10, 10, -10, -10), "\n".join(results), readOnly=True)
w.open()
