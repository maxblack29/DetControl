"""
Central MFC manager: one persistent serial connection per controller (A, B, C)
opened when the GUI starts. All Alicat commands go through this manager to avoid
repeated open/close and COM port conflicts.

Multiple FlowController instances on the same COM port must share ONE pyserial
handle and ONE asyncio lock; otherwise reads interleave and you get
UnicodeDecodeError / empty responses / "Could not read control point."
"""
import asyncio
import threading
import serial as pyserial

import alicat.util as alicat_util
from alicat import FlowController

# --- Patch numat/alicat SerialClient: shared port + shared lock per address ---

_port_entries = {}  # key -> {"ser", "refs"}


def _port_key(address, baudrate, bytesize, stopbits, parity, timeout):
    return (address, baudrate, bytesize, stopbits, parity, timeout)


def _patched_serial_init(
    self,
    address,
    baudrate=19200,
    timeout=0.15,
    bytesize=pyserial.EIGHTBITS,
    stopbits=pyserial.STOPBITS_ONE,
    parity=pyserial.PARITY_NONE,
):
    alicat_util.Client.__init__(self, timeout)
    self.address = address
    assert isinstance(self.address, str)
    self.serial_details = {
        "baudrate": baudrate,
        "bytesize": bytesize,
        "stopbits": stopbits,
        "parity": parity,
        "timeout": timeout,
    }
    key = _port_key(address, baudrate, bytesize, stopbits, parity, timeout)
    if key not in _port_entries:
        _port_entries[key] = {"ser": pyserial.Serial(address, **self.serial_details), "refs": 0}
    ent = _port_entries[key]
    ent["refs"] += 1
    self.ser = ent["ser"]
    self._port_key = key
    # One asyncio lock per COM port for all controllers on that port (set in _open_all).
    locks = getattr(alicat_util, "_shared_serial_locks", None)
    if locks is None or address not in locks:
        raise RuntimeError("Alicat shared lock not initialized; bug in AlicatManager._open_all")
    self.lock = locks[address]


async def _patched_serial_close(self):
    key = self._port_key
    ent = _port_entries[key]
    ent["refs"] -= 1
    if ent["refs"] <= 0:
        try:
            ent["ser"].close()
        except Exception:
            pass
        del _port_entries[key]
    self.open = False


async def _patched_readline(self) -> str:
    raw = self.ser.readline().strip()
    if not raw:
        return ""
    return raw.decode("latin-1", errors="replace").replace("\x00", "")


async def _patched_read(self, length: int) -> str:
    return self.ser.read(length).decode("latin-1", errors="replace")


alicat_util.SerialClient.__init__ = _patched_serial_init
alicat_util.SerialClient.close = _patched_serial_close
alicat_util.SerialClient._readline = _patched_readline
alicat_util.SerialClient._read = _patched_read

# Cached settings (updated when we set flow/gas)
gas_settings = {
    "A": {"gas": "C2H2", "setpoint": 0.0, "unit": "SLPM"},
    "B": {"gas": "H2", "setpoint": 0.0, "unit": "SLPM"},
    "C": {"gas": "O2", "setpoint": 0.0, "unit": "SLPM"},
    "D": {"gas": "N2", "setpoint": 0.0, "unit": "SLPM"},
}

DEFAULT_ADDRESS = "COM3"
<<<<<<< HEAD
# Controllers to open on this COM port (Alicat unit letters)
UNITS = ["A", "B", "C"]
=======
# Match Alicat front-panel unit IDs (A–Z). Must match hardware addressing on the multidrop line.
UNITS = ["A", "B", "C"]

# Serial settings passed to FlowController -> SerialClient (must match device menu).
DEFAULT_BAUDRATE = 19200
# Slightly longer timeout helps RS-485 / multidrop turnarounds.
DEFAULT_SERIAL_TIMEOUT = 0.5


def _flow_kwargs():
    return {
        "baudrate": DEFAULT_BAUDRATE,
        "timeout": DEFAULT_SERIAL_TIMEOUT,
    }
>>>>>>> bd9bae6f7cc0f362f8fb177ce2510fd83112400b


