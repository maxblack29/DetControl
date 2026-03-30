import serial
import time
import threading

# ---------------- SERIAL SETUP ----------------
SERIAL_PORT = 'COM3'  # update this to the correct port
ser = None

def _ensure_serial_open():
    """Open the serial port on-demand (avoids import-time COM conflicts)."""
    global ser
    if ser is None or not getattr(ser, "is_open", False):
        ser = serial.Serial(
            port=SERIAL_PORT,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1,
        )
    return ser


XON = b'\x11' #character that klinger outputs when ready

#Commands List: 
MOVE_TO_NEGATIVE_29500 = "NX-29500"
MOVE_TO_ZERO = "NX0"
SET_HIGH_SPEED = "RX4000"

# ---------------- HELPERS ----------------
_serial_lock = threading.Lock()

def wait_for_xon(timeout_s=10.0):
    """Wait until controller sends XON (ready)."""
    s = _ensure_serial_open()
    deadline = time.time() + float(timeout_s)
    while time.time() < deadline:
        data = s.read(1)
        if data == XON:
            return
    raise TimeoutError("Timed out waiting for XON from Klinger.")

def send(cmd):
    """Send a command safely with handshake"""
    print(f"Sending: {cmd}")
    s = _ensure_serial_open()
    s.write((cmd + '\r').encode()) #adds a carriage return to the command

def send_and_wait(cmd, timeout_s=10.0):
    """Send one command, then wait for XON before returning."""
    with _serial_lock:
        s = _ensure_serial_open()
        # Clear any stale bytes so we don't accidentally match an older XON.
        try:
            s.reset_input_buffer()
        except Exception:
            pass
        send(cmd)
        wait_for_xon(timeout_s=timeout_s)

def set_high_speed(timeout_s=10.0):
    send_and_wait(SET_HIGH_SPEED, timeout_s=timeout_s)

def move_to_negative_29500(timeout_s=10.0):
    send_and_wait(MOVE_TO_NEGATIVE_29500, timeout_s=timeout_s)

def move_to_zero(timeout_s=10.0):
    send_and_wait(MOVE_TO_ZERO, timeout_s=timeout_s)

def initialize_at_startup(timeout_s=10.0):
    """RX4000 then NX-29500, with XON after each command."""
    set_high_speed(timeout_s=timeout_s)
    move_to_negative_29500(timeout_s=timeout_s)

def return_to_negative_29500(timeout_s=10.0):
    """Return the klinger stage to -29500."""
    move_to_negative_29500(timeout_s=timeout_s)
