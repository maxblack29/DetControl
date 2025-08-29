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

    await asyncio.sleep(15)
    #nicontrol.warning_sound()
    speaker = "cDAQ9188-169338EMod2/port0/line0:7"
    speakerstate = [False, True, False, False, False, False, False, False]
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(speaker, line_grouping=LineGrouping.CHAN_PER_LINE)
        task.write(speakerstate)

    await asyncio.sleep(15) 

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

    #turns off speaker
    speaker = "cDAQ9188-169338EMod2/port0/line0:7"
    speakerstate = [False] * 8
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(speaker, line_grouping=LineGrouping.CHAN_PER_LINE)
        task.write(speakerstate)

    await asyncio.gather(
        connect('A', 0.0),
        connect('B', 0.0),
        connect('C', 0.0)
    )

    print("Purge complete!")

    #Figure out the solenoid control based on how you plumb it today
    async def test_initiator_driver(setpointA, setpointB, setpointC, setpointD, setpointC_driver):

        print("Test starting")

        await asyncio.gather(
            connect('A', setpointA),
            connect('B', setpointB),
            connect('C', setpointC), 
            connect('D', 0.0)  
        )

        await asyncio.sleep(1) 

        solenoids1 = [True, True, False, False, False, False, False, False] #Solenoid States at the Beginning of the Test
        nicontrol.set_digital_output(solenoids1)

        await asyncio.sleep(15)
        #nicontrol.warning_sound()
        speaker = "cDAQ9188-169338EMod2/port0/line0:7"
        speakerstate = [False, True, False, False, False, False, False, False]
        with nidaqmx.Task() as task:
            task.do_channels.add_do_chan(speaker, line_grouping=LineGrouping.CHAN_PER_LINE)
            task.write(speakerstate)

        await asyncio.sleep(15) 



        solenoids2 = [False, True, False, False, False, False, False, False] #Purge solenoid states
        nicontrol.set_digital_output(solenoids2)

        await asyncio.sleep(1)

        #now fill the driver line

        await asyncio.gather(
            connect('A', 0.0), 
            connect('B', 0.0),
            connect('C', setpointC_driver),
            connect('D', setpointD)
        )

        await asyncio.sleep(1) #1 second fill for driver gas 

        await asyncio.gather(
            connect('A', 0.0), 
            connect('B', 0.0),
            connect('C', 0.0),
            connect('D', 0.0)
        )

        print("Fill complete, Ignite and press the standard purge button")
        #Exhaust line and purge line are controlled by DIFFERENT solenoids. Exhaust line is next to manifold and purge line is closest to the table with the computer

async def driver_purge(setpointA, setpointB, setpointC, setpointD):
    solenoids = [False, False, False, False, False, False, False, False]
    nicontrol.set_digital_output(solenoids)
    await asyncio.gather(
        connect('A', setpointA),
        connect('B', setpointB),
        connect('C', setpointC),
        connect('D', setpointD)
    )

    print("Purging...")
    await asyncio.sleep(5)

    solenoids3 = [False, True, False, False, False, False, False, False]
    nicontrol.set_digital_output(solenoids3)

    #turns off speaker
    speaker = "cDAQ9188-169338EMod2/port0/line0:7"
    speakerstate = [False] * 8
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(speaker, line_grouping=LineGrouping.CHAN_PER_LINE)
        task.write(speakerstate)

    await asyncio.gather(
        connect('A', 0.0),
        connect('B', 0.0),
        connect('C', 0.0),
        connect('D', 0.0)
    )

    print("Purge complete!")