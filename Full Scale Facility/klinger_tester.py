import serial
import time

# ---------------- SERIAL SETUP ----------------
ser = serial.Serial(
    port='COM3',            # update this to the correct port
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

XON = b'\x11' #character that klinger outputs when ready

# ---------------- HELPERS ----------------
def wait_for_xon():
    """Wait until controller sends XON (ready)"""
    while True:
        data = ser.read(1)
        if data == XON:
            return

def send(cmd):
    """Send a command safely with handshake"""
    print(f"Sending: {cmd}")
    ser.write((cmd + '\r').encode()) #adds a carriage return to the command

# ---------------- MAIN PROGRAM ----------------
print("Klinger X-axis test ready.")
print("Press ENTER to move to -29500 and back to 0.")
print("Type 'q' to quit.\n")

while True:
    user_input = input("Command: ")

    if user_input.lower() == 'q':
        break

    # ---- Set high speed ----
    send("RX4000")

    # ---- Move to -29500 ----
    send("NX-29500")
    wait_for_xon()   # wait until move complete
    print("Reached -29500")

    # ---- Carriage return / turnaround pause ----
    time.sleep(1)

    # ---- Move back to origin ----
    send("NX0")   # faster than OX unless you NEED re-homing
    wait_for_xon()
    print("Returned to origin (0)\n")

# ---------------- CLEANUP ----------------
ser.close()
print("Program exited.")