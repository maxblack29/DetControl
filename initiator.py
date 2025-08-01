# Test automation script for intiator testing without data acquisition (for now)
import nidaqmx
from nidaqmx.constants import LineGrouping
import nicontrol
import asyncio
import alicat 
from alicat import FlowController
from alicatcontrol import change_rate, zero
import time
#import os


async def connect(unit, setpoint):
    async with FlowController(address='COM3', unit=unit) as mfc:
        await mfc.set_flow_rate(setpoint)

async def test_initiator(setpointA, setpointB, setpointC):

    print("Test starting")

    await asyncio.gather(
        connect('A', setpointA),
        connect('B', setpointB),
        connect('C', setpointC)
    )

    await asyncio.sleep(1) 

    solenoids1 = [True, True, False, False, False, False, False, False] #Solenoid States at the Beginning of the Test
    nicontrol.set_digital_output(solenoids1)

    await asyncio.sleep(30)

    solenoids2 = [False]*8 #Purge solenoid states
    nicontrol.set_digital_output(solenoids2)

    await asyncio.gather(
        connect('A', 0.0), 
        connect('B', 0.0),
        connect('C', 0.0)
    )

    print("Test Complete! You can now change the setpoints of each MFC.")
    #Exhaust line and purge line are controlled by DIFFERENT solenoids. Exhaust line is next to manifold and purge line is closest to the table with the computer

async def stanpurge(setpointA, setpointB, setpointC):
    solenoids = [False] * 8
    nicontrol.set_digital_output(solenoids)
    await asyncio.gather(
        connect('A', setpointA),
        connect('B', setpointB),
        connect('C', setpointC)
    )

    print("Purge complete!")

    #Figure out the solenoid control based on how you plumb it today
async def emerpurge(setpointA, setpointB, setpointC):

    print("Emergency Purge Initiated")

    await asyncio.gather(
        connect('A', setpointA),
        connect('B', setpointB),
        connect('C', setpointC)
        )

    await asyncio.sleep(1)

    solenoids = [False]*8
    nicontrol.set_digital_output(solenoids)

    await asyncio.sleep(10)

    await connect('B', 0.000)

    print("Emergency Purge Complete")
    