from GlyphsApp import Glyphs, Message
# from GlyphsApp.plugins import *
import traceback


class BrokenMetricsFinder:
    def __init__(self):
        self.font = Glyphs.font
        self.brokenGlyphs = []

    def find_broken_linked_metrics(self):
        """Find glyphs with broken or invalid metrics links"""
        for glyph in self.font.glyphs:
            try:
                # Check left, right, and width metrics keys
                leftKey = glyph.leftMetricsKey
                rightKey = glyph.rightMetricsKey
                widthKey = glyph.widthMetricsKey

                # Validate left metrics key
                if leftKey and not self.is_valid_metrics_key(leftKey):
                    self.brokenGlyphs.append(glyph.name)
                    continue  # Move to the next glyph if this one is broken

                # Validate right metrics key
                if rightKey and not self.is_valid_metrics_key(rightKey):
                    self.brokenGlyphs.append(glyph.name)
                    continue  # Move to the next glyph if this one is broken

                # Validate width metrics key
                if widthKey and not self.is_valid_metrics_key(widthKey):
                    self.brokenGlyphs.append(glyph.name)
                    continue  # Move to the next glyph if this one is broken

            except Exception as e:
                # Log any unexpected issues during metrics processing
                print(f"Error processing {glyph.name}: {e}")
                traceback.print_exc()

    def is_valid_metrics_key(self, key):
        """Check if the given metrics key is valid"""
        # Strip off any '=' and whitespace
        key = key.strip()

        # Allow any key that starts with =| as valid
        if key.startswith("=|"):
            return True

        # Strip leading '=' if present for glyph reference
        if key.startswith("="):
            key = key[1:]  # Remove the '=' at the start

        # Ignore valid special cases like /= and * (these are allowed for glyph metrics references)
        if key in ["|", "/", "*", "==", "!="]:
            return True

        # Check if the remaining part is a valid glyph name in the font
        return key in [g.name for g in self.font.glyphs]

    def open_new_tab_with_broken_glyphs(self):
        """Open a new tab and show glyphs with broken metrics links"""
        if not self.brokenGlyphs:
            Message("No broken linked metrics", "All glyphs seem to have valid metrics links.")
        else:
            tab_text = "/%s" % "/".join(self.brokenGlyphs)
            self.font.newTab(tab_text)


def show_broken_linked_metrics():
    """Main function to find and display broken linked metrics"""
    metrics_finder = BrokenMetricsFinder()
    metrics_finder.find_broken_linked_metrics()
    metrics_finder.open_new_tab_with_broken_glyphs()


# Run the function
show_broken_linked_metrics()
