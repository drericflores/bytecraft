# bytecraft
A lightweight Hex editor
ByteCraft Hex Editor
 Project History and User Manual

Created by: Dr. Eric O. Flores
CajaRota Tech Solutions
September 2024
GNU General Public License v3.0 (GPL-3.0) Statement
ByteCraft Hex Editor is licensed under the GNU General Public License version 3 (GPL-3.0). This means that you are free to use, modify, and distribute this software, provided that any distributed version (modified or unmodified) also remains under the GPL-3.0 license.
The full terms of the GPL-3.0 ensure that ByteCraft, as open-source software, remains free and accessible to all, promoting collaborative improvement and innovation. By using ByteCraft, you acknowledge and agree to the terms set out in the GPL-3.0 license.
For more details, refer to the full license at:  https://www.gnu.org/licenses/gpl-3.0.html
Project Overview
ByteCraft is a powerful and user-friendly hex editor designed to handle binary file editing and text manipulation. Released under GPLv3 license, ByteCraft enables users to view, edit, and modify the contents of binary files in both hex and ASCII formats. It features a clean interface with intuitive tools that allow users to easily navigate and manipulate file data.
Project History
The development of ByteCraft went through multiple stages, from a simple concept to a fully functional hex editor with split-view, highlighting, and various advanced features.
    1. Initial Concept
        ◦ The project started as a basic hex editor with minimal features using Tkinter in Python.
        ◦ The goal was to create an editor capable of handling binary files and displaying them in hex format.
          
    2. Transition to PyQt5
        ◦ To provide a more professional and feature-rich GUI, I decied to transition the application from Tkinter to PyQt5.
        ◦ PyQt5 offers more polished interface, allowing for better handling of text and hex editing.
    3. Feature Enhancements
        ◦ I introduced two-part editing screen, allowing one to view hex code on the left side and the corresponding text representation on the right side.
        ◦ Additional menu options were added to toggle between hex/text modes, making the tool more versatile.
          
    4. Highlighting Functionality:
        ◦ A key feature is the ability to highlight hex code when text is selected, and vice versa.
        ◦ This allowed for an intuitive link between hex data and the corresponding ASCII representation, greatly improving user experience.
          
    5. Tabular Hex Display:
        ◦ The tabular hex displays allows data to be reformatted into a tabular format with right-aligned hex values and monospaced fonts.
        ◦ This ensured that hex code is clearly presented, making it easier to follow, read, and edit the binary content.
          
    6. Final Release:
        ◦ Final release is version 3.1.  I will continue to work on this project and release new versions later on in a near future.
        ◦ The project is complete with a user-friendly menu system, search-and-replace functionality, and customization light/dark mode.
        ◦ While the software is released under the GPLv3 license for public use and modification. This application is specifically for out Pop!_OS Facebook community.
Technologies and GUI Interfaces Used:
    1. Programming Languages:
        ◦ Original Code: Created in C++ and then converted to Python3. 
        ◦ Python: A versatile and powerful language used to build the core functionality of the editor.
          
    2. GUI Framework:
        ◦ PyQt5: Chosen for its advanced widgets, flexibility, and professional look. It allowed for the implementation of a clean user interface with rich text editing features.
          
    3. File Handling:
        ◦ Binary and Text Editing: ByteCraft allows both binary file editing (in hex) and text file editing (in ASCII), using Python's built-in file handling capabilities.
          
    4. PDF Generation:
        ◦ ReportLab: Used for the printing functionality, allowing users to save content as PDF files.
          
    5. Cross-Platform Compatibility:
        ◦ ByteCraft works on Linux, Windows, and macOS platforms, making it accessible to a wide range of users.
