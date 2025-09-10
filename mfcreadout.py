# Mass Flow rate readout for MFCs to get a constant readout of flow rates
import asyncio
import alicat
from alicat import FlowController

async def read_flow_rates():
    async with FlowController(address = 'COM3', unit = 'A') as mfc:
        data = await mfc.get() #This prints a dictionary with all the readout info; we want only the flow rate value
        z = str(data['volumetric_flow'])
        x = str(data['mass_flow'])
        print("Volumetric flow: " + z + ", mass flow: " + x) #prints the flow rate values only (dont know which one Sean wants yet)

if __name__ == '__main__':
    asyncio.run(read_flow_rates())