"""
Main window Setup and Configuration for File Transfer GUI
"""

import customtkinter as ctk
from .send_tab import SendTab
from .receive_tab import ReceiveTab


class FileTransferApp:
    def __init__(self):
        # Set appearance mode and color theme
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Create the main window
        self.root = ctk.CTk()
        self.root.title("File Transfer Tool")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        self.setup_ui()
    
    def setup_ui(self):
        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="File Transfer Tool",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 30))

        # Tab view for send/receive functionality
        self.tab_view = ctk.CTkTabview(main_frame, width=550, height=400)
        self.tab_view.pack(fill="both", expand=True, padx=20, pady=10)

        # Add tabs
        self.tab_view.add("Send File")
        self.tab_view.add("Receive File")

        # Initialize tab content
        self.send_tab = SendTab(self.tab_view.tab("Send File"), self.root)
        self.receive_tab = ReceiveTab(self.tab_view.tab("Receive File"), self.root)
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        # Clean up receive tabe if needed
        if hasattr(self.receive_tab, 'stop_receiving'):
            self.receive_tab.stop_receiving()
        self.root.destroy()

