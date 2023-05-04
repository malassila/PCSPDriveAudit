
from tkinter import Frame, Tk, Toplevel, messagebox
import tkinter as tk
import customtkinter
from wipe import wipe_device
from linux import get_drive_handle
import globals
import database as db
import threading

def wipe_all_button_click(wipe_method="Partition"):
    treeview = globals.connected_treeview
    if messagebox.askyesno("Wipe Device", f"Are you sure you want to wipe all devices?"):
        for item in treeview.get_children():
            serial = treeview.item(item)['values'][1]
            status = treeview.item(item)['values'][6]
            wipe_thread = threading.Thread(target=wipe_device, args=(serial, wipe_method, status))
            wipe_thread.daemon = True
            wipe_thread.name = f"Wipe {serial}"
            wipe_thread.start()

    
def wipe_selected_button_click(wipe_method="Partition"):
    treeview = globals.connected_treeview
    # If nothing is selected, prompt the user to select something
    if len(treeview.selection()) == 0:
        messagebox.showinfo("No Selection", "Please select a device to wipe.")
    else:
        # Get the selected item
        selected_item = treeview.selection()
        # Get the device name from the selected item
        serial = treeview.item(selected_item)['values'][1]
        status = treeview.item(selected_item)['values'][6]
        # Prompt the user to confirm the wipe
        if messagebox.askyesno("Wipe Device", f"Are you sure you want to wipe {serial}?"):
            # Wipe the device
            wipe_thread = threading.Thread(target=wipe_device, args=(serial, wipe_method, status))
            wipe_thread.daemon = True
            wipe_thread.name = f"Wipe {serial}"
            wipe_thread.start()

# def view_smart_button_click(scrollable_file_frame):
#     treeview = globals.connected_treeview
#     # If nothing is selected, prompt the user to select something
#     if len(treeview.selection()) == 0:
#         messagebox.showinfo("No Selection", "Please select a device to view SMART data.")
#     else:
#         # Get the selected item
#         selected_item = treeview.selection()
#         # Get the device name from the selected item
#         serial = treeview.item(selected_item)['values'][1]
#         print(f"Getting SMART data for {serial}")
#         # Get the SMART data from the file "/ConnectedDrives/smart/smart_{serial}.txt"
#         smart_file = f"/ConnectedDrives/smart/smart_{serial}.txt"
#         try:
#             with open(smart_file, "r") as f:
#                 smart_data = f.read()
#         except:
#             messagebox.showerror("Error", f"Failed to open {smart_file}")
#             return
#         # Clear the existing content in the scrollable file frame
#         for widget in scrollable_file_frame.winfo_children():
#             widget.destroy()
#         # Add the SMART data to the scrollable file frame
#         smart_textbox = customtkinter.CTkTextBox(scrollable_file_frame)
#         smart_textbox.insert("end", smart_data)
#         smart_textbox.pack(fill="both", expand=True)

def view_smart_button_click():
    treeview = globals.connected_treeview
    # If nothing is selected, prompt the user to select something
    if len(treeview.selection()) == 0:
        messagebox.showinfo("No Selection", "Please select a device to view SMART data.")
    else:
        # Get the selected item
        selected_item = treeview.selection()
        # Get the device name from the selected item
        serial = treeview.item(selected_item)['values'][1]
        print(f"Getting SMART data for {serial}")
        # Get the SMART data from the file "/ConnectedDrives/smart/smart_{serial}.txt"
        try:
            with open(f"/ConnectedDrives/smart/smart_{serial}.txt", "r") as f:
                smart_data = f.read()
                # Create a pop-up window with the SMART data
                popup = tk.Toplevel()
                popup.title(f"SMART Data for {serial}")
                # Create a frame to hold the text and scrollbar
                frame = tk.Frame(popup)
                frame.pack(fill='both', expand=True)
                # Create a text widget to display the SMART data
                text = tk.Text(frame, wrap='word')
                text.insert('end', smart_data)
                text.pack(side='left', fill='both', expand=True)
                # Create a scrollbar and attach it to the text widget
                scrollbar = tk.Scrollbar(frame, command=text.yview)
                scrollbar.pack(side='right', fill='y')
                text.config(yscrollcommand=scrollbar.set)
        except FileNotFoundError:
            messagebox.showinfo("File Not Found", f"No SMART data found for {serial}.")


        
        
        