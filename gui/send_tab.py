"""
Send File Tab - UI for sending files
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
# from network.sender import FileSender

class SendTab:
    def __init__(self, parent, root):
        self.parent = parent
        self.root = root
        self.selected_file = None
        self.sender = None

        self.setup_ui()

    def setup_ui(self):
        # File selection frame
        file_section = ctk.CTkFrame(self.parent)
        file_section.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(
            file_section,
            text="Select file to send",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))

        # File path display
        self.file_path_var = tk.StringVar(value="No file selected")
        self.file_path_label = ctk.CTkLabel(
            file_section,
            textvariable=self.file_path_var,
            wraplength=400,
        )
        self.file_path_label.pack(pady=5)