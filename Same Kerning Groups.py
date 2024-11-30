# MenuTitle: Same Kerning Groups
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__ = """
Opens a new tab containing all members of the left and right kerning groups of the current glyph.
"""

from GlyphsApp import Glyphs, Message

thisFont = Glyphs.font  # frontmost font
thisGlyph = thisFont.selectedLayers[0].parent

if thisGlyph:
    leftGroup = thisGlyph.leftKerningGroup
    rightGroup = thisGlyph.rightKerningGroup

    leftGroupText = ""
    rightGroupText = ""

    # Check if the left kerning group is not empty
    if leftGroup:
        leftGroupText = "L: "
        for g in thisFont.glyphs:
            if g.leftKerningGroup == leftGroup and g != thisGlyph:
                leftGroupText += "/%s " % g.name

    # Check if the right kerning group is not empty
    if rightGroup:
        rightGroupText = "R: "
        for g in thisFont.glyphs:
            if g.rightKerningGroup == rightGroup and g != thisGlyph:
                rightGroupText += "/%s " % g.name

    # Create the new tab content
    tabText = "/%s\n" % thisGlyph.name
    if leftGroupText.strip() != "L:":
        tabText += leftGroupText.strip() + "\n"
    if rightGroupText.strip() != "R:":
        tabText += rightGroupText.strip() + "\n"

    if tabText.strip() != "/%s" % thisGlyph.name:
        thisFont.newTab(tabText)
    else:
        Message(title="No Kerning Groups", message="The selected glyph does not belong to any kerning group.", OKButton=None)
else:
    Message(title="Script Error", message="No glyph currently selected.", OKButton=None)
