import glob
import os
import subprocess
import re
import database as db
import globals

def get_all_connected():
    data_dir = "/ConnectedDrives/data"
    connected_list = []
    # Get list of all the files that start with "sd"
    drive_files = [filename for filename in os.listdir(data_dir) if filename.startswith("sd")]
    for filename in drive_files:
        # process each drive file
        connected_list.append(filename)
    return connected_list



def get_drive_slot(drive_handle):
    try:
        with open(f"/ConnectedDrives/{drive_handle}", "r") as f:
            first_line = f.readline().strip()
            port_num = first_line[-3:-1]
            slot = globals.get_port_name(port_num)
            return slot
    except FileNotFoundError:
        return None

def get_drive_serial(drive_handle):
    data_dir = "/ConnectedDrives/data"
    filename = f"{drive_handle}_*"
    file_path = os.path.join(data_dir, filename)
    matches = glob.glob(file_path)
    if matches:
        match = matches[0]
        serial = match.split("_")[1]
        return serial
    else:
        return None

def get_drive_data(drive_handle):
    data_dir = "/ConnectedDrives/data"
    filename = f"{drive_handle}_*"
    file_path = os.path.join(data_dir, filename)
    matches = glob.glob(file_path)
    if matches:
        match = matches[0]
        with open(match, "r") as f:
            contents = f.read()
        model = contents.split("Model: ")[1].split("\n")[0]
        size = contents.split("Size: ")[1].split("\n")[0]
        hours = contents.split("Hours: ")[1].split("\n")[0]
        reallocated_sectors = contents.split("ReallocatedSectors: ")[1].split("\n")[0]
        smart_status = contents.split("SMART: ")[1].split("\n")[0]
    
        return (model, size, hours, reallocated_sectors, smart_status)
    else:
        return None



def get_number_of_connected():
    return len([f for f in os.listdir("/ConnectedDrives/data") if f.startswith("sd")])

def get_number_of_wiping():
    print("Getting number of wiping")
    
def get_number_of_failed():
    print("Getting number of failed")
    
def get_number_of_complete():
    print("Getting number of complete")
    


def link_connected(connected_value_val, root, connected_treeview):
    def update_connected_value():
        connected = get_number_of_connected()
        if connected != globals.num_connected:
            connected_value_val.set(connected)
            if connected > globals.num_connected:
                globals.num_connected = connected
                drive_added(root, connected_treeview)
            else:
                globals.num_connected = connected
                drive_removed(root, connected_treeview)
        root.after(1000, update_connected_value)

    update_connected_value()
    
def drive_added(root, connected_treeview):
    drives = get_all_connected()
    for drive in drives:
        handle = drive.split("_")[0]
        serial = drive.split("_")[1]
        if drive in globals.connected_drives:
            continue
        else:
            globals.connected_drives.append(drive)
            slot = get_drive_slot(handle)
            in_database = db.lookup_drive(serial)
            if in_database:
                model, size, hours, reallocated_sectors, smart_status, status = db.get_drive_data(serial)
            else:
                model, size, hours, reallocated_sectors, smart_status = get_drive_data(handle)
                status = "Connected"
                db.insert_new_drive(serial, model, size, hours, reallocated_sectors, smart_status, status, slot)
            

            tag = "connected"
            if status == "Wiping":
                tag = "wiping"
            elif status == "Wiped":
                tag = "wiped"
            elif status == "Wipe Failed":
                tag = "wipe_failed"
                
            connected_treeview.insert("", "end", values=(slot, serial, size, hours, reallocated_sectors, smart_status, status), tags=(tag,))
            
            # Configure the tag with the appropriate colors
            connected_treeview.tag_configure("connected", foreground="white")
            connected_treeview.tag_configure("wiping", foreground=globals.get_hex_color("oceanblue"))
            connected_treeview.tag_configure("wiped", foreground=globals.get_hex_color("companylightgreen"))
            connected_treeview.tag_configure("wipe_failed", foreground="black", background="red")

            

            
    
def drive_removed(root, connected_treeview):
    drives = get_all_connected()
    for drive in globals.connected_drives:
        handle = drive.split("_")[0]
        serial = drive.split("_")[1]
        if drive not in drives:
            globals.connected_drives.remove(drive)
            # delete only the row with the serial number
            for row in connected_treeview.get_children():
                if connected_treeview.item(row)["values"][1] == serial:
                    connected_treeview.delete(row)


def get_drive_handle(serial):
    data_dir = "/ConnectedDrives/data"
    filename = f"*_{serial}"
    file_path = os.path.join(data_dir, filename)
    matches = glob.glob(file_path)
    if matches:
        match = matches[0]
        file_name = os.path.basename(match)
        handle = file_name.split("_")[0]
        return handle
    else:
        return None

def led_locate(handle):
    # get the led file from /ConnectedDrives/{handle} on the first line (note it has spaces: i.e "/sys/class/enclosure/6:0:1:0/Slot 16/")
    enclosure_path = f"/ConnectedDrives/{handle}"
    with open(enclosure_path, "r") as f:
        led_file = f.readline().strip()
        led_file += "/locate"
    with open(led_file, "w") as f:
        f.write("1")

def led_fault(handle):
    # get the led file from /ConnectedDrives/{handle} on the second line (note it has spaces: i.e "/sys/class/enclosure/6:0:1:0/Slot 16/")
    enclosure_path = f"/ConnectedDrives/{handle}"
    with open(enclosure_path, "r") as f:
        f.readline()
        led_file = f.readline().strip()
        led_file += "/fault"
    with open(led_file, "w") as f:
        f.write("1")  

    



