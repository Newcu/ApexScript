#include <windows.h>
#include <Xinput.h>
#include <iostream>
#include <thread>
#include <chrono>

int main() {
    XINPUT_STATE state;
    ZeroMemory(&state, sizeof(XINPUT_STATE));

    bool isHoldingL2 = false;
    auto holdStartTime = std::chrono::steady_clock::now();

    while (true) {
        XInputGetState(0, &state); // Get the current controller state

        // Check if L2 is pressed (Left Trigger)
        if (state.Gamepad.bLeftTrigger > XINPUT_GAMEPAD_TRIGGER_THRESHOLD) {
            if (!isHoldingL2) {
                // Start the hold timer
                isHoldingL2 = true;
                holdStartTime = std::chrono::steady_clock::now();
            } else {
                // Check if L2 has been held for 0.2 seconds
                auto now = std::chrono::steady_clock::now();
                auto holdDuration = std::chrono::duration_cast<std::chrono::milliseconds>(now - holdStartTime).count();

                if (holdDuration >= 200) { // 200ms = 0.2 seconds
                    std::cout << "L2 held for 0.2 seconds. Triggering Left Joystick Click and L2." << std::endl;

                    // Simulate Left Joystick Click (Crouch)
                    state.Gamepad.wButtons |= XINPUT_GAMEPAD_LEFT_THUMB;
                    XInputSetState(0, &state);

                    // Small delay to simulate a "press"
                    std::this_thread::sleep_for(std::chrono::milliseconds(50));

                    // Release Left Joystick Click
                    state.Gamepad.wButtons &= ~XINPUT_GAMEPAD_LEFT_THUMB;
                    XInputSetState(0, &state);

                    // Simulate L2 (Jump)
                    // Note: L2 is a trigger, not a button, so we set the trigger value directly
                    XINPUT_VIBRATION vibration;
                    ZeroMemory(&vibration, sizeof(XINPUT_VIBRATION));
                    vibration.wLeftMotorSpeed = 65535; // Vibrate left motor
                    vibration.wRightMotorSpeed = 65535; // Vibrate right motor
                    XInputSetState(0, &vibration);

                    state.Gamepad.bLeftTrigger = 255; // Max trigger value
                    XInputSetState(0, &state);

                    std::this_thread::sleep_for(std::chrono::milliseconds(50));

                    // Release L2
                    state.Gamepad.bLeftTrigger = 0;
                    XInputSetState(0, &state);
                }
            }
        } else {
            // Reset the hold state if L2 is released
            isHoldingL2 = false;
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(10)); // Small delay to avoid high CPU usage
    }

    return 0;
}
