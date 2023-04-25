import os

def get_all_connected():
    data_dir = "/ConnectedDrives/data"
    connected_drives = []
    for filename in os.listdir(data_dir):
        if not os.path.isfile(os.path.join(data_dir, filename)):
            continue
        if not filename.startswith("s"):
            continue
        try:
            drive, serial = filename.split("_")
        except ValueError:
            continue
        with open(os.path.join(data_dir, filename), "r") as f:
            contents = f.read()
        if "Serial:" not in contents:
            continue
        serial = contents.split("Serial:")[1].strip()
        connected_drives.append((drive, serial))
    return connected_drives

