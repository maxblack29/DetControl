"""
Central MFC manager: one persistent serial connection per controller (A, B, C)
opened when the GUI starts. All Alicat commands go through this manager to avoid
repeated open/close and COM port conflicts.
"""
import asyncio
import threading
from alicat import FlowController

# Cached settings (updated when we set flow/gas)
gas_settings = {
    "A": {"gas": "C2H2", "setpoint": 0.0, "unit": "SLPM"},
    "B": {"gas": "H2", "setpoint": 0.0, "unit": "SLPM"},
    "C": {"gas": "O2", "setpoint": 0.0, "unit": "SLPM"},
    "D": {"gas": "N2", "setpoint": 0.0, "unit": "SLPM"},
}

DEFAULT_ADDRESS = "COM3"
# Controllers to open on this COM port (Alicat unit letters)
UNITS = ["A", "B", "C"]


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
        for unit in UNITS:
            mfc = FlowController(address=self._address, unit=unit)
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
            # Second attempt after a short pause (device busy / serial timing).
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

    def start(self, timeout=10):
        if self._thread is not None:
            return
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        if not self._ready.wait(timeout=timeout):
            raise RuntimeError("AlicatManager failed to open MFC connections in time")

    def _submit(self, coro, timeout=10):
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


def start_manager(timeout=10):
    """Create and start the manager (call once when GUI opens)."""
    get_manager().start(timeout=timeout)
