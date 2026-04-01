import serial 
import time 
import threading

# ---------------- SERIAL SETUP ----------------
ser = serial.Serial(
    port='COM3',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=0.1   # shorter timeout helps live updates
ser.reset_input_buffer() 
)

XON = b'\x11'

# ---------------- LIVE SERIAL READER ----------------
def read_serial():
    """Continuously read and print incoming serial data"""
    while True:
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)
            try:
                print(data.decode(errors='ignore'), end='')
            except:
                print(data)

# Start background thread
threading.Thread(target=read_serial, daemon=True).start()

# ---------------- HELPERS ----------------
def wait_for_xon():
    """Wait until controller sends XON (ready)"""
    while True:
        data = ser.read(1)
        if data == XON:
            return

def send(cmd):
    """Send a command safely with handshake"""
    print(f"\nSending: {cmd}")
    ser.write((cmd + '\r').encode())

# ---------------- MAIN PROGRAM ----------------
print("Klinger X-axis test ready.")
print("Press ENTER to move to -29500 and back to 0.")
print("Type 'q' to quit.\n")

while True:
    user_input = input("Command: ")

    if user_input.lower() == 'q':
        break

    send("RX4000")
    wait_for_xon()

    send("NX-29500")
    wait_for_xon()
    print("\nReached -29500")

    time.sleep(1)

    send("NX0")
    wait_for_xon()
    print("\nReturned to origin (0)\n")

# ---------------- CLEANUP ----------------
ser.close()
print("Program exited.")