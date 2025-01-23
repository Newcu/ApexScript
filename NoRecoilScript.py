import hid
import random
import time
import threading

# PS5 DualSense Vendor ID and Product ID
VENDOR_ID = 0x054C  # Sony
PRODUCT_ID = 0x0CE6  # DualSense

# Jitter settings
JITTER_INTENSITY = 0.05  # How far the joystick moves (0 to 1)
JITTER_DELAY = 0.01      # Time between jitter movements (in seconds)

# Toggle script on/off
script_active = False

# Open the PS5 controller
try:
    device = hid.device()
    device.open(VENDOR_ID, PRODUCT_ID)
    print("PS5 Controller connected!")
except Exception as e:
    print(f"Failed to connect to PS5 controller: {e}")
    exit()

# Function to jitter the joystick
def jitter_aim():
    global script_active
    while True:
        if script_active:
            # Generate random jitter movements
            jitter_x = random.uniform(-JITTER_INTENSITY, JITTER_INTENSITY)
            jitter_y = random.uniform(-JITTER_INTENSITY, JITTER_INTENSITY)

            # Read the current joystick position
            report = device.read(64)
            if report:
                # Extract the current joystick position from the HID report
                # Note: You'll need to reverse-engineer the HID report format for the DualSense
                current_x = report[1] / 127.0 - 1  # Normalize to -1 to 1
                current_y = report[2] / 127.0 - 1  # Normalize to -1 to 1

                # Add jitter to the current position
                new_x = current_x + jitter_x
                new_y = current_y + jitter_y

                # Clamp the values to the valid range (-1 to 1)
                new_x = max(-1, min(1, new_x))
                new_y = max(-1, min(1, new_y))

                # Create a new HID report with the updated joystick position
                new_report = [0] * 64
                new
