# MenuTitle: Text holder
# -*- coding: utf-8 -*-
# This sets the menu title in Glyphs App and declares the script encoding as UTF-8.

__doc__ = """
Text holder.
"""
# Text holder.

import os
from GlyphsApp import *
from vanilla import *
from AppKit import NSWindow, NSFloatingWindowLevel  # Import necessary modules for window level control

# Define the file path
file_path = os.path.join(GSGlyphsInfo.applicationSupportPath(), "Text holder.txt")

class TextHolderWindow:
    def __init__(self):
        # Load the existing content from the file
        self.content = self.load_file_content()

        # Create the main window, allowing it to be resizable
        self.w = Window((500, 400), "Text Holder", minSize=(500, 400), maxSize=(1200, 800), autosaveName="TextHolderWindow")

        # Position the window at the top-left of the screen
        self.w.getNSWindow().setFrameOrigin_((0, 500))

        # Make the window stay on top of other windows
        self.w.getNSWindow().setLevel_(NSFloatingWindowLevel)

        # Add a text editor box
        self.w.textEditor = TextEditor((10, 10, -10, -150), self.content)

        # Add Find and Replace labels and fields
        self.w.findLabel = TextBox((10, -130, 50, 20), "Find:")
        self.w.findText = EditText((60, -130, -10, 20), placeholder="Text to find")

        self.w.replaceLabel = TextBox((10, -100, 50, 20), "Replace:")
        self.w.replaceText = EditText((60, -100, -10, 20), placeholder="Replacement text")

        # Add Find button (finds and highlights the text)
        self.w.findButton = Button((165, -70, 150, 30), "Find", callback=self.find_text)

        # Add Find & Replace button
        self.w.replaceButton = Button((10, -70, 150, 30), "Find & Replace", callback=self.find_and_replace)

        # Add Save button (saves without closing the window)
        self.w.saveButton = Button((10, -40, 150, 30), "Save", callback=self.save_content)

        # Add buttons for Save & Close and Ignore & Close
        self.w.saveCloseButton = Button((-335, -40, 150, 30), "Save & Close", callback=self.save_and_close)
        self.w.ignoreButton = Button((-180, -40, 150, 30), "Ignore & Close", callback=self.ignore_and_close)

        # Open the window
        self.w.open()

    def load_file_content(self):
        """Load the content of the file if it exists."""
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return file.read()
        else:
            return ""

    def find_text(self, sender):
        """Find and highlight text in the main window."""
        find_text = self.w.findText.get()
        text_editor = self.w.textEditor.getNSTextView()
        content = self.w.textEditor.get()

        if find_text:
            # Find the range of the first occurrence of the text
            range_start = content.find(find_text)
            if range_start != -1:
                # Highlight the found text
                range_length = len(find_text)
                text_editor.setSelectedRange_((range_start, range_length))
                text_editor.scrollRangeToVisible_((range_start, range_length))
            else:
                print("Text not found.")

    def find_and_replace(self, sender):
        """Find and replace text in the selected area or entire content."""
        find_text = self.w.findText.get()
        replace_text = self.w.replaceText.get()
        text_editor = self.w.textEditor.getNSTextView()

        # Get the selected range
        selected_range = text_editor.selectedRange()
        content = self.w.textEditor.get()

        if find_text:
            if selected_range.length > 0:
                # Operate on selected text
                selected_text = content[selected_range.location:selected_range.location + selected_range.length]
                new_selected_text = selected_text.replace(find_text, replace_text)
                # Replace the selected text
                text_editor.textStorage().replaceCharactersInRange_withString_(selected_range, new_selected_text)
            else:
                # Operate on the entire content
                new_content = content.replace(find_text, replace_text)
                self.w.textEditor.set(new_content)

    def save_content(self, sender):
        """Save the content of the window without closing it."""
        content = self.w.textEditor.get()
        with open(file_path, 'w') as file:
            file.write(content)
        print("Content saved.")

    def save_and_close(self, sender):
        """Save the content to the file and close the window."""
        self.save_content(sender)
        self.w.close()

    def ignore_and_close(self, sender):
        """Ignore changes and close the window."""
        self.w.close()

# Instantiate and open the window
TextHolderWindow()
