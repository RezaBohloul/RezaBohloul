# MenuTitle: Broken Metrics Finder
# -*- coding: utf-8 -*-

from GlyphsApp import Glyphs, Message


def find_broken_linked_metrics(font):
    """Find glyphs with broken or invalid metrics links"""
    brokenGlyphs = []
    for glyph in font.glyphs:
        if glyph._metricsKeysInvalid():
            brokenGlyphs.append(glyph.name)

    if brokenGlyphs:
        tab_text = "/" + "/".join(brokenGlyphs)
        font.newTab(tab_text)
    else:
        Message("No broken linked metrics", "All glyphs seem to have valid metrics links.")


def show_broken_linked_metrics(font):
    """Main function to find and display broken linked metrics"""
    find_broken_linked_metrics(font)


# Run the function
show_broken_linked_metrics(Glyphs.font)
