"""
Send File Tab - UI for sending files
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
from network.sender import FileSender
from utils.helpers import discover_file_server_ip

class SendTab:
    def __init__(self, parent, root):
        self.parent = parent
        self.root = root
        self.selected_file = None
        self.sender = FileSender()  # Initialize FileSender

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

        # Browse button
        self.browse_button = ctk.CTkButton(
            file_section,
            text="Browse Files",
            command=self.browse_file,
            height=35
        )
        self.browse_button.pack(pady=(10, 15))

        # Connection section
        conn_section = ctk.CTkFrame(self.parent)
        conn_section.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            conn_section,
            text="Connection Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))

        # Host input
        host_frame = ctk.CTkFrame(conn_section)
        host_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(host_frame, text="Host:").pack(side="left", padx=(10, 5))
        self.host_entry = ctk.CTkEntry(host_frame, placeholder_text="Enter host address (or 'auto' for discovery)")
        self.host_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.host_entry.insert(0, "auto")

        # Port input
        port_frame = ctk.CTkFrame(conn_section)
        port_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(port_frame, text="Port:").pack(side="left", padx=(10, 5))
        self.port_entry = ctk.CTkEntry(port_frame, placeholder_text="9999", width=100)
        self.port_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.port_entry.insert(0, "9999")

        # Destination filename input
        dest_frame = ctk.CTkFrame(conn_section)
        dest_frame.pack(fill="x", padx=20, pady=(5, 15))

        ctk.CTkLabel(dest_frame, text="Destination Filename:").pack(side="left", padx=(10, 5))
        self.dest_filename_entry = ctk.CTkEntry(dest_frame, placeholder_text="Enter filename")
        self.dest_filename_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Send button
        self.send_button = ctk.CTkButton(
            self.parent,
            text="Send File",
            command=self.send_file,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.send_button.pack(pady=20)

        # Status label for sending
        self.send_status_var = tk.StringVar(value="Ready to send")
        self.send_status_label = ctk.CTkLabel(
            self.parent,
            textvariable=self.send_status_var,
            text_color="gray",
            font=ctk.CTkFont(size=12)
        )
        self.send_status_label.pack(pady=5)
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a file to send",
            filetypes=[("All Files", "*.*")]
        )
        if file_path:
            self.selected_file = file_path
            self.file_path_var.set(f"Selected file: {os.path.basename(file_path)}")
            # Always set destination filename to the selected file's basename (with extension)
            self.dest_filename_entry.delete(0, 'end')
            self.dest_filename_entry.insert(0, os.path.basename(file_path))

    def send_file(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file to send.")
            return

        if not self.dest_filename_entry.get().strip():
            messagebox.showerror("Error", "Please enter a destination filename.")
            return

        # Disable the send button during transfer
        self.send_button.configure(state="disabled")
        self.send_status_var.set("Sending file...")

        # Start the file sending in a separate thread
        threading.Thread(
            target=self._send_file_thread,
            daemon=True
        ).start()

    def _send_file_thread(self):
        try:
            host = self.host_entry.get().strip() or "auto"
            port = int(self.port_entry.get() or 9999)
            dest_filename = self.dest_filename_entry.get().strip()

            # Set up progress callback
            def progress_callback(progress):
                self.root.after(0, lambda p=progress: self.send_status_var.set(f"Sending... {p:.1f}%"))

            # Auto-discovery visual feedback
            if host == "auto":
                self.root.after(0, lambda: self.send_status_var.set("Discovering host on local network..."))
                discovered_host = discover_file_server_ip()
                if not discovered_host:
                    self.root.after(0, lambda: self.send_status_var.set("No file server found on local network."))
                    self.root.after(0, lambda: self.send_button.configure(state="normal"))
                    return
                self.root.after(0, lambda: self.send_status_var.set(f"Discovered host: {discovered_host}"))
                host = discovered_host

            # Send the file
            self.sender.send_file(
                self.selected_file,
                host,
                port,
                dest_filename,
                progress_callback
            )

            # Update UI on success
            self.root.after(0, lambda: self.send_status_var.set("File sent successfully!"))
            self.root.after(0, lambda: messagebox.showinfo("Success", f"File sent successfully as '{dest_filename}'"))

        except Exception as e:
            self.root.after(0, lambda: self.send_status_var.set(f"Error: {str(e)}"))
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to send file: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.send_button.configure(state="normal"))