# MenuTitle: Magic Remover
# encoding: utf-8
from __future__ import division, print_function, unicode_literals
import traceback
from GlyphsApp import Glyphs, GSNode, GSAnchor, GSHint, GSComponent
from AppKit import NSEvent, NSEventModifierFlagCommand
from operator import itemgetter


def hintID(h):
    return (h.name, h.origin, h.target, h.other1, h.other2)


def backupAllLayersOfGlyph(glyph):
    for layer in glyph.layers:
        if layer.isMasterLayer:
            layer.contentToBackgroundCheckSelection_keepOldBackground_(False, False)
            layer.background = layer.background.copyDecomposedLayer()


def eraseSelectedItemsOnAllMasters():
    try:
        keysPressed = NSEvent.modifierFlags()
        shouldBackupFirst = keysPressed & NSEventModifierFlagCommand == NSEventModifierFlagCommand

        # get current font
        font = Glyphs.font
        if font:
            # We’re in the Edit View
            if font.currentTab and len(font.selectedLayers) == 1:
                currentLayer = font.selectedLayers[0]
                thisGlyph = currentLayer.parent
                if shouldBackupFirst:
                    backupAllLayersOfGlyph(thisGlyph)

                # collect selected items:
                pathNodeIndexes = []
                anchorNames = []
                componentIndexes = []
                hintIDs = []

                for thisItem in currentLayer.selection:
                    if isinstance(thisItem, GSNode):
                        pathNodeIndexes.append(
                            currentLayer.indexPathOfNode_(thisItem)
                        )
                    elif isinstance(thisItem, GSAnchor):
                        anchorNames.append(
                            thisItem.name
                        )
                    elif isinstance(thisItem, GSComponent):
                        componentIndexes.append(
                            thisItem.elementIndex()
                        )
                    elif isinstance(thisItem, GSHint):
                        if thisItem.isCorner:
                            hintIDs.append(
                                hintID(thisItem)
                            )

                # delete respective items on all (compatible) layers:
                if pathNodeIndexes or anchorNames or componentIndexes or hintIDs:

                    # reverse-sort path and node indexes
                    # so deletion of nodes does not mess with the indexes of the next node to be deleted
                    pathNodeIndexes = sorted(
                        pathNodeIndexes,
                        key=itemgetter(0, 1),
                        reverse=True,
                    )

                    currentCS = currentLayer.compareString()
                    allCompatibleLayers = [
                        layer for layer in thisGlyph.layers
                        if (layer.isMasterLayer or layer.isSpecialLayer)
                        and (layer.compareString() == currentCS)
                    ]

                    thisGlyph.beginUndo()  # begin undo grouping
                    removePaths = list()
                    for thisLayer in allCompatibleLayers:
                        removeNodes = list()
                        for pathNodeIndex in pathNodeIndexes:
                            node = thisLayer.nodeAtIndexPath_(pathNodeIndex)
                            removeNodes.append(node)
                        if len(removeNodes) == 1:
                            node = removeNodes[0]
                            path = node.parent
                            path.removeNodeCheckKeepShape_normalizeHandles_(node, True)
                            if len(path) == 0:
                                removePaths.append(path)
                        else:
                            for node in removeNodes:
                                path = node.parent
                                if path is None or node not in path.nodes:  # can be removed already
                                    continue
                                path.removeNodeCheckKeepShape_normalizeHandles_(node, True)
                                if len(path.nodes) == 0:
                                    removePaths.append(path)
                        for anchorName in anchorNames:
                            thisLayer.removeAnchorWithName_(anchorName)
                        for componentIndex in sorted(componentIndexes, reverse=True):
                            if Glyphs.versionNumber >= 3:
                                # GLYPHS 3
                                del thisLayer.shapes[componentIndex]
                            else:
                                # GLYPHS 2
                                del thisLayer.components[componentIndex]

                        if hintIDs:
                            for hintIndex in sorted(range(len(thisLayer.hints)), reverse=True):
                                if hintID(thisLayer.hints[hintIndex]) in hintIDs:
                                    thisLayer.removeHint_(thisLayer.hints[hintIndex])
                    for path in removePaths:
                        path.parent.removeShape_(path)

                    thisGlyph.endUndo()   # end undo grouping

    except Exception as e:
        Glyphs.clearLog()  # clears macro window log
        print("Magic Remover Exception:")
        print(e)
        print("\nMagic Remover Traceback:")
        print(traceback.format_exc())


# Execute the function
eraseSelectedItemsOnAllMasters()
