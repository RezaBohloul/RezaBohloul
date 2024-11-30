# MenuTitle: Export To All Formats with Options
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import os
from vanilla import FloatingWindow, CheckBox, Button, TextBox, ProgressBar
from GlyphsApp import Glyphs, INSTANCETYPEVARIABLE
from vanilla.dialogs import getFolder

__doc__ = """
Export to all formats.
If “PS outlines” is off, TT outlines will be exported for the web formats.
"""

Glyphs.clearLog()


class ExportToAllFormats:
    def __init__(self):
        # Window settings
        window_width, window_height = 360, 215
        margin = 10

        # Create the window
        self.w = FloatingWindow((window_width, window_height), "Export to All Formats with Options")

        # UI Elements
        self.w.exportPathLabel = TextBox((margin, 10, 120, 20), "Export to:")
        self.w.exportPathText = TextBox((75, 10, -margin - margin, 20), "")
        self.w.changeExportPathButton = Button((-190 - margin, 130, -margin, 20), "Change Export Path", callback=self.selectExportPath)

        self.w.exportAllFonts = CheckBox((margin, 40, 150, 20), "Export all open fonts", value=False)
        self.w.subfoldersCheckBox = CheckBox((margin + 180, 40, 180, 20), "Separate subfolders", value=True)

        # Export format checkboxes
        self.w.exportOTF = CheckBox((margin, 70, 100, 20), "OTF", value=True)
        self.w.exportTTF = CheckBox((margin + 90, 70, 100, 20), "TTF", value=True)
        self.w.exportWEB = CheckBox((margin + 180, 70, 100, 20), "WEB", value=True)
        self.w.exportVariable = CheckBox((margin + 270, 70, 100, 20), "Variable", value=True)

        # Autohint, remove overlaps, PS outlines
        self.w.autohint = CheckBox((margin, 100, 150, 20), "Autohint", value=False)
        self.w.removeOverlaps = CheckBox((margin + 90, 100, 150, 20), "Remove overlaps", value=True)
        self.w.psOutlines = CheckBox((margin, 130, 150, 20), "PS Outlines for WEB", value=True)

        # Run button and progress bar
        self.w.runButton = Button((margin, 160, -margin, 20), "Export", callback=self.exportFonts)
        self.w.progressBar = ProgressBar((margin + 5, 185, -margin - 5, 20))

        # Set the export path to the font file location on initialization
        self.exportPath = self.getFontFilePath()
        if self.exportPath:
            self.w.exportPathText.set(self.exportPath)
        else:
            self.w.exportPathText.set("No font file loaded. Save font first.")

        self.w.open()

    def getFontFilePath(self):
        currentFont = Glyphs.font
        if currentFont and currentFont.filepath:
            return os.path.dirname(currentFont.filepath)
        return None

    def selectExportPath(self, sender):
        exportFolder = getFolder("Select Export Folder")
        if exportFolder:
            self.exportPath = exportFolder[0]
            self.w.exportPathText.set(self.exportPath)

    def createSubfolder(self, parentPath, subfolderName):
        """Create subfolder if it doesn't exist."""
        folderPath = os.path.join(parentPath, subfolderName)
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
        return folderPath

    def exportFonts(self, sender):
        # Ensure export path is set
        if not self.exportPath:
            print("No export path available. Please save the font first or select an export path.")
            return

        print(f"Exporting to path: {self.exportPath}")

        # Get selected fonts
        fonts = Glyphs.fonts if self.w.exportAllFonts.get() else [Glyphs.font]
        if not fonts:
            print("No fonts available for export.")
            return

        # Export formats
        exportOTF = self.w.exportOTF.get()
        exportTTF = self.w.exportTTF.get()
        exportWEB = self.w.exportWEB.get()
        exportVariable = self.w.exportVariable.get()
        useSubfolders = self.w.subfoldersCheckBox.get()

        autohint = self.w.autohint.get()
        removeOverlaps = self.w.removeOverlaps.get()
        psOutlines = self.w.psOutlines.get()

        totalFonts = len(fonts)
        progressStep = 100 / totalFonts
        currentProgress = 0

        for font in fonts:
            fontExportPath = self.createSubfolder(self.exportPath, font.familyName)

            # Export OTF
            if exportOTF:
                self.exportFontInstances(font, "OTF", fontExportPath, useSubfolders, autohint, removeOverlaps)

            # Export TTF
            if exportTTF:
                self.exportFontInstances(font, "TTF", fontExportPath, useSubfolders, autohint, removeOverlaps)

            # Export WEB (WOFF/WOFF2)
            if exportWEB:
                woffPath = self.createSubfolder(fontExportPath, "WOFF") if useSubfolders else fontExportPath
                woff2Path = self.createSubfolder(fontExportPath, "WOFF2") if useSubfolders else fontExportPath
                self.exportFontInstances(font, "WEB", fontExportPath, useSubfolders, autohint, removeOverlaps, woffPath=woffPath, woff2Path=woff2Path, psOutlines=psOutlines)

            # Export Variable (as TTF, WOFF, and WOFF2)
            if exportVariable:
                variablePathTTF = self.createSubfolder(fontExportPath, "Variable/TTF") if useSubfolders else fontExportPath
                variablePathWOFF = self.createSubfolder(fontExportPath, "Variable/WOFF") if useSubfolders else fontExportPath
                variablePathWOFF2 = self.createSubfolder(fontExportPath, "Variable/WOFF2") if useSubfolders else fontExportPath
                self.exportFontInstances(font, "Variable", fontExportPath, useSubfolders, autohint, removeOverlaps, variableOnly=True, variablePaths={"TTF": variablePathTTF, "WOFF": variablePathWOFF, "WOFF2": variablePathWOFF2})

            # Update progress
            currentProgress += progressStep
            self.w.progressBar.set(currentProgress)

        Glyphs.showNotification("Export Complete", "All fonts were exported successfully.")

    def exportFontInstances(self, font, formatType, exportPath, useSubfolders, autohint=False, removeOverlaps=True, woffPath=None, woff2Path=None, psOutlines=False, variableOnly=False, variablePaths=None):
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
                    instance.generate(Format="TTF", FontPath=variablePaths["TTF"], RemoveOverlap=removeOverlaps, AutoHint=autohint)
                    instance.generate(Format="TTF", FontPath=variablePaths["WOFF"], Containers=["WOFF"], RemoveOverlap=removeOverlaps, AutoHint=autohint)
                    instance.generate(Format="TTF", FontPath=variablePaths["WOFF2"], Containers=["WOFF2"], RemoveOverlap=removeOverlaps, AutoHint=autohint)
            elif formatType != "Variable" and instance.type == INSTANCETYPEVARIABLE:
                continue

            # Use subfolder if required
            if useSubfolders and formatType != "WEB":
                instancePath = self.createSubfolder(exportPath, formatType)

            # Export logic based on format type
            if formatType == "OTF":
                instance.generate(Format="OTF", FontPath=instancePath, RemoveOverlap=removeOverlaps, AutoHint=autohint)
            elif formatType == "TTF":
                instance.generate(Format="TTF", FontPath=instancePath, RemoveOverlap=removeOverlaps, AutoHint=autohint)
            elif formatType == "WEB":
                # Export WOFF
                if woffPath:
                    instance.generate(Format="TTF", FontPath=woffPath, Containers=["WOFF"], RemoveOverlap=removeOverlaps, AutoHint=autohint)
                # Export WOFF2
                if woff2Path:
                    instance.generate(Format="TTF", FontPath=woff2Path, Containers=["WOFF2"], RemoveOverlap=removeOverlaps, AutoHint=autohint)
            elif formatType == "Variable" and not variableOnly:
                instance.generate(Format="TTF", FontPath=instancePath, RemoveOverlap=removeOverlaps, AutoHint=autohint)


# Run the script
ExportToAllFormats()
