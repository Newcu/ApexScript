#include <windows.h>
#include <Xinput.h>
#include <iostream>
#include <thread>
#include <chrono>

int main() {
    XINPUT_STATE state;
    ZeroMemory(&state, sizeof(XINPUT_STATE));

    bool isHoldingInput = false;
    auto holdStartTime = std::chrono::steady_clock::now();

    // Adjust this delay to match the timing of your mantle jumps
    const int jumpDelayMs = 150; // Example: 150ms delay

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
                // Check if the input has been held for the configured delay
                auto now = std::chrono::steady_clock::now();
                auto holdDuration = std::chrono::duration_cast<std::chrono::milliseconds>(now - holdStartTime).count();

                if (holdDuration >= jumpDelayMs) { // Use the configured delay
                    std::cout << "Input held for " << jumpDelayMs << "ms. Simulating mantle jump." << std::endl;

                    // Simulate a jump to cancel the mantle
                    state.Gamepad.wButtons |= XINPUT_GAMEPAD_A; // Press Jump (A button)
                    XInputSetState(0, &state);

                    // Small delay to simulate a "press"
                    std::this_thread::sleep_for(std::chrono::milliseconds(20));

                    // Release Jump
                    state.Gamepad.wButtons &= ~XINPUT_GAMEPAD_A;
                    XInputSetState(0, &state);

                    // Reset the hold state to allow repeated jumps
                    isHoldingInput = false;
                }
            }
        } else {
            // Reset the hold state if the input is released
            isHoldingInput = false;
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(10)); // Small delay to avoid high CPU usage
    }

    return 0;
}