class AlicatManager:
    """Keeps FlowController connections open for each entry in UNITS. Runs one asyncio loop in a dedicated thread."""

    def __init__(self, address=DEFAULT_ADDRESS):
        self._address = address
        self._loop = None
        self._thread = None
        self._mfcs = {}  # unit -> FlowController (after __aenter__)
        self._ready = threading.Event()
        self._last_gas = {}  # unit -> last gas string sent (avoid redundant set_gas)

    async def _open_all(self):
        # Must exist before any FlowController constructs SerialClient (see patched __init__).
        if not hasattr(alicat_util, "_shared_serial_locks"):
            alicat_util._shared_serial_locks = {}
        if self._address not in alicat_util._shared_serial_locks:
            alicat_util._shared_serial_locks[self._address] = asyncio.Lock()

        kw = _flow_kwargs()
        for unit in UNITS:
            mfc = FlowController(address=self._address, unit=unit, **kw)
            await mfc.__aenter__()
            self._mfcs[unit] = mfc
        self._ready.set()

    async def _close_all(self):
        for unit in list(self._mfcs.keys()):
            try:
                await self._mfcs[unit].__aexit__(None, None, None)
            except Exception:
                pass
            self._mfcs.pop(unit, None)

    async def _set_flow_rate(self, unit, setpoint):
        await self._mfcs[unit].set_flow_rate(setpoint)
        data = await self._mfcs[unit].get()
        if unit in gas_settings:
            gas_settings[unit]["setpoint"] = float(setpoint)
        return float(data.get("mass_flow", setpoint))

    async def _set_gas(self, unit, gas):
        gas = str(gas).strip()
        if self._last_gas.get(unit) == gas:
            return
        mfc = self._mfcs[unit]
        try:
            await mfc.set_gas(gas)
        except OSError as e:
            if "Cannot set gas" in str(e):
                await asyncio.sleep(0.2)
                await mfc.set_gas(gas)
            else:
                raise
        await asyncio.sleep(0.05)
        self._last_gas[unit] = gas
        if unit in gas_settings:
            gas_settings[unit]["gas"] = gas
        print(f"Set gas for controller {unit} to {gas}")

    async def _read_flows(self):
        out = {}
        for u in UNITS:
            data = await self._mfcs[u].get()
            out[u] = float(data.get("mass_flow", 0.0))
            await asyncio.sleep(0.02)
        return out

    def _run_loop(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_until_complete(self._open_all())
            self._loop.run_forever()
        finally:
            self._loop.run_until_complete(self._close_all())
            self._loop.close()

    def start(self, timeout=30):
        if self._thread is not None:
            return
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        if not self._ready.wait(timeout=timeout):
            raise RuntimeError("AlicatManager failed to open MFC connections in time")

    def _submit(self, coro, timeout=30):
        if self._loop is None:
            raise RuntimeError("AlicatManager not started; call start() first")
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return future.result(timeout=timeout)

    def set_flow_rate(self, unit, setpoint):
        """Set flow rate for one unit; returns current volumetric flow (SLPM)."""
        if unit not in self._mfcs:
            return 0.0
        return self._submit(self._set_flow_rate(unit, float(setpoint)))

    def set_gas(self, unit, gas):
        """Set gas type for one unit. No-op if that unit is not in UNITS (not opened)."""
        if unit not in self._mfcs:
            return
        self._submit(self._set_gas(unit, gas))

    def read_flows(self):
        """Return dict {'A': flow_a, 'B': flow_b, 'C': flow_c} in SLPM."""
        return self._submit(self._read_flows())

    def stop(self):
        if self._loop is None:
            return

        async def _shutdown():
            await self._close_all()
            self._loop.stop()

        self._loop.call_soon_threadsafe(
            lambda: asyncio.ensure_future(_shutdown(), loop=self._loop)
        )


_manager = None
_lock = threading.Lock()


def get_manager():
    global _manager
    with _lock:
        if _manager is None:
            _manager = AlicatManager()
        return _manager


def start_manager(timeout=30):
    """Create and start the manager (call once when GUI opens)."""
    get_manager().start(timeout=timeout)
