# Mass Flow rate readout for MFCs to get a constant readout of flow rates
import asyncio
from alicat import FlowController

async def read_flow_rateA_async():
    async with FlowController(address='COM3', unit='A') as mfc:
        data = await mfc.get()
        print("DEBUG: mfc.get() returned:", data)
        x = data.get('mass_flow')
        print("DEBUG: mass_flow value:", x)
        return x

def read_flow_rateA():
    value = asyncio.run(read_flow_rateA_async())
    try:
        return float(value)
    except (TypeError, ValueError):
        print(f"Invalid mass_flow value: {value}")
        return 0.0


async def read_flow_rateB_async():
    async with FlowController(address='COM3', unit='B') as mfc:
        data = await mfc.get()
        print("DEBUG: mfc.get() returned:", data)
        x = data.get('mass_flow')
        print("DEBUG: mass_flow value:", x)
        return x

def read_flow_rateB():
    value = asyncio.run(read_flow_rateB_async())
    try:
        return float(value)
    except (TypeError, ValueError):
        print(f"Invalid mass_flow value: {value}")
        return 0.0

async def read_flow_rateC_async():
    async with FlowController(address='COM3', unit='C') as mfc:
        data = await mfc.get()
        print("DEBUG: mfc.get() returned:", data)
        x = data.get('mass_flow')
        print("DEBUG: mass_flow value:", x)
        return x

def read_flow_rateC():
    value = asyncio.run(read_flow_rateC_async())
    try:
        return float(value)
    except (TypeError, ValueError):
        print(f"Invalid mass_flow value: {value}")
        return 0.0

if __name__ == '__main__':
    print(read_flow_rateB())
    print(read_flow_rateC())