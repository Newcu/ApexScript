# ApexScript

Apex Legends Scripts For Playstation 5 controller.

Key Features of the Codes:
Input Detection:
- Listens for "L2" (Left Trigger).
- Waits for 0.2 seconds of continuous hold before triggering the output.

Output Simulation:
- Simulates the Superglide or Mantlejump.

Flexibility:
- You can switch input and output by modifying the button check.

How to Compile and Run:
- Save the code to a file.
- Compile the code using a C++ compiler with XInput linked:
  - g++ apex_controller.cpp -o apex_controller -lXinput
  
Run the executable:
- ./apex_controller
