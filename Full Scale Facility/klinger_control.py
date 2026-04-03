"""
Klinger MC4 stepper control over RS-232 (same command sequences as the original test script).

Use move_to_negative_29500() / move_to_zero() from background threads during automatic test;
serial access is serialized with a lock so ignite homing waits if a move is in progress.
"""

import os
import threading
import time

import serial

XON = b"\x11"

_lock = threading.Lock()
_ser = None

# Default matches prior test setup; override with env KLINGER_COM if needed.
_DEFAULT_PORT = os.environ.get("KLINGER_COM", "COM1")


def _get_serial():
    """Open the serial port once (lazy) so importing this module does not require hardware."""
    global _ser
    if _ser is not None and _ser.is_open:
        return _ser
    _ser = serial.Serial(
        port=_DEFAULT_PORT,
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=0.1,
    )
    _ser.reset_input_buffer()
    return _ser


def wait_for_xon(ser):
    while True:
        data = ser.read(1)
        if data == XON:
            return


def _send(ser, cmd):
    ser.write((cmd + "\r").encode())


def move_to_negative_29500():
    """Move stage to -29500 (blocking; call from a worker thread for non-blocking GUI)."""
    try:
        with _lock:
            ser = _get_serial()
            _send(ser, "RX4000")
            time.sleep(0.2)
            _send(ser, "-X")
            time.sleep(0.2)
            _send(ser, "NX29500")
            time.sleep(0.2)
            _send(ser, "MX")
            wait_for_xon(ser)
    except Exception as e:
        print("Klinger move_to_negative_29500 failed:", e)


def move_to_zero():
    """Move stage back to 0 after negative travel (blocking)."""
    try:
        with _lock:
            ser = _get_serial()
            _send(ser, "RX4000")
            time.sleep(0.2)
            _send(ser, "+X")
            time.sleep(0.2)
            _send(ser, "NX29500")
            time.sleep(0.2)
            _send(ser, "MX")
            wait_for_xon(ser)
    except Exception as e:
        print("Klinger move_to_zero failed:", e)
