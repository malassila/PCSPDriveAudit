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
from linux import get_all_connected, link_connected
from button_clicks import wipe_all_button_click, wipe_selected_button_click, view_smart_button_click


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
            
            self.label_frame = customtkinter.CTkFrame(self.top_frame, fg_color=globals.get_hex_color("dark_gray"))
            self.label_frame.pack(side="top", fill="x", padx=10, pady=10)
            self.label_frame.grid_columnconfigure(0, weight=1)  
            
            self.connected_label_frame = customtkinter.CTkFrame(self.label_frame, fg_color=globals.get_hex_color("dark_gray"))
            self.connected_label_frame.grid(row=0, column=0, padx=10, pady=10)
            
            self.connected_title_label = customtkinter.CTkLabel(self.connected_label_frame, text="Connected", font=("Arial", 20), fg_color=globals.get_hex_color("dark_gray"), width=10)
            self.connected_title_label.grid(row=0, column=0, sticky="new", padx=10, pady=10)
            
            self.connected_value_val = tk.StringVar()
            self.connected_value_val.set("0")
            
            self.connected_value_label = customtkinter.CTkLabel(self.connected_label_frame, text="0", font=("Arial", 36), fg_color=globals.get_hex_color("dark_gray"), textvariable=self.connected_value_val, width=10)
            self.connected_value_label.grid(row=1, column=0, sticky="new", padx=10, pady=10)
            
            # self.serial_label_frame = customtkinter.CTkFrame(self.label_frame, fg_color=globals.get_hex_color("dark_gray"))
            # self.serial_label_frame.grid(row=0, column=1, padx=10, pady=10)
            
            # self.serial_title_label = customtkinter.CTkLabel(self.serial_label_frame, text="serial", font=("Arial", 20), fg_color=globals.get_hex_color("dark_gray"), width=10)
            # self.serial_title_label.grid(row=0, column=0, sticky="new", padx=10, pady=10)
            
            self.serial_value_val = tk.StringVar()
            self.serial_value_val.set("-")
            
            # self.serial_value_label = customtkinter.CTkLabel(self.serial_label_frame, text="0", font=("Arial", 36), fg_color=globals.get_hex_color("dark_gray"), textvariable=self.serial_value_val, width=10)
            # self.serial_value_label.grid(row=1, column=0, sticky="new", padx=10, pady=10)
            
            self.wiping_label_frame = customtkinter.CTkFrame(self.label_frame, fg_color=globals.get_hex_color("dark_gray"))
            self.wiping_label_frame.grid(row=0, column=2, padx=10, pady=10)
            
            self.wiping_title_label = customtkinter.CTkLabel(self.wiping_label_frame, text="Wiping", font=("Arial", 20), 
                                                             fg_color=globals.get_hex_color("dark_gray"), width=10, text_color=globals.get_hex_color("oceanblue"))
            self.wiping_title_label.grid(row=0, column=0, sticky="new", padx=10, pady=10)
            
            self.wiping_value_val = tk.StringVar()
            self.wiping_value_val.set("0")
            
            self.wiping_value_label = customtkinter.CTkLabel(self.wiping_label_frame, text="0", font=("Arial", 36), fg_color=globals.get_hex_color("dark_gray"), textvariable=self.wiping_value_val)
            self.wiping_value_label.grid(row=1, column=0, sticky="new", padx=10, pady=10)
            
            self.completed_label_frame = customtkinter.CTkFrame(self.label_frame, fg_color=globals.get_hex_color("dark_gray"))
            self.completed_label_frame.grid(row=0, column=3, padx=10, pady=10)
            
            self.completed_title_label = customtkinter.CTkLabel(self.completed_label_frame, text="Complete", font=("Arial", 20), 
                                                                fg_color=globals.get_hex_color("dark_gray"), text_color=globals.get_hex_color("companylightgreen"), width=10)
            self.completed_title_label.grid(row=0, column=0, sticky="new", padx=10, pady=10)
            
            self.completed_value_val = tk.StringVar()
            self.completed_value_val.set("0")
            
            self.completed_value_label = customtkinter.CTkLabel(self.completed_label_frame, text="0", font=("Arial", 36), fg_color=globals.get_hex_color("dark_gray"), textvariable=self.completed_value_val)
            self.completed_value_label.grid(row=1, column=0, sticky="new", padx=10, pady=10)
            
            self.failed_label_frame = customtkinter.CTkFrame(self.label_frame, fg_color=globals.get_hex_color("dark_gray"))
            self.failed_label_frame.grid(row=0, column=4, padx=10, pady=10)
            
            self.failed_title_label = customtkinter.CTkLabel(self.failed_label_frame, text="Failed", font=("Arial", 20), 
                                                             fg_color=globals.get_hex_color("dark_gray"), text_color=globals.get_hex_color("red"))
            self.failed_title_label.grid(row=0, column=0, sticky="new", padx=10, pady=10)
            
            self.failed_value_val = tk.StringVar()
            self.failed_value_val.set("0")
            
            self.failed_value_label = customtkinter.CTkLabel(self.failed_label_frame, text="0", font=("Arial", 36), 
                                                             fg_color=globals.get_hex_color("dark_gray"), textvariable=self.failed_value_val)
            self.failed_value_label.grid(row=1, column=0, sticky="new", padx=10, pady=10)
            

            
        def action_frame(parent):
            self.action_frame = customtkinter.CTkFrame(parent, fg_color=globals.get_hex_color("dark_gray"))
            self.action_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            
            self.action_label_frame = customtkinter.CTkFrame(self.action_frame, fg_color=globals.get_hex_color("dark_gray"))
            self.action_label_frame.pack(side="top", fill="x", padx=10, pady=10)
            
            self.action_title_label = customtkinter.CTkLabel(self.action_label_frame, text="Commands", font=("Arial", 20), fg_color=globals.get_hex_color("dark_gray"))
            self.action_title_label.pack(side="top", fill="x", padx=10, pady=10)
            
            self.action_button_frame = customtkinter.CTkFrame(self.action_frame, fg_color=globals.get_hex_color("dark_gray"))
            self.action_button_frame.pack(side="top", fill="x", padx=10, pady=10)
            
            self.wipe_type_val = tk.StringVar()
            self.wipe_type_options = ["Partition", "Full"]
            self.wipe_type_val.set(self.wipe_type_options[0])

            self.wipe_option_menu = customtkinter.CTkOptionMenu(self.action_button_frame, values=self.wipe_type_options, variable=self.wipe_type_val)
            self.wipe_option_menu.pack(side="top", fill="x", padx=10, pady=10)
            
            self.wipe_all_button = customtkinter.CTkButton(self.action_button_frame, text="Wipe All", 
                                                           font=("Arial", 16), fg_color=globals.get_hex_color("dark_gray"), 
                                                           command=wipe_all_button_click)
            self.wipe_all_button.pack(side="top", fill="x", padx=10, pady=10)
            
            
            self.wipe_selected_button = customtkinter.CTkButton(self.action_button_frame, text="Wipe Selected",
                                                                font=("Arial", 16), fg_color=globals.get_hex_color("dark_gray"), 
                                                                command=wipe_selected_button_click)
            self.wipe_selected_button.pack(side="top", fill="x", padx=10, pady=10)
            
            self.filler_label = customtkinter.CTkLabel(self.action_button_frame, text="", font=("Arial", 16), fg_color=globals.get_hex_color("dark_gray"))
            self.filler_label.pack(side="top", fill="both", padx=10, pady=10)
            
            self.view_smart_button = customtkinter.CTkButton(self.action_button_frame, 
                                                            text="View SMART", font=("Arial", 16), fg_color=globals.get_hex_color("dark_gray"))
            self.view_smart_button.pack(side="bottom", fill="x", padx=10, pady=10)
            
            self.view_wipe_button = customtkinter.CTkButton(self.action_button_frame, text="View Wipe", font=("Arial", 16), fg_color=globals.get_hex_color("dark_gray"))
            self.view_wipe_button.pack(side="bottom", fill="x", padx=10, pady=10)
            
            

        def connected_frame(parent):
            self.connected_frame = customtkinter.CTkFrame(parent, fg_color=globals.get_hex_color("dark_gray"), corner_radius=10)
            self.connected_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            
            self.label = customtkinter.CTkLabel(self.connected_frame, text="Connected", font=("Arial", 20), fg_color=globals.get_hex_color("dark_gray"))
            self.label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

            style = ttk.Style(self.connected_frame)
            style.theme_use("clam")
            style.configure("Treeview", background="gray10", foreground="#ffffff", fieldbackground="gray10", font=('Arial', 10,), borderwidth=3, bordercolor="gray40", rowheight=30)
            head_style = ttk.Style(parent)
            head_style.theme_use("clam")
            style.configure("Treeview.Heading", background="gray40", foreground=globals.get_hex_color("companylightgreen"), font=('Arial', 10, 'bold'), borderwidth=0)
            
            self.connected_treeview = ttk.Treeview(self.connected_frame)
            columns = self.connected_treeview["columns"] = ("port", 1, 2, 3, 4, 5, 6)
            self.connected_treeview.heading("port", text="Port", anchor=tk.CENTER)
            self.connected_treeview.column("port", anchor=tk.CENTER, minwidth=35, width=35)
            self.connected_treeview.heading(1, text="Serial", anchor=tk.CENTER)
            self.connected_treeview.column(1, anchor=tk.CENTER, minwidth=0, width=150)
            self.connected_treeview.heading(2, text="Size", anchor=tk.CENTER)
            self.connected_treeview.column(2, anchor=tk.CENTER, minwidth=0, width=100)
            self.connected_treeview.heading(3, text="Hours", anchor=tk.CENTER)
            self.connected_treeview.column(3, anchor=tk.CENTER, minwidth=0, width=75)
            self.connected_treeview.heading(4, text="Reallocated", anchor=tk.CENTER)
            self.connected_treeview.column(4, anchor=tk.CENTER, minwidth=0, width=100)
            self.connected_treeview.heading(5, text="SMART", anchor=tk.CENTER)
            self.connected_treeview.column(5, anchor=tk.CENTER, minwidth=0, width=100)
            self.connected_treeview.heading(6, text="Status", anchor=tk.CENTER)
            self.connected_treeview.column(6, anchor=tk.CENTER, minwidth=0, width=100)
            self.connected_treeview['show'] = 'headings'
            self.connected_treeview.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

            globals.connected_treeview = self.connected_treeview
            
            self.connected_treeview.tag_configure("connected", foreground="white")
            self.connected_treeview.tag_configure("wiping", foreground=globals.get_hex_color("oceanblue"))
            self.connected_treeview.tag_configure("wiped", foreground=globals.get_hex_color("companylightgreen"))
            self.connected_treeview.tag_configure("wipe_failed", foreground="black", background="red")
            
            self.scrollable_file_frame = customtkinter.CTkScrollableFrame(master=self, width=200)
            self.scrollable_file_frame.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)



        def main_frame():
            self.main_frame = customtkinter.CTkFrame(self, fg_color=globals.get_hex_color("dark_gray"))
            self.main_frame.pack(side="top", fill="both", expand=True)
            
            self.main_frame.grid_columnconfigure(1, weight=1)
            self.main_frame.grid_rowconfigure(2, weight=1)
            
            self.right_frame = customtkinter.CTkFrame(self.main_frame, fg_color=globals.get_hex_color("dark_gray"))
            self.right_frame.grid(row=0, column=1, sticky="nsew")
            
            self.left_frame = customtkinter.CTkFrame(self.main_frame, fg_color=globals.get_hex_color("dark_gray"))
            self.left_frame.grid(row=0, column=0, sticky="nsew")
            

            connected_frame(self.left_frame)
            
            action_frame(self.right_frame)
            
            self.scaling_label = customtkinter.CTkLabel(self.main_frame, text="UI Scaling:", anchor="w")
            self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
            self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.main_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                                command=self.change_scaling_event)
            self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
            
       

        
        self.title(DriveDashboard.APP_NAME)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.grid_rowconfigure(1, weight=1)
        top_frame()
        main_frame()
        self.view_smart_button.configure(command=lambda: view_smart_button_click())
        # self.connected_treeview.bind("<<TreeviewSelect>>", lambda event: load_labels(self.serial_value_val, self.wiping_value_val, self.completed_value_val, self.failed_value_val))
        self.set_default_scaling()
        
        thread = threading.Thread(target=link_connected, args=(self.connected_value_val, self, self.connected_treeview))
        thread.start()
        
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    
    def set_default_scaling(self):
        customtkinter.set_widget_scaling(0.8)
        
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