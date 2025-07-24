# Test automation script for intiator testing without data acquisition (for now)
import nidaqmx
import asyncio
import alicat 
from alicat import FlowController
from alicatcontrol import change_rate, zero


async def test_initiator(setpointA, setpointB, setpointC):
    #with nidaqmx.Task() as task:
        #Step 1, control two solenoids to open and close right here that control the gas flow to the intiator and exhaust. Exhaust is closed
        #(normally open solenoid) and initator flow is open (normally closed solenoid)
    #Step 2, set the desired flow rate for the gas to the intiator
    async with FlowController(address = 'COM3', unit = 'A') as mfc:
        await mfc.set_flow_rate(setpointA)
        await asyncio.sleep(30)
        await mfc.set_flow_rate(0.0)
    async with FlowController(address = 'COM3', unit = 'B') as mfc:
        await mfc.set_flow_rate(setpointB)
        await asyncio.sleep(30)
        await mfc.set_flow_rate(0.0)
    async with FlowController(address = 'COM3', unit = 'C') as mfc:
        await mfc.set_flow_rate(setpointC)
        await asyncio.sleep(30)
        await mfc.set_flow_rate(0.0)
    #Step 3, Open exhaust valve and ignite initiator as soon after as possible
    #Step 4, purge the system (open the exhaust valve)
    #Step 5, close the exhaust valve and reopen the initiator valve to redo the test

    #Exhaust line and purge line are controlled by DIFFERENT solenoids. Exhaust line is next to manifold and purge line is closest to the table with the computer



# if __name__ == '__main__': function here? 
    