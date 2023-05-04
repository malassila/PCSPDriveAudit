from tkinter import messagebox
import globals
from database import update_drive_status, get_drive_status
from linux import get_drive_handle, led_fault, led_locate

import random
import time
import subprocess
import traceback
import os
import platform
import subprocess
from datetime import datetime
import time
from pathlib import Path

def wipe_device(serial, wipe_method="dd", status=None):
    if status != "Complete" and status != "Wiping":
        update_drive_status(serial, "Wiping")
        # Overwrite the device with zeros using dd command
        handle = get_drive_handle(serial)
        try:
            print(f"Wiping {serial} with {wipe_method}")
            if wipe_method == "Partition":
                dd_command = f"dd if=/dev/zero of=/dev/{handle} bs=512 count=1000000"
                subprocess.run(dd_command, shell=True)
            # elif wipe_method == "secure":
            #     secure_command = f"hdparm --user-master u --security-set-pass Eins /dev/{handle}"
            #     subprocess.run(secure_command, shell=True)
            update_drive_status(serial, "Complete")
            
            print(f"{serial} wiped successfully")
            led_locate(handle)
            time.sleep(10)
            led_locate(handle)
        except Exception as e:
            print(traceback.format_exc())
            update_drive_status(serial, "Failed")
            print(f"{serial} wipe failed")
            led_fault(handle)
            time.sleep(10)
            led_fault(handle)
    else:
        # messagebox.showinfo("Wipe Device", f"{serial} is already wiped.")
        led_locate(handle)

def print_wipe_banner(serial, drive, model, capacity, hours, reallocated, port):
    system_info = {
        "Distro": platform.linux_distribution()[0],
        "Shell": os.environ.get("SHELL"),
        "Kernel": platform.release()
    }

    wipe_server = {
        "Architecture": platform.machine(),
        "Hardware Vendor": subprocess.getoutput('hostnamectl status | grep "Hardware Vendor" | cut -d":" -f2').strip(),
        "Processor": subprocess.getoutput('lscpu | grep "^Model name" | cut -d":" -f2- | sed -e "s/^[ \\t]*//"').strip(),
        "Raid Controller": subprocess.getoutput('lspci | grep -i raid | cut -d":" -f3- | sed -e "s/^[ \\t]*//"').strip()
    }

    wipe_tool_info = {
        "Wipe Tool": subprocess.getoutput('hdparm -V').strip(),
        "Build Date": subprocess.getoutput('man hdparm | tail -n 1 | awk \'{print $3" "$4}\'').strip(),
        "Method of Wipe": "Secure Erase (normal)"
    }

    banner = f"""******************************************************************************************
    PC Server & Parts Wipe Tool
******************************************************************************************
    Date: {datetime.now().strftime('%a %b %d %T %Z %Y')}    Port: {port}   Server: {platform.node()}
******************************************************************************************
    Used Technologies:
        Distro: {system_info["Distro"]}
        Shell: {system_info["Shell"]}
        Kernel: {system_info["Kernel"]}

    Wipe Server:
        Architecture: {wipe_server["Architecture"]}
        Hardware Vendor: {wipe_server["Hardware Vendor"]}
        Processor: {wipe_server["Processor"]}
        Raid Controller: {wipe_server["Raid Controller"]}

    Wipe Tool: {wipe_tool_info["Wipe Tool"]}
        Build Date: {wipe_tool_info["Build Date"]}
        Method of Wipe: {wipe_tool_info["Method of Wipe"]}

    Basic Drive Information:
        Drive Model: {model}
        Serial Number: {serial}
        Capacity: {capacity}
        Power On Hours: {hours}
        Reallocated Sectors: {reallocated}
******************************************************************************************
"""
    Path("/DRIVE/Test/Wipe/").mkdir(parents=True, exist_ok=True)
    with open(f"/DRIVE/Test/Wipe/{serial}_wipe.txt", "w") as wipe_file:
        wipe_file.write(banner)


def print_wipe_footer(serial, start_time, path, wipe_result):
    elapsed_time = int(time.time() - start_time)
    formatted_time = datetime.utcfromtimestamp(elapsed_time).strftime('%H:%M:%S')

    with open(path, "a") as wipe_file:
        if wipe_result == 'success':
            wipe_file.write(f"\n\n\t{serial} wiped successfully in {formatted_time}\n")
            print(f"{serial} wiped successfully in {formatted_time} and saved to {path}")
        else:
            wipe_file.write(f"\n\n\t{serial} wipe failed in {formatted_time} with result: {wipe_result}\n")
            print(f"{serial} wipe failed in {formatted_time} with result: {wipe_result} and saved to {path}")

        wipe_file.write("******************************************************************************************\n")
        wipe_file.write("\tAuthor: Matt L\t\tBuild Date: April 2023\n")
        wipe_file.write("******************************************************************************************\n\n")

    subprocess.Popen(["rsync", "-avz", path, "/mnt/nfs/Wiped/"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
