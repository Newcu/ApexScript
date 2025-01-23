import keyboard
import time
import threading
import hid

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

# Function to check if a button is pressed
def is_button_pressed():
    # Read input data from the controller
    data = device.read(64)  # Read 64 bytes of data
    if data:
        # Example: Check if L2 (Left Trigger) is pressed
        # Note: You'll need to reverse-engineer the HID report format for the DualSense
        l2_trigger = data[5]  # Example: Byte 5 represents the L2 trigger
        return l2_trigger > 0  # Return True if L2 is pressed
    return False

# Function to spam jump and crouch inputs
def superglide_spam():
    while True:
        if is_button_pressed():  # Only spam inputs while the button is held down
            # Simulate jump (Space) and crouch (Ctrl) inputs
            keyboard.press('space')  # Press jump
            keyboard.press('ctrl')   # Press crouch
            time.sleep(0.01)         # Small delay to simulate simultaneous inputs
            keyboard.release('space')  # Release jump
            keyboard.release('ctrl')   # Release crouch
        else:
            time.sleep(0.01)  # Small delay to avoid high CPU usage

# Start the superglide spam thread
superglide_thread = threading.Thread(target=superglide_spam)
superglide_thread.daemon = True
superglide_thread.start()

# Main loop
print("Hold L2 to spam jump and crouch for supergliding.")
while True:
    time.sleep(0.1)  # Small delay to avoid high CPU usage
