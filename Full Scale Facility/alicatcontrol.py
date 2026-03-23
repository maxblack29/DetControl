"""Serial-only Alicat manager: gas switching + GUI flow readback."""
import asyncio
import threading
from alicat import FlowController

DEFAULT_ADDRESS = "COM3"
UNITS = ["A", "B", "C"]


class AlicatManager:
    def __init__(self, address=DEFAULT_ADDRESS):
        self._address = address
        self._loop = None
        self._thread = None
        self._mfcs = {}
        self._ready = threading.Event()

    async def _open_all(self):
        for unit in UNITS:
            mfc = FlowController(address=self._address, unit=unit)
            await mfc.__aenter__()
            self._mfcs[unit] = mfc
        self._ready.set()

    async def _close_all(self):
        for unit, mfc in list(self._mfcs.items()):
            try:
                await mfc.__aexit__(None, None, None)
            except Exception:
                pass
            self._mfcs.pop(unit, None)

    async def _set_gas(self, unit, gas):
        await self._mfcs[unit].set_gas(gas)

    async def _read_flows(self):
        out = {}
        for unit in UNITS:
            data = await self._mfcs[unit].get()
            out[unit] = float(data.get("mass_flow", 0.0))
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
        return asyncio.run_coroutine_threadsafe(coro, self._loop).result(timeout=timeout)

    def set_gas(self, unit, gas):
        self._submit(self._set_gas(unit, gas))

    def read_flows(self):
        return self._submit(self._read_flows())

    def stop(self):
        if self._loop is not None:
            self._loop.call_soon_threadsafe(self._loop.stop)


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
