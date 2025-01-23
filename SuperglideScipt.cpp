#include <windows.h>
#include <Xinput.h>
#include <iostream>
#include <thread>
#include <chrono>

int main() {
    XINPUT_STATE state;
    ZeroMemory(&state, sizeof(XINPUT_STATE));

    bool isHoldingInput = false;
    bool isTriggeringOutputs = false;
    auto holdStartTime = std::chrono::steady_clock::now();

    while (true) {
        XInputGetState(0, &state); // Get the current controller state

        // Check if L2 is pressed (Left Trigger) or Triangle (Y Button)
        bool isInputPressed = (state.Gamepad.bLeftTrigger > XINPUT_GAMEPAD_TRIGGER_THRESHOLD); // For L2
        // bool isInputPressed = (state.Gamepad.wButtons & XINPUT_GAMEPAD_Y); // For Triangle

        if (isInputPressed) {
            if (!isHoldingInput) {
                // Start the hold timer
                isHoldingInput = true;
                holdStartTime = std::chrono::steady_clock::now();
            } else {
                // Check if the input has been held for 0.2 seconds
                auto now = std::chrono::steady_clock::now();
                auto holdDuration = std::chrono::duration_cast<std::chrono::milliseconds>(now - holdStartTime).count();

                if (holdDuration >= 200) { // 200ms = 0.2 seconds
                    if (!isTriggeringOutputs) {
                        std::cout << "Input held for 0.2 seconds. Rapidly triggering outputs." << std::endl;
                        isTriggeringOutputs = true;
                    }

                    // Rapidly trigger Left Joystick Click (Crouch) and L2 (Jump)
                    state.Gamepad.wButtons |= XINPUT_GAMEPAD_LEFT_THUMB; // Press Left Joystick Click
                    state.Gamepad.bLeftTrigger = 255; // Press L2 (Max trigger value)
                    XInputSetState(0, &state);

                    // Small delay to simulate a "press"
                    std::this_thread::sleep_for(std::chrono::milliseconds(20)); // Adjust for speed

                    // Release Left Joystick Click and L2
                    state.Gamepad.wButtons &= ~XINPUT_GAMEPAD_LEFT_THUMB; // Release Left Joystick Click
                    state.Gamepad.bLeftTrigger = 0; // Release L2
                    XInputSetState(0, &state);

                    // Small delay before next trigger
                    std::this_thread::sleep_for(std::chrono::milliseconds(20)); // Adjust for speed
                }
            }
        } else {
            // Reset the hold state if the input is released
            isHoldingInput = false;
            isTriggeringOutputs = false;
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(10)); // Small delay to avoid high CPU usage
    }

    return 0;
}
