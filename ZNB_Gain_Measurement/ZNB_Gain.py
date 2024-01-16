# Example for NRP-Z powersensors, modifield to ZNB
# Preconditions:
# - Installed RsInstrument Python module Version 1.7.0 or newer from pypi.org
# - Installed R&S Visa 5.12.x or newer

# from RsInstrument.RsInstrument import RsInstrument, BinFloatFormat  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details

import tkinter as tk
from tkinter import messagebox
import time
import sys

# Define a dictionary to map input keys to frequency ranges
freq_ranges = {
    'D': {'start': '690M', 'stop': '3.2G', 'power': '3.0G'},
	'E': {'start': '2.5G', 'stop': '6.0G','power': '3.0G'}
}

# Get user input for the band key
band_key = input("Enter the band key (D/E): ").upper()

StartFreq_input = freq_ranges[band_key]['start']
StopFreq_input = freq_ranges[band_key]['stop']
Fre_Nominal_Input_Power = freq_ranges[band_key]['power']

def on_closing():
    root.destroy()

def popup_cal():
    # Ask the user if they want to perform the calibration
    result = messagebox.askquestion("Calibration", "Do you want to perform the calibration?")
    
    # If the user clicks "yes", show a message to perform the calibration and exit the script
    if result == 'yes':
        messagebox.showinfo("Message", "Please perform the calibration.")
        on_closing()  # Call the function to destroy the root window and exit the script
    
    # If the user clicks "no", show a message that the calibration will be performed later
    else:
        messagebox.showinfo("Message", "Calibration will be performed later.")
        # Stop the python file and print a message asking the user to try again
        sys.exit("Please try again later.")

def popup_import():
    messagebox.showinfo("Message", "Import the Previous Gain File, and select memory file")
    on_closing()  # Call the function to destroy the root window and exit the script

from RsInstrument import *

NoOfPoints = 401 
instr = None
try:

	ZNB = RsInstrument('TCPIP::172.20.33.253::INSTR', True, True, "SelectVisa='rs'")  # Standard LAN connection (also called VXI-11))
	ZNB.visa_timeout = 5000  # Timeout for VISA Read Operations
	ZNB.instrument_status_checking = True  # Error check after each command

	print(f'Visa manufacturer: {ZNB.visa_manufacturer}')
	print(f'Instrument Identification string: {ZNB.idn_string}')

except Exception as ex:
	print('Error initializing the instrument session:\n' + ex.args[0])
	exit()

try:

	SG = RsInstrument('TCPIP::172.20.33.226::INSTR', True, True, "SelectVisa='rs'")  # Standard LAN connection (also called VXI-11))
	SG.visa_timeout = 5000  # Timeout for VISA Read Operations
	SG.instrument_status_checking = True  # Error check after each command

	print(f'Visa manufacturer: {SG.visa_manufacturer}')
	print(f'Instrument Identification string: {SG.idn_string}')

except Exception as ex:
	print('Error initializing the instrument session:\n' + ex.args[0])
	exit()

ZNB.write_str_with_opc('*RST') # Reset the instrument, clear the Error queue

ZNB.write_str(f'FREQ:STAR {StartFreq_input}Hz')
ZNB.write_str(f'FREQ:STOP {StopFreq_input}Hz')

# Power  
ZNB.write_str_with_opc(f"SOUR:POW -15")

# BandWidth
ZNB.write_str(f'BAND 10')

# Sweep Point
ZNB.write_str_with_opc(f"SWE:POIN {NoOfPoints}")

# Scale/Div
ZNB.write_str_with_opc(f"DISP:WIND:TRAC1:Y:PDIV 2")

# Create the main window
root = tk.Tk()
root.withdraw()  # we don't want a full GUI, so keep the root window from appearing

# Call the function to create the popup_cal
popup_cal()

# Start the event loop
root.mainloop()

ZNB.write_str_with_opc(f"CALC1:MARK1 ON")
ZNB.write_str_with_opc(f"CALC1:MARK2 ON")
ZNB.write_str_with_opc(f"CALC1:MARK3 ON")
ZNB.write_str_with_opc(f"CALC1:MARK4 ON")
ZNB.write_str_with_opc(f"CALC1:MARK5 ON")

ZNB.write_str_with_opc(f"CALC1:MARK1:X {StartFreq_input}Hz")
ZNB.write_str_with_opc(f"CALC1:MARK2:X {StopFreq_input}Hz")
ZNB.write_str_with_opc(f"CALC1:MARK3:X {Fre_Nominal_Input_Power}Hz")
ZNB.write_str_with_opc(f"CALC1:MARK4:FUNC:EXEC MAX")
ZNB.write_str_with_opc(f"CALC1:MARK5:FUNC:EXEC MIN")

ZNB.write_str_with_opc(f"CALC1:MARK4:SEAR:TRAC ON")
ZNB.write_str_with_opc(f"CALC1:MARK5:SEAR:TRAC ON")

# Create the main window
root = tk.Tk()
root.withdraw()  # we don't want a full GUI, so keep the root window from appearing

# Call the function to create the popup_import
popup_import()

# Start the event loop
root.mainloop()

ZNB.write_str_with_opc(f"CALC1:MARK1 ON")
ZNB.write_str_with_opc(f"CALC1:MARK2 ON")
ZNB.write_str_with_opc(f"CALC1:MARK3 ON")
ZNB.write_str_with_opc(f"CALC1:MARK4 ON")
ZNB.write_str_with_opc(f"CALC1:MARK5 ON")

ZNB.write_str_with_opc(f"CALC1:MARK1:X {StartFreq_input}Hz")
ZNB.write_str_with_opc(f"CALC1:MARK2:X {StopFreq_input}Hz")
ZNB.write_str_with_opc(f"CALC1:MARK3:X {Fre_Nominal_Input_Power}Hz")
ZNB.write_str_with_opc(f"CALC1:MARK4:FUNC:EXEC MAX")
ZNB.write_str_with_opc(f"CALC1:MARK4:FUNC:EXEC MIN")

# # -----------------------------------------------------------x	
SG.write_str_with_opc('*RST')
SG.write_str_with_opc(f':SOUR1:FREQ:CW {Fre_Nominal_Input_Power}Hz')
# SG.write_str('OUTP ON')
# time.sleep(5)
# SG.write_str('OUTP OFF')

# -----------------------------------------------------------
# PM.write_str_with_opc('*RST')