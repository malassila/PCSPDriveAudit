import socket
import mysql.connector
import globals

def get_connection():
    connection = mysql.connector.connect(
        host=globals.mysql_host,
        port=3306,
        database=globals.mysql_database,
        user=globals.mysql_user,
        password=globals.mysql_password
    )
    return connection

def insert_new_drive(serial, model, size, hours, reallocated_sectors, smart_status, status, slot):
    try:
        server = socket.gethostname()
        connection = get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO drive (serial, model, size, hours, reallocated_sectors, smart_status, status, server, slot) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (serial, model, size, hours, reallocated_sectors, smart_status, status, server, slot))
        connection.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()

def insert_new_report(serial, report_type, timestamp, status):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO report (serial, type, timestamp, status) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (serial, report_type, timestamp, status))
        connection.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()

def update_report(serial, report_type, timestamp, status):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = "UPDATE report SET status = %s WHERE serial = %s AND status = 'Active"
        cursor.execute(query, (status, serial, report_type, timestamp))
        connection.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()


def get_drive_data(drive):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = "SELECT model, size, hours, reallocated_sectors, smart_status, status FROM drive WHERE serial = %s"
        cursor.execute(query, (drive,))
        result = cursor.fetchone()
        if result:
            return result
        else:
            return None
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        connection.close()

    
def lookup_drive(serial):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = "SELECT serial FROM drive WHERE serial = %s"
        cursor.execute(query, (serial,))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        connection.close()

def update_drive_status(serial, status):
    update_tree_status(serial, status)
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = "UPDATE drive SET status = %s WHERE serial = %s"
        cursor.execute(query, (status, serial))
        connection.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()

def get_drive_status(serial):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = "SELECT status FROM drive WHERE serial = %s"
        cursor.execute(query, (serial,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        connection.close()

# def load_labels(serial_label, hours_label, reallocated_sectors_label, smart_status_label):
#     treeview = globals.connected_treeview
#     # Get the selected item
#     selected_item = treeview.selection()
#     # Get the device name from the selected item
#     serial = treeview.item(selected_item)['values'][1]
#     connection = get_connection()
#     try:
#         cursor = connection.cursor()
#         query = "SELECT hours, reallocated_sectors, smart_status FROM drive WHERE serial = %s"
#         cursor.execute(query, (serial,))
#         result = cursor.fetchone()
#         if result:
#             hours_label.set(result[0])
#             reallocated_sectors_label.set(result[1])
#             smart_status_label.set(result[2])
#             serial_label.set(serial)
#         else:
#             hours_label.set("")
#             reallocated_sectors_label.set("")
#             smart_status_label.set("")
#             serial_label.set("")
#     except Exception as e:
#         print(e)
#     finally:
#         cursor.close()
#         connection.close()
    
    
    

# Example usage:
def update_tree_status(serial, status):
    treeview = globals.connected_treeview
    for item in treeview.get_children():
        if treeview.item(item)['values'][1] == serial:
            treeview.item(item, values=(treeview.item(item)['values'][0], treeview.item(item)['values'][1], 
                                        treeview.item(item)['values'][2], treeview.item(item)['values'][3], 
                                        treeview.item(item)['values'][4], treeview.item(item)['values'][5], status))
            globals.set_row_status(treeview, item, status)
            break
