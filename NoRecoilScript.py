import vgamepad as vg
import time
import threading

# Initialize virtual gamepad
gamepad = vg.VX360Gamepad()

# Tap strafe settings
TAP_STRAFE_DELAY = 0.01  # Time between directional inputs (in seconds)

# Toggle script on/off
script_active = False

# Function to simulate tap strafe
def tap_strafe():
    global script_active
    while True:
        if script_active:
            # Read the current left joystick position
            left_stick_x, left_stick_y = get_left_stick_position()  # You'll need to implement this

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

# Function to toggle script on/off
def toggle_script():
    global script_active
    script_active = not script_active
    print(f"Script {'active' if script_active else 'inactive'}")

# Start the tap strafe thread
tap_strafe_thread = threading.Thread(target=tap_strafe)
tap_strafe_thread.daemon = True
tap_strafe_thread.start()

# Main loop
print("Press 'T' to toggle the script on/off.")
while True:
    # Check for button press (e.g., L2 or R2)
    # Replace this with your preferred button detection method
    if some_button_pressed():  # You'll need to implement this
        toggle_script()

    # Simulate normal movement
    # Replace this with your preferred method of reading the left joystick
    left_stick_x, left_stick_y = get_left_stick_position()  # You'll need to implement this
    gamepad.left_joystick_float(x_value_float=left_stick_x, y_value_float=left_stick_y)
    gamepad.update()

    time.sleep(0.01)  # Small delay to avoid high CPU usage
