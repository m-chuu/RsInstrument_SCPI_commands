'''Run the following command: pip install pyinstaller
Navigate to the directory where your script is located.
eg: C:\Users\CHAIBENG\AppData\Local\Programs\Python\Python310
Run the following command: pyinstaller --onefile your_script_name.py
After the process completes, you will find the .exe file in the dist folder inside your script's directory.
'''

import win32gui
import win32con
import time
import win32api

# Define the title of the windows to close
window_titles = ["SmartCal MessageBox", "SmartCal InputBox","Headline","MyDlgPictureBox"]


while True:
    for title in window_titles:
        # Get the handle of the window
        hwnd = win32gui.FindWindow(None, title )

        # Check if the window is found
        if hwnd != 0:

            # Set the window as the foreground window
            win32gui.SetForegroundWindow(hwnd)

            # Send the enter key to the window
            win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)
            win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)

    # Wait for 30 seconds before checking again
    time.sleep(30)