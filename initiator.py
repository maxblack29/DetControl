# Test automation script for intiator testing without data acquisition (for now)
import nidaqmx
from nidaqmx.constants import LineGrouping
import nicontrol
import asyncio
import alicat 
from alicat import FlowController
from alicatcontrol import change_rate, zero
import time
import gc 
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

    solenoids2 = [False, True, False, False, False, False, False, False] #Purge solenoid states
    nicontrol.set_digital_output(solenoids2)

    await asyncio.sleep(1)

    await asyncio.gather(
        connect('A', 0.0), 
        connect('B', 0.0),
        connect('C', 0.0)
    )

    print("Fill complete, Ignite and press the standard purge button")
    #Exhaust line and purge line are controlled by DIFFERENT solenoids. Exhaust line is next to manifold and purge line is closest to the table with the computer

async def stanpurge(setpointA, setpointB, setpointC):
    solenoids = [False, False, False, False, False, False, False, False]
    nicontrol.set_digital_output(solenoids)
    await asyncio.gather(
        connect('A', setpointA),
        connect('B', setpointB),
        connect('C', setpointC)
    )

    print("Purging...")
    await asyncio.sleep(5)

    solenoids3 = [False, True, False, False, False, False, False, False]
    nicontrol.set_digital_output(solenoids3)


    await asyncio.gather(
        connect('A', 0.0),
        connect('B', 0.0),
        connect('C', 0.0)
    )

    print("Purge complete!")

    gc.collect()

    #Figure out the solenoid control based on how you plumb it today
