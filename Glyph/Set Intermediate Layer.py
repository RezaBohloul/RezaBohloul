# MenuTitle: Set Intermediate Layer
# -*- coding: utf-8 -*-


from GlyphsApp import Glyphs
import vanilla

__doc__ = """
Set Intermediate Layer.
"""


class UserInputDialog(object):
    def __init__(self):
        self.w = vanilla.FloatingWindow((200, 70), "Input Value")
        self.w.textBox = vanilla.EditText((10, 10, -10, 20), "800")
        self.w.okButton = vanilla.Button((10, 40, -10, 20), "OK", callback=self.okCallback)
        self.w.open()

    def okCallback(self, sender):
        try:
            self.user_input = int(self.w.textBox.get())
        except ValueError:
            self.user_input = 700  # Default to 700 if invalid input
        self.w.close()

        # Now, run the rest of your script with the user input
        self.runScript()

    def runScript(self):
        font = Glyphs.font
        currentTab = font.currentTab

        # Store the existing layers in the current tab (to keep the view)
        if currentTab:
            existingLayers = list(currentTab.layers)  # Copy the existing layers

        # Loop through each selected glyph
        for i, layer in enumerate(font.selectedLayers):
            glyph = layer.parent

            # Duplicate the selected layer
            newLayer = layer.copy()

            # Add the new layer to the glyph's layers
            glyph.layers.append(newLayer)

            # Name the new layer "New Layer"
            newLayer.name = "New Layer"

            # Set the custom attribute "coordinates" with the user input
            newLayer.attributes["coordinates"] = {"a01": self.user_input}

            # Re-interpolate the new layer
            newLayer.reinterpolate()

            # Update the existing layer in its original position
            if currentTab:
                for j, existingLayer in enumerate(existingLayers):
                    if existingLayer.parent == glyph:
                        existingLayers[j] = newLayer  # Replace the original layer with the new one

        # Reassign the modified list back to the current tab to keep the original order
        if currentTab:
            currentTab.layers = existingLayers

        # Update the UI to reflect the change
        Glyphs.redraw()


# Instantiate and show the dialog
UserInputDialog()
