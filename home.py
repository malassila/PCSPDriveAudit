import threading
import time
from tkinter import Image, messagebox
from tkinter.tix import IMAGETEXT
import traceback
import os

import customtkinter
import tkinter as tk
from tkinter import ttk 
import mysql.connector
from PIL import Image, ImageTk
# import customtkinter

# Local modules
import globals
from linux import get_all_connected



class DriveDashboard(customtkinter.CTk):

    APP_NAME = f"PCSP Drive Audit {globals.version}"
    WIDTH = 550
    HEIGHT = 100
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set Default Appearance Mode to Dark
        customtkinter.set_appearance_mode(globals.THEME)

        def top_frame():
            self.top_frame = customtkinter.CTkFrame(self, fg_color=globals.get_hex_color("dark_gray"))
            self.top_frame.pack(side="top", fill="x")
            
            self.search_frame = customtkinter.CTkFrame(self.top_frame, fg_color=globals.get_hex_color("dark_gray"))
            self.search_frame.pack(side='top', fill='x')
            
            self.search_entry = customtkinter.CTkEntry(self.search_frame, fg_color=globals.get_hex_color("dark_gray"), font=("Arial", 12), width=50)
            self.search_entry.pack(side='right', fill='x', expand=True)
            
            
            

        def connected_frame(parent):
            self.connected_frame = customtkinter.CTkFrame(parent, fg_color=globals.get_hex_color("dark_gray"), corner_radius=10)
            self.connected_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            
            self.label = customtkinter.CTkLabel(self.connected_frame, text="Connected", font=("Arial", 20), fg_color=globals.get_hex_color("dark_gray"))
            self.label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

            style = ttk.Style(self.connected_frame)
            style.theme_use("clam")
            style.configure("Treeview", background="gray10", foreground="#ffffff", fieldbackground="gray10", font=('Arial', 12,), borderwidth=3, bordercolor="gray40", rowheight=30)
            head_style = ttk.Style(parent)
            head_style.theme_use("clam")
            style.configure("Treeview.Heading", background="gray40", foreground=globals.get_hex_color("companylightgreen"), font=('Arial', 16, 'bold'), borderwidth=0)
            
            self.connected_treeview = ttk.Treeview(self.connected_frame)
            columns = self.connected_treeview["columns"] = ("port", 1, 2, 3)
            self.connected_treeview.heading("port", text="Port")
            self.connected_treeview.column("port", anchor=tk.CENTER)
            self.connected_treeview.heading(1, text="Model")
            self.connected_treeview.column(1, anchor=tk.CENTER)
            self.connected_treeview.heading(2, text="Size")
            self.connected_treeview.column(2, anchor=tk.CENTER)
            self.connected_treeview.heading(3, text="Status")
            self.connected_treeview.column(3, anchor=tk.CENTER)
            self.connected_treeview['show'] = 'headings'
            self.connected_treeview.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)



        def main_frame():
            self.main_frame = customtkinter.CTkFrame(self, fg_color=globals.get_hex_color("dark_gray"))
            self.main_frame.pack(side="top", fill="both", expand=True)
            self.main_frame.grid_columnconfigure(1, weight=1)
            
            self.left_frame = customtkinter.CTkFrame(self.main_frame, fg_color=globals.get_hex_color("dark_gray"))
            self.left_frame.grid(row=0, column=0, sticky="nsew")
            
            self.right_frame = customtkinter.CTkFrame(self.main_frame, fg_color=globals.get_hex_color("dark_gray"))
            self.right_frame.grid(row=0, column=1, sticky="nsew")

            connected_frame(self.left_frame)
            print(get_all_connected())
            
            
        def load_connected():
            print("load_connected")
        
        def load_wiping():
            print("load_disconnected")
            
        def load_complete():
            print("load_wiped")
        


        
        self.title(DriveDashboard.APP_NAME)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.grid_rowconfigure(1, weight=1)

        top_frame()
        main_frame()

    def on_closing(self):
        import sys
        print(f"There are {len(threading.enumerate())} threads running")
        for thread in threading.enumerate():
            print(f"Thread: {thread.name}")
            if thread.is_alive():
                print(f"Stopping thread: {thread.name}")
                thread._running = False
        self.destroy()
        sys.exit()