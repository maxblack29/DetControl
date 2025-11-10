# Mass Flow rate readout for MFCs to get a constant readout of flow rates
import asyncio
from alicat import FlowController

# Mass Flow rate readout for MFCs to get a constant readout of flow rates
import asyncio
from alicat import FlowController

def read_flow_rateA():
    value = asyncio.run(read_flow_rateA_async())
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0  # Return 0.0 silently if the value is invalid

def read_flow_rateB():
    value = asyncio.run(read_flow_rateB_async())
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0  # Return 0.0 silently if the value is invalid

def read_flow_rateC():
    value = asyncio.run(read_flow_rateC_async())
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0  # Return 0.0 silently if the value is invalid

async def read_flow_rateA_async():
    try:
        async with FlowController(address='COM3', unit='A') as mfc:
            data = await mfc.get()
            return data.get('mass_flow', 0.0)  # Default to 0.0 if 'mass_flow' is missing
    except Exception:
        return 0.0  # Return 0.0 silently in case of any error

async def read_flow_rateB_async():
    try:
        async with FlowController(address='COM3', unit='B') as mfc:
            data = await mfc.get()
            return data.get('mass_flow', 0.0)  # Default to 0.0 if 'mass_flow' is missing
    except Exception:
        return 0.0  # Return 0.0 silently in case of any error

async def read_flow_rateC_async():
    try:
        async with FlowController(address='COM3', unit='C') as mfc:
            data = await mfc.get()
            return data.get('mass_flow', 0.0)  # Default to 0.0 if 'mass_flow' is missing
    except Exception:
        return 0.0  # Return 0.0 silently in case of any error