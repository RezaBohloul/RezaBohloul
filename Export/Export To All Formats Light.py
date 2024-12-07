# MenuTitle: Export To All Formats Light
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import os
from vanilla import FloatingWindow, Button
from GlyphsApp import Glyphs, INSTANCETYPEVARIABLE

__doc__ = """
Always export to all formats.
"""

Glyphs.clearLog()


class ExportToAllFormats:
    def __init__(self):
        # Window settings
        window_width, window_height = 180, 40
        margin = 10

        # Create the window
        self.w = FloatingWindow((window_width, window_height), "Export")

        # Run button
        self.w.runButton = Button((margin, 10, -margin, 20), "Export All Formats", callback=self.exportFonts)

        self.exportPath = self.getFontFilePath()

        self.w.open()

    def getFontFilePath(self):
        currentFont = Glyphs.font
        if currentFont and currentFont.filepath:
            return os.path.dirname(currentFont.filepath)
        return None

    def createSubfolder(self, parentPath, subfolderName):
        """Create subfolder if it doesn't exist."""
        folderPath = os.path.join(parentPath, subfolderName)
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
        return folderPath

    def exportFonts(self, sender):
        # Ensure export path is set
        if not self.exportPath:
            print("No export path available. Please save the font first.")
            return

        print(f"Exporting to path: {self.exportPath}")

        # Only export the current font
        font = Glyphs.font
        if not font:
            print("No font available for export.")
            return

        useSubfolders = True  # Always use separate subfolders

        fontExportPath = self.createSubfolder(self.exportPath, font.familyName)

        # Export OTF, TTF, WEB, and Variable formats
        self.exportFontInstances(font, "OTF", fontExportPath, useSubfolders)
        self.exportFontInstances(font, "TTF", fontExportPath, useSubfolders)
        woffPath = self.createSubfolder(fontExportPath, "WOFF") if useSubfolders else fontExportPath
        woff2Path = self.createSubfolder(fontExportPath, "WOFF2") if useSubfolders else fontExportPath
        self.exportFontInstances(font, "WEB", fontExportPath, useSubfolders, woffPath=woffPath, woff2Path=woff2Path)
        variablePathTTF = self.createSubfolder(fontExportPath, "Variable/TTF") if useSubfolders else fontExportPath
        variablePathWOFF = self.createSubfolder(fontExportPath, "Variable/WOFF") if useSubfolders else fontExportPath
        variablePathWOFF2 = self.createSubfolder(fontExportPath, "Variable/WOFF2") if useSubfolders else fontExportPath
        self.exportFontInstances(font, "Variable", fontExportPath, useSubfolders, variableOnly=True, variablePaths={"TTF": variablePathTTF, "WOFF": variablePathWOFF, "WOFF2": variablePathWOFF2})

        Glyphs.showNotification("Export Complete", "The font was exported successfully.")

    def exportFontInstances(self, font, formatType, exportPath, useSubfolders, woffPath=None, woff2Path=None, variableOnly=False, variablePaths=None):
        """Exports the instances of a font in a specific format."""
        activeInstances = [inst for inst in font.instances if inst.active]

        for instance in activeInstances:
            instancePath = exportPath

            # Handle Variable instances
            if variableOnly:
                if instance.type != INSTANCETYPEVARIABLE:
                    continue
                # Export Variable as TTF, WOFF, and WOFF2
                if variablePaths:
                    instance.generate(Format="TTF", FontPath=variablePaths["TTF"], RemoveOverlap=True, AutoHint=False)
                    instance.generate(Format="TTF", FontPath=variablePaths["WOFF"], Containers=["WOFF"], RemoveOverlap=True, AutoHint=False)
                    instance.generate(Format="TTF", FontPath=variablePaths["WOFF2"], Containers=["WOFF2"], RemoveOverlap=True, AutoHint=False)
            elif formatType != "Variable" and instance.type == INSTANCETYPEVARIABLE:
                continue

            # Use subfolder if required
            if useSubfolders and formatType != "WEB":
                instancePath = self.createSubfolder(exportPath, formatType)

            # Export logic based on format type
            if formatType == "OTF":
                instance.generate(Format="OTF", FontPath=instancePath, RemoveOverlap=True, AutoHint=False)
            elif formatType == "TTF":
                instance.generate(Format="TTF", FontPath=instancePath, RemoveOverlap=True, AutoHint=False)
            elif formatType == "WEB":
                # Export WOFF
                if woffPath:
                    instance.generate(Format="TTF", FontPath=woffPath, Containers=["WOFF"], RemoveOverlap=True, AutoHint=False)
                # Export WOFF2
                if woff2Path:
                    instance.generate(Format="TTF", FontPath=woff2Path, Containers=["WOFF2"], RemoveOverlap=True, AutoHint=False)
            elif formatType == "Variable" and not variableOnly:
                instance.generate(Format="TTF", FontPath=instancePath, RemoveOverlap=True, AutoHint=False)


# Run the script
ExportToAllFormats()
