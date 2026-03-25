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
