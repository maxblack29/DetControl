import asyncio
from alicat import FlowController
import time #Don't know if I actually need this yet, figured I would import it just in case

gas_settings = {
    "A": {"gas": "C2H2", "setpoint": 0.0, "unit": "SLPM"},
    "B": {"gas": "H2", "setpoint": 0.0, "unit": "SLPM"},
    "C": {"gas": "O2", "setpoint": 0.0, "unit": "SLPM"},
    "D": {"gas": "N2", "setpoint": 0.0, "unit": "SLPM"},
}

async def get():
    #Establish connections with mass flow controllers A, B, and C
    for unit in ['A', 'B', 'C']:
        async with FlowController(address = 'COM3', unit = unit) as mfc:
            print(await mfc.get())

async def change_rate(unit, setpoint):
    """Set flow rate and return the current volumetric flow reported by the controller."""
    async with FlowController(address="COM3", unit=unit) as mfc:
        await mfc.set_flow_rate(setpoint)  # In units of SLPM
        data = await mfc.get()
        # Update cached settings
        if unit in gas_settings:
            gas_settings[unit]["setpoint"] = float(setpoint)
        return float(data.get("volumetric_flow", setpoint))


async def zero():
    controller = ['A', 'B', 'C'] #Add D when the controller is in place
    for unit in ['A', 'B', 'C']:
        async with FlowController(address = 'COM3', unit = unit) as mfc:
            x = mfc.set_flow_rate(0.0)
            await x
            if unit := 0.0:
                print(f'{unit} failed to reset to 0.0')
            else:
                print('All controllers reset to 0.0 SLPM') #continues to loop 3 times, figure out later after user input list

async def set_gas(unit, gas):
    async with FlowController(address = 'COM3', unit = unit) as mfc:
        await mfc.set_gas(gas)
        print(f'Set gas for controller {unit} to {gas}')

async def read_flows_all():
    """Read current volumetric flow for controllers A, B, C and return a dict."""
    results = {}
    for unit in ['A', 'B', 'C']:
        async with FlowController(address='COM3', unit=unit) as mfc:
            data = await mfc.get()
            results[unit] = float(data.get('volumetric_flow', 0.0))
    return results

if __name__ == '__main__':
    #Global settings for the flow controllers
    asyncio.run(get())
    asyncio.run(change_rate(unit='A', setpoint = 0.0))
    asyncio.run(change_rate(unit='B', setpoint = 0.0))

