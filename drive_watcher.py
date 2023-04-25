import os
import subprocess
import time
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import traceback
import mysql.connector
import socket
import re
import globals
# Define a class to handle file events
class DriveFileHandler(FileSystemEventHandler):    
    
    def on_deleted(self, event):
        fileName = os.path.basename(event.src_path)
        serial = fileName.split("_")[1]
        print(f"File Deleted: {serial}")
        # import globals
        connection = mysql.connector.connect(
            host=globals.mysql_host,
            port=3306,
            database=globals.mysql_database,
            user=globals.mysql_user,
            password=globals.mysql_password
        )
        cursor = connection.cursor()
        try:
            query = """UPDATE status SET connected_status = 'Removed' WHERE serial = %s"""
            cursor.execute(query, (serial,))
            connection.commit()
        except Exception as e:
            print(f"Error inserting data into MySQL table: \n{traceback.format_exc()}")
        finally:
            cursor.close()
            connection.close()
                
    def on_created(self, event):
        
        def get_eta(drive_name):
            command = ["openSeaChest_Erase", "-d", f"/dev/{drive_name}", "--showEraseSupport"]
            p1 = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p2 = subprocess.Popen(["grep", "hour\|minute\|second"], stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p3 = subprocess.Popen(["sed", "-e", "s/^[ \t]*//"], stdin=p2.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
            output, error = p3.communicate()
            eta = output.strip()
            return eta
        
        def get_enclosure(drive_name):
            port_dictionary = {
                "Slot 01": "A6",
                "Slot 02": "A5",
                "Slot 03": "A4",
                "Slot 04": "A3",
                "Slot 05": "A2",
                "Slot 06": "A1",
                "Slot 07": "B6",
                "Slot 08": "B5",
                "Slot 09": "B4",
                "Slot 10": "B3",
                "Slot 11": "B2",
                "Slot 12": "B1",
                "Slot 13": "C6",
                "Slot 14": "C5",
                "Slot 15": "C4",
                "Slot 16": "C3",
                "Slot 17": "C2",
                "Slot 18": "C1",
                "Slot 19": "D6",
                "Slot 20": "D5",
                "Slot 21": "D4",
                "Slot 22": "D3",
                "Slot 23": "D2",
                "Slot 24": "D1"
            }
            with open(f"/ConnectedDrives/{drive_name}") as file:
                enclosure_slot = file.read()

            for slot, port in port_dictionary.items():
                if slot in enclosure_slot:
                    enclosure_slot = port
                    return enclosure_slot
            else:
                print("The enclosure slot could not be determined")
                
        def get_drive_data(file_name):
            # Get the hostname
            hostname = socket.gethostname()
            
            # Open the file and read its contents
            with open(f"/ConnectedDrives/data/{file_name}") as file:
                contents = file.read()
            
            drive_name = file_name.split("_")[0]

            # Extract the data using regular expressions
            
            serial = re.search(r"Serial: (.+)", contents).group(1)
            model = re.search(r"Model: (.+)", contents).group(1)
            size = re.search(r"Size: (.+)", contents).group(1)
            hours = re.search(r"Hours: (.+)", contents).group(1)
            reallocated_sectors = re.search(r"ReallocatedSectors: (.+)", contents).group(1)
            smart = re.search(r"SMART: (.+)", contents).group(1)
            port = get_enclosure(drive_name)
            eta = get_eta(drive_name)
            # Return a dictionary containing the extracted data
            return {"serial": serial, "hostname": hostname, "size": size, "hours": hours, "reallocated_sectors": reallocated_sectors, "smart": smart, "model": model, "port": port, "eta": eta}

        def insert_drive_data(file_path):
            drive_data = get_drive_data(file_path)
            connection = mysql.connector.connect(
                host=globals.mysql_host,
                port=3306,
                database=globals.mysql_database,
                user=globals.mysql_user,
                password=globals.mysql_password
            )
            cursor = connection.cursor()
            try:
                query = """INSERT IGNORE INTO drive (serial, model, size, hours, re_sec, smart) VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (drive_data["serial"], drive_data["model"], drive_data["size"], drive_data["hours"], drive_data["reallocated_sectors"], drive_data["smart"]),)
                connection.commit()
                query = """INSERT IGNORE INTO status (serial, server, eta, port) VALUES (%s, %s, %s, %s)"""
                cursor.execute(query, (drive_data["serial"], drive_data["hostname"], drive_data["eta"], drive_data["port"]),)
                connection.commit()
                query = """UPDATE status SET connected_status = 'Connected' WHERE serial = %s"""
                cursor.execute(query, (drive_data["serial"],))
                connection.commit()
            except Exception as e:
                print(f"Error inserting data into MySQL table: \n{traceback.format_exc()}")
            finally:
                cursor.close()
                connection.close()
            # print(drive_data)
            
            
        fileName = os.path.basename(event.src_path)
        # split on the "_" character
        drive_name = fileName.split("_")[0]

        try:
            time.sleep(2)

            # Insert the data into the MySQL database
            # table_name = os.path.splitext(fileName)[0]
            print(f"File Name: {fileName}")
            insert_drive_data(fileName)
            # if table_name in active_threads and active_threads[table_name].is_alive():
            #     print(f"Table Name: {table_name}, Thread: {active_threads}")



        except Exception as e:
            print(f"Error processing {fileName}: \n{traceback.format_exc()}")


def main():
    print("Starting drive watcher...")
    # Set up the watchdog observer and event handler
    observer = Observer()
    event_handler = DriveFileHandler()
    observer.schedule(event_handler, path='/ConnectedDrives/data', recursive=False)
    active_threads = {}
    # Enter a loop to monitor the directory for new files
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == '__main__':
    # Create a new thread to run the main() function
    thread = threading.Thread(target=main)
    # Start the thread
    thread.start()
    import home
    home.Dashboard().mainloop()