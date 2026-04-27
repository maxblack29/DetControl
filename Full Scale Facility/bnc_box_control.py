import serial
import time

COM_PORT = "COM10"
BAUD = 9600
READ_TIMEOUT_S = 1.0

def switch_preset(preset_number):
    """Send *RCL <n> to the BNC box; expect a line containing ``ok`` (case-insensitive)."""
    n = int(preset_number) #converts preset number to an integer
    ser = serial.Serial(COM_PORT, BAUD, timeout=READ_TIMEOUT_S)
    try:  # send *RCL; raise if response line has no ok
        ser.reset_input_buffer()
        ser.write(b"*RCL %d\r\n" % n)
        ser.flush()
        ser.readline()  # discard echo
        line = ser.readline()
        if b"ok" not in line.lower():
            raise RuntimeError(
                f"BNC box did not accept *RCL {n} (expected response containing 'ok'); got {line!r}"
            )
    finally:
        ser.close()

def arm(state):
    """Send :PULSE0:STATE ON or OFF to the BNC box; expect a line containing ``ok`` (case-insensitive)."""
    state = str(state).upper()
    ser = serial.Serial(COM_PORT, BAUD, timeout=READ_TIMEOUT_S)
    try:
        ser.reset_input_buffer()
        ser.write(f":PULSE0:STATE {state}\r\n".encode())
        ser.flush()
        ser.readline()  # discard echo
        line = ser.readline()
        if b"ok" not in line.lower():
            raise RuntimeError(
                f"BNC box did not accept :PULSE0:STATE {state} (expected response containing 'ok'); got {line!r}"
            )
    finally:
        ser.close()




'Main function used for testing the BNC box. Click run while in this file to test the BNC box.'
def main(): 
    print("Continuous Mode")
    switch_preset(9)
    time.sleep(5)
    print("Arming")
    arm("ON")
    time.sleep(10)
    switch_preset(12)
    print("Single Shot")
    print("Waiting for pulse...")
    time.sleep(5)
    print("Switching to continuous mode")
    switch_preset(9)
    time.sleep(10)
    print("Done")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")