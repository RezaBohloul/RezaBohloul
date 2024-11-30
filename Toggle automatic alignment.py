# MenuTitle: Toggle automatic alignment components
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__="""
Toggle automatic alignment for selected components in the Edit View, or for all components in all selected glyphs when nothing is selected.
"""

# ---------------------
# Variables
# ---------------------
f = Glyphs.font
selected_layers = f.selectedLayers
edit_view_selection = f.currentTab and f.currentTab.selectedLayers

# ---------------------
# Helper Functions
# ---------------------
def toggle_automatic_alignment_all_masters(layer, selected_components):
    for l in layer.parent.layers:  # Iterate through all masters
        for c in l.components:
            if not selected_components or c.name in [sc.name for sc in selected_components]:
                c.automaticAlignment = not c.automaticAlignment  # Toggle alignment

# ---------------------
# Engine
# ---------------------
for layer in selected_layers:
    if layer.isMasterLayer:
        # Check if there are selected components in the Edit View
        selected_components = [c for c in layer.components if c.selected]
        
        if selected_components:
            # Apply to selected components in the Edit View
            toggle_automatic_alignment_all_masters(layer, selected_components)
            alignment_state = "enabled" if selected_components[0].automaticAlignment else "disabled"
            print(layer.parent.name, layer.name, f"----- Automatic alignment {alignment_state} (selected components)")
        else:
            # Apply to all components if nothing is selected
            toggle_automatic_alignment_all_masters(layer, None)
            alignment_state = "enabled" if layer.components[0].automaticAlignment else "disabled"
            print(layer.parent.name, layer.name, f"----- Automatic alignment {alignment_state} (all components)")

# Pop-up notification
toggle_state = "Enabled" if selected_layers[0].components[0].automaticAlignment else "Disabled"
Glyphs.showNotification("Toggle automatic alignment", f"Automatic alignment {toggle_state} in all masters.")

# ---------------------
# Test
# ---------------------
print("Done!")
