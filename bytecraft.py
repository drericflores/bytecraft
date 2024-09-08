import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QFileDialog, QTextEdit,
                             QMessageBox, QDialog, QLabel, QVBoxLayout, QInputDialog,
                             QPlainTextEdit, QMenu, QMenuBar, QSplitter, QWidget)
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from reportlab.pdfgen import canvas
import tempfile
import platform
import os

class HexEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Byte Craft")
        self.setGeometry(100, 100, 800, 600)

        # Data members
        self.file_data = bytearray()
        self.current_file_path = ""
        self.is_hex_mode = True
        self.dark_mode_enabled = False
        self.is_split_view_enabled = False  # New state for split view

        # Create Split View
        self.splitter = QSplitter(Qt.Horizontal, self)
        self.hex_view = QPlainTextEdit(self.splitter)
        self.text_view = QPlainTextEdit(self.splitter)
        self.text_view.setReadOnly(True)  # Make text view non-editable
        self.setCentralWidget(self.splitter)

        # Hex view configuration - monospaced font
        monospaced_font = QFont("Courier", 10)
        self.hex_view.setFont(monospaced_font)

        # Initially hide text view, only hex is shown
        self.text_view.hide()

        # Connect selection signals
        self.hex_view.cursorPositionChanged.connect(self.on_hex_selection)
        self.text_view.cursorPositionChanged.connect(self.on_text_selection)

        # Menu bar setup
        self.create_menu()

    def create_menu(self):
        # Menu bar
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu('File')
        new_action = QAction('New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.on_menu_file_new)
        file_menu.addAction(new_action)

        open_action = QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.on_menu_file_open)
        file_menu.addAction(open_action)

        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.on_menu_file_save)
        file_menu.addAction(save_action)

        save_as_action = QAction('Save As', self)
        save_as_action.setShortcut('Ctrl+Shift+S')
        save_as_action.triggered.connect(self.on_menu_file_save_as)
        file_menu.addAction(save_as_action)

        print_action = QAction('Print', self)
        print_action.setShortcut('Ctrl+P')
        print_action.triggered.connect(self.on_menu_file_print)
        file_menu.addAction(print_action)

        close_action = QAction('Close', self)
        close_action.setShortcut('Ctrl+F4')
        close_action.triggered.connect(self.on_menu_file_close)
        file_menu.addAction(close_action)

        file_menu.addSeparator()

        quit_action = QAction('Quit', self)
        quit_action.triggered.connect(self.on_menu_file_quit)
        file_menu.addAction(quit_action)

        # Edit Menu
        edit_menu = menu_bar.addMenu('Edit')
        cut_action = QAction('Cut', self)
        cut_action.setShortcut('Ctrl+X')
        cut_action.triggered.connect(self.on_menu_edit_cut)
        edit_menu.addAction(cut_action)

        copy_action = QAction('Copy', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(self.on_menu_edit_copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction('Paste', self)
        paste_action.setShortcut('Ctrl+V')
        paste_action.triggered.connect(self.on_menu_edit_paste)
        edit_menu.addAction(paste_action)

        undo_action = QAction('Undo', self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(self.on_menu_edit_undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction('Redo', self)
        redo_action.setShortcut('Ctrl+Y')
        redo_action.triggered.connect(self.on_menu_edit_redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        search_action = QAction('Search', self)
        search_action.triggered.connect(self.on_menu_edit_search)
        edit_menu.addAction(search_action)

        search_replace_action = QAction('Search and Replace', self)
        search_replace_action.triggered.connect(self.on_menu_edit_search_replace)
        edit_menu.addAction(search_replace_action)

        # View Menu
        view_menu = menu_bar.addMenu('View')
        toggle_action = QAction('Toggle Hex/ASCII Mode', self)
        toggle_action.triggered.connect(self.on_toggle_ascii_hex)
        view_menu.addAction(toggle_action)

        light_dark_action = QAction('Light/Dark Mode', self)
        light_dark_action.triggered.connect(self.on_toggle_light_dark_mode)
        view_menu.addAction(light_dark_action)

        # New Hex/Text Split Mode toggle
        hex_text_mode_action = QAction('Hex/Text Mode', self)
        hex_text_mode_action.triggered.connect(self.on_toggle_hex_text_mode)
        view_menu.addAction(hex_text_mode_action)

        # Help Menu
        help_menu = menu_bar.addMenu('Help')
        about_action = QAction('About', self)
        about_action.triggered.connect(self.on_menu_help_about)
        help_menu.addAction(about_action)

    # New file functionality
    def on_menu_file_new(self):
        """Clear the editor to create a new file."""
        self.hex_view.clear()
        self.text_view.clear()
        self.file_data = bytearray()

    # Open file functionality
    def on_menu_file_open(self):
        """Open a file and load it into the editor."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All files (*.*);;Text files (*.txt)")
        if file_path:
            self.load_file(file_path)

    # Save file functionality
    def on_menu_file_save(self):
        """Save the current file."""
        if self.current_file_path:
            self.save_file(self.current_file_path)
        else:
            self.on_menu_file_save_as()

    # Save As functionality
    def on_menu_file_save_as(self):
        """Save the file with a new name."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text files (*.txt);;Hex files (*.hex);;All files (*.*)")
        if file_path:
            if file_path.endswith('.txt'):
                self.save_as_text(file_path)
            else:
                self.save_file(file_path)

    # Print functionality to save as PDF or print
    def on_menu_file_print(self):
        """Print the content or save it as PDF."""
        printer = QPrinter(QPrinter.HighResolution)
        print_dialog = QPrintDialog(printer, self)
        if print_dialog.exec_() == QPrintDialog.Accepted:
            self.hex_view.print_(printer)

    # Close functionality
    def on_menu_file_close(self):
        """Close the current file."""
        self.hex_view.clear()
        self.text_view.clear()
        self.file_data = bytearray()
        self.current_file_path = ""

    def on_menu_file_quit(self):
        """Quit the application."""
        self.close()

    # Cut functionality
    def on_menu_edit_cut(self):
        """Cut selected text from the hex view."""
        self.hex_view.cut()

    # Copy functionality
    def on_menu_edit_copy(self):
        """Copy selected text from the hex view."""
        self.hex_view.copy()

    # Paste functionality
    def on_menu_edit_paste(self):
        """Paste text into the hex view."""
        self.hex_view.paste()

    # Undo functionality
    def on_menu_edit_undo(self):
        """Undo the last edit."""
        self.hex_view.undo()

    # Redo functionality
    def on_menu_edit_redo(self):
        """Redo the last undone action."""
        self.hex_view.redo()

    # Search functionality
    def on_menu_edit_search(self):
        """Search for a text or hex value in the file."""
        search_str, ok = QInputDialog.getText(self, "Search", "Enter text or hex value to search:")
        if ok and search_str:
            self.perform_search(search_str)

    # Search and Replace functionality
    def on_menu_edit_search_replace(self):
        """Search and replace text or hex values."""
        find_str, ok = QInputDialog.getText(self, "Find", "Enter the text or hex value to find:")
        if ok and find_str:
            replace_str, ok = QInputDialog.getText(self, "Replace", "Enter the replacement text or hex value:")
            if ok and replace_str:
                self.find_and_replace(find_str, replace_str)

    # Toggle between Hex and ASCII modes
    def on_toggle_ascii_hex(self):
        """Toggle between Hex and ASCII view."""
        self.is_hex_mode = not self.is_hex_mode
        self.refresh_hex_view()

    # Toggle light and dark mode
    def on_toggle_light_dark_mode(self):
        """Toggle between light and dark modes."""
        self.dark_mode_enabled = not self.dark_mode_enabled
        self.apply_css_theme()

    # Toggle Hex/Text split mode
    def on_toggle_hex_text_mode(self):
        """Toggle between Hex/Text split view and single view."""
        self.is_split_view_enabled = not self.is_split_view_enabled
        if self.is_split_view_enabled:
            self.text_view.show()
            self.refresh_text_view()  # Show text view when split mode is enabled
        else:
            self.text_view.hide()

    def load_file(self, file_path):
        """Load file content into the editor."""
        self.current_file_path = file_path
        if file_path.endswith('.txt'):
            with open(file_path, 'r') as file:
                file_content = file.read()
                self.hex_view.setPlainText(file_content)
                self.file_data = bytearray(file_content.encode())
        else:
            with open(file_path, 'rb') as file:
                self.file_data = bytearray(file.read())
            self.refresh_hex_view()

    def save_file(self, file_path):
        """Save the file as binary content."""
        with open(file_path, 'wb') as file:
            file.write(self.file_data)
        self.current_file_path = file_path

    def save_as_text(self, file_path):
        """Save the file as plain text."""
        with open(file_path, 'w') as file:
            file.write(self.hex_view.toPlainText())
        self.current_file_path = file_path

    def refresh_hex_view(self):
        """Refresh the hex view and format it in a tabular layout."""
        if self.is_hex_mode:
            display_text = ""
            for i in range(0, len(self.file_data), 16):
                # Add address offset at the start of each line
                display_text += f"{i:08x}: "

                # Show hex values
                hex_chunk = ' '.join(f"{byte:02x}" for byte in self.file_data[i:i+16])
                display_text += hex_chunk.ljust(48)  # Adjust spacing for alignment

                # Add ASCII representation
                ascii_chunk = ''.join(chr(byte) if 32 <= byte <= 126 else '.' for byte in self.file_data[i:i+16])
                display_text += f"  |{ascii_chunk}|\n"

            self.hex_view.setPlainText(display_text)
        else:
            try:
                display_text = self.file_data.decode('ascii')
            except UnicodeDecodeError:
                display_text = self.file_data.decode('ascii', errors='replace')
            self.hex_view.setPlainText(display_text)

        if self.is_split_view_enabled:
            self.refresh_text_view()  # Update text view when in split mode

    def refresh_text_view(self):
        """Refresh the text view with the original ASCII representation."""
        try:
            display_text = self.file_data.decode('ascii')
        except UnicodeDecodeError:
            display_text = self.file_data.decode('ascii', errors='replace')
        self.text_view.setPlainText(display_text)

    def perform_search(self, search_str):
        """Perform a search in hex or ASCII mode."""
        search_bytes = bytearray.fromhex(search_str) if self.is_hex_mode else search_str.encode()
        index = self.file_data.find(search_bytes)
        if index != -1:
            cursor = self.hex_view.textCursor()
            cursor.setPosition(index)
            self.hex_view.setTextCursor(cursor)
        else:
            QMessageBox.information(self, "Result", "No match found.")

    def find_and_replace(self, find_str, replace_str):
        """Find and replace hex or ASCII values."""
        find_bytes = bytearray.fromhex(find_str) if self.is_hex_mode else find_str.encode()
        replace_bytes = bytearray.fromhex(replace_str) if self.is_hex_mode else replace_str.encode()

        self.file_data = self.file_data.replace(find_bytes, replace_bytes)
        self.refresh_hex_view()

    def apply_css_theme(self):
        """Apply the appropriate CSS theme for light or dark mode."""
        if self.dark_mode_enabled:
            self.hex_view.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4;")
            self.text_view.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4;")
        else:
            self.hex_view.setStyleSheet("background-color: white; color: black;")
            self.text_view.setStyleSheet("background-color: white; color: black;")

    # Highlight matching hex in hex_view when text is selected
    def on_text_selection(self):
        """Highlight the corresponding hex when text is selected in the text view."""
        cursor = self.text_view.textCursor()
        selected_text = cursor.selectedText()

        if selected_text:
            selected_bytes = selected_text.encode()
            hex_index = self.file_data.find(selected_bytes)
            if hex_index != -1:
                self.highlight_hex(hex_index, len(selected_bytes))

    # Highlight matching text in text_view when hex is selected
    def on_hex_selection(self):
        """Highlight the corresponding text when hex is selected in the hex view."""
        cursor = self.hex_view.textCursor()
        selected_hex = cursor.selectedText().strip().replace(" ", "")

        if selected_hex:
            try:
                selected_bytes = bytearray.fromhex(selected_hex)
                text_index = self.file_data.find(selected_bytes)
                if text_index != -1:
                    self.highlight_text(text_index, len(selected_bytes))
            except ValueError:
                pass  # Ignore invalid hex selection

    def highlight_hex(self, start, length):
        """Highlight the selected hex code."""
        self.clear_highlights(self.hex_view)
        cursor = self.hex_view.textCursor()
        cursor.setPosition(start * 3)  # Adjust for hex formatting (3 chars per byte)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, length * 3)

        fmt = QTextCharFormat()
        fmt.setBackground(QColor("yellow"))
        cursor.setCharFormat(fmt)

    def highlight_text(self, start, length):
        """Highlight the selected text."""
        self.clear_highlights(self.text_view)
        cursor = self.text_view.textCursor()
        cursor.setPosition(start)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, length)

        fmt = QTextCharFormat()
        fmt.setBackground(QColor("lightgreen"))
        cursor.setCharFormat(fmt)

    def clear_highlights(self, view):
        """Clear all highlights in the given view."""
        cursor = view.textCursor()
        cursor.select(QTextCursor.Document)
        fmt = QTextCharFormat()
        cursor.setCharFormat(fmt)

    def on_menu_help_about(self):
        """Display the About dialog."""
        about_text = (
            "ByteCraft\n"
            "Version 3.1\n"
            "September 2024\n\n"
            "ByteCraft is a small and lightweight Hex Editing Application.\n\n"
            "Technologies: Python, PyQt5, ReportLab, Tempfile, Platform\n\n"
            "Copyright 2024 - CajaRota Tech Solutions.\n"
            "GNU General Public License, Version 3 or Later\n\n"
            "Credits:\n"
            "Created by Dr. Eric O. Flores"
        )
        QMessageBox.about(self, "About ByteCraft", about_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    hex_editor = HexEditor()
    hex_editor.show()
    sys.exit(app.exec_())
