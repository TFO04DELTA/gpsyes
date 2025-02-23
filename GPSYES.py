import tkinter as tk
from tkinter import StringVar
import serial
import time

# Initialize the serial connection to the GPYes device
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Update this to your correct port

# Function to read the data from GPYes
def get_gps_data():
    while True:
        line = ser.readline().decode('ascii', errors='ignore')
        if line.startswith('$GPGGA'):  # NMEA GGA sentence
            data = line.split(',')
            if len(data) > 9:
                latitude = data[2]
                longitude = data[4]
                satellites = data[7]
                time_utc = data[1]
                return latitude, longitude, satellites, time_utc

# Update the GUI with the latest GPS info
def update_gui():
    latitude, longitude, satellites, time_utc = get_gps_data()
    lat_label.set(f"Latitude: {latitude}")
    lon_label.set(f"Longitude: {longitude}")
    sat_label.set(f"Satellites: {satellites}")
    time_label.set(f"Time (UTC): {time_utc}")

    # Update every second
    root.after(1000, update_gui)

# Create the main window
root = tk.Tk()
root.title("GPYes GPS Data")

# Create variables to hold the data
lat_label = StringVar()
lon_label = StringVar()
sat_label = StringVar()
time_label = StringVar()

# Create and place labels on the window
tk.Label(root, textvariable=lat_label).pack()
tk.Label(root, textvariable=lon_label).pack()
tk.Label(root, textvariable=sat_label).pack()
tk.Label(root, textvariable=time_label).pack()

# Start updating the GUI
update_gui()

# Run the GUI loop
root.mainloop()