Cross-Platform Compatibility 
Python-based applications, particularly those using PyQt5, refers to the ability to run the same codebase on multiple operating systems (Linux, Windows, macOS) without significant changes. PyQt5 provides bindings for the Qt framework, which is cross-platform by design. This allows the ByteCraft hex editor to run on Windows and macOS, as well as Linux, with minimal adjustments.
Here’s how ByteCraft can work on different platforms:
Cross-Platform Compatibility of ByteCraft
As a developer, my preference has always leaned toward Linux, particularly Pop!_OS, which serves as my go-to operating system on both my desktop and laptop. My choice of programming languages ranges from Basic, C, C++, to more recently, Python—a language I've been exploring for the past two years. Given my daily use of Linux, I have tailored ByteCraft to run seamlessly on this OS. However, I understand that many users operate across different platforms, including Windows and macOS, which led me to ensure ByteCraft can be cross-platform. While I don't regularly use Windows or macOS, I've made sure the tool can be adapted for those environments with relative ease. Here's how ByteCraft functions across these platforms:
Linux (Other Distros)
ByteCraft was developed primarily on Pop!_OS, a Linux distribution known for its developer-friendly tools and ease of use. Naturally, the tool runs flawlessly on Pop!_OS, and by extension, it should work without any issues on other major Linux distributions like Ubuntu, Debian, Fedora, and others.
How it Works:
Since ByteCraft relies on Python and PyQt5, which are both well-supported across all major Linux distributions, the transition from one Linux flavor to another is seamless. Linux's shared Unix-like architecture ensures that the core dependencies work consistently across these systems.
Steps to Run:
    1. Install Python and PyQt5: You can install both Python and PyQt5 through the distribution’s package manager. For example, on Ubuntu or Pop!_OS, you would run:
       In Terminal type:
       sudo apt install python3-pyqt5
    2. Platform-Specific Dependencies: Ensure that any platform-specific libraries (e.g., printing drivers) are installed and compatible with your Linux distribution.
User Manual: How to Use ByteCraft
1. Opening ByteCraft:
    • When you launch ByteCraft, you'll see the main window shown in one complete editing screen.  You can divided into two parts click on View and select Hex/Text Mode then the screen will be divided into two screens (hex on the left and text on the right) when you open a file.
    • By default, only the hex view is shown, and you can enable the split-view mode by navigating to the View menu.
2. Main Features:
    • Two-Part Editing Screen:
        ◦ The left side shows the file's hex values, while the right side shows the text equivalent. You can switch between the views or keep them both visible.
    • Hex/Text Toggle:
        ◦ Use the View menu to toggle between hex-only mode and split-view mode (Hex/Text Mode).
        ◦ In split-view mode, changes made in the hex side are immediately reflected in the text side and vice versa.
3. Editing Files:
    • Hex Editing:
        ◦ You can click on the left panel to edit the hex code directly.
        ◦ The values are displayed in a tabular format for easy navigation and editing.
    • Text Editing:
        ◦ You can also edit the text directly on the right side (when in split-view mode).
        ◦ ByteCraft will automatically highlight the corresponding hex value when text is selected, and vice versa.
4. Menu Options:
    • File Menu:
        ◦ New: Clears the editor for a new file.
        ◦ Open: Opens an existing file in either text or binary format.
        ◦ Save: Saves changes to the current file.
        ◦ Save As: Save the file under a new name or format (text/hex).
        ◦ Print: Offers options to print the file or save it as a PDF.
        ◦ Quit: Exits the application.
    • Edit Menu:
        ◦ Cut/Copy/Paste: Basic editing functionality to cut, copy, or paste text/hex.
        ◦ Undo/Redo: Allows reverting or redoing changes.
        ◦ Search: Enables you to search for specific text or hex values.
        ◦ Search and Replace: Find and replace functionality in both hex and text.
    • View Menu:
        ◦ Toggle Hex/ASCII Mode: Switch between hex and ASCII view.
        ◦ Hex/Text Mode: Enable or disable split-view.
        ◦ Light/Dark Mode: Switch between light and dark themes for the interface.
5. Search and Replace:
    • You can search for specific text or hex values in the Edit menu. Use the Search and Replace feature to find and substitute values easily.
6. Hex Highlighting:
    • When text is selected on the right side, ByteCraft will automatically highlight the matching hex value in yellow on the left side.
    • Similarly, if you select a hex value on the left, the corresponding text will be highlighted in light-green on the right side.
7. Saving Files:
    • You can save your changes in either binary or text format using the Save or Save As options. If you're editing a binary file, make sure to save it as a hex file.
8. Print as PDF:
    • Use the Print option to generate a PDF file of the contents for easy reference or sharing.
My Final Thoughts
While ByteCraft is a flexible and lightweight hex editor designed with both power users and beginners in mind. With its simple interface, advanced features like hex highlighting, search and replace, and split-view mode, ByteCraft is perfect for binary file editing, reverse engineering, and low-level file manipulation.
Developed using PyQt5 for professional-grade GUI and Python for backend logic, ByteCraft combines the simplicity of Python with the power of a robust GUI framework, offering a cross-platform solution for anyone needing a high-quality hex editor.  Released under GPLv3, ByteCraft is open for public use, modification, and distribution.
