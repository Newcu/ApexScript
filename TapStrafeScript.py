import vgamepad as vg
import time
import threading
import hid

# Initialize virtual gamepad
gamepad = vg.VX360Gamepad()

# Tap strafe settings
TAP_STRAFE_DELAY = 0.01  # Time between directional inputs (in seconds)

# PS5 DualSense Vendor ID and Product ID
VENDOR_ID = 0x054C  # Sony
PRODUCT_ID = 0x0CE6  # DualSense

# Open the PS5 controller
try:
    device = hid.device()
    device.open(VENDOR_ID, PRODUCT_ID)
    print("PS5 Controller connected!")
except Exception as e:
    print(f"Failed to connect to PS5 controller: {e}")
    exit()

# Function to read the left joystick position
def get_left_stick_position():
    # Read input data from the controller
    data = device.read(64)  # Read 64 bytes of data
    if data:
        # Extract left joystick X and Y values from the HID report
        # Note: You'll need to reverse-engineer the HID report format for the DualSense
        left_stick_x = data[1] / 127.0 - 1  # Normalize to -1 to 1
        left_stick_y = data[2] / 127.0 - 1  # Normalize to -1 to 1
        return left_stick_x, left_stick_y
    return 0.0, 0.0  # Default to neutral position if no data is read

# Function to check if L2 is pressed
def is_l2_pressed():
    # Read input data from the controller
    data = device.read(64)  # Read 64 bytes of data
    if data:
        # Example: Check if L2 (Left Trigger) is pressed
        # Note: You'll need to reverse-engineer the HID report format for the DualSense
        l2_trigger = data[5]  # Example: Byte 5 represents the L2 trigger
        return l2_trigger > 0  # Return True if L2 is pressed
    return False

# Function to simulate tap strafe
def tap_strafe():
    while True:
        if is_l2_pressed():  # Only tap strafe while L2 is held down
            # Read the current left joystick position
            left_stick_x, left_stick_y = get_left_stick_position()

            # Simulate rapid directional inputs
            gamepad.left_joystick_float(x_value_float=left_stick_x, y_value_float=left_stick_y)  # Move in the held direction
            gamepad.update()
            time.sleep(TAP_STRAFE_DELAY)

            # Reset joystick to neutral
            gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
            gamepad.update()
            time.sleep(TAP_STRAFE_DELAY)
        else:
            time.sleep(0.1)

# Start the tap strafe thread
tap_strafe_thread = threading.Thread(target=tap_strafe)
tap_strafe_thread.daemon = True
tap_strafe_thread.start()

# Main loop
print("Hold L2 to tap strafe.")
while True:
    # Simulate normal movement
    left_stick_x, left_stick_y = get_left_stick_position()
    gamepad.left_joystick_float(x_value_float=left_stick_x, y_value_float=left_stick_y)
    gamepad.update()

    time.sleep(0.01)  # Small delay to avoid high CPU usage
