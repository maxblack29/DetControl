from alicat import FlowController
import asyncio
import time


async def auto():
    async with FlowController(address = 'COM3', unit = 'B') as mfc:
        await mfc.set_flow_rate(3.906) # In units of SLPM
        await asyncio.sleep(5)
        await mfc.set_flow_rate(0.0)
        
if __name__== '__main__':
    asyncio.run(auto())
