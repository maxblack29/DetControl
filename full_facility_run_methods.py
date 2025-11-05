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

async def automatic_test(setpointA, setpointB, setpointC, setpointD, setpointC_driver):

    print("Test starting")

    #determine fill times based on molar flow rates
    molar_flow_rate_A = setpointA/60 * 101300 / (8.314 * 298)  # Convert SLPM to mol/s)
    molar_flow_rate_B = setpointA/60 * 101300 / (8.314 * 298)  # Convert SLPM to mol/s)
    molar_flow_rate_C = setpointA/60 * 101300 / (8.314 * 298)  # Convert SLPM to mol/s)

    total_molar_flow_rate = molar_flow_rate_A + molar_flow_rate_B + molar_flow_rate_C  # Total molar flow rate (mol/s)

    fill_volume = 14.2/1000  # Volume to be filled (m^3) 

    n_needed = 10000*fill_volume / (8.314*298)  # Moles needed to fill the volume at 10 kPa and 298 K

    fill_time = n_needed/ total_molar_flow_rate  # Time to fill (s)

    await asyncio.sleep(1) 

    #BEGIN TEST 
    #1: Open up valves to MFCs and vacuum down to 60 milTorr

    print("Vacuuming down...")

    turn_vacuum_on_array = [True, False, False, False, False, False, False, False] #Solenoid States to turn on vacuum pump
    nicontrol.set_digital_output_2(turn_vacuum_on_array)

    vacuum_solenoids = [True, True, True, True, True, True, True, False] #Solenoid States for Vacuuming Down. All open except S4 and S6 (normally closed) 
    nicontrol.set_digital_output(vacuum_solenoids)

    vacuum_running = True
    while vacuum_running:
        await(1)
        pressure_check = 0; #Replace with actual pressure reading function
        if pressure_check > 5:
            vacuum_running = False

    print("Vacuum down complete. Starting fill sequence...")
        
    post_vacuum_solenoids = [False, True, True, True, True, True, False, False] #Solenoid States Post Vacuuming Down. S1, S4, S5, S6, S7 closed
    nicontrol.set_digital_output(post_vacuum_solenoids)

    turn_vacuum_off_array = [False, False, False, False, False, False, False, False] #Solenoid States to turn off vacuum pump
    nicontrol.set_digital_output_2(turn_vacuum_off_array)

    #2: Fill 
        
    await asyncio.gather(
        connect('A', setpointA),
        connect('B', setpointB),
        connect('C', setpointC), 
        connect('D', 0.0)  
    )

    await asyncio.sleep(fill_time/2)
    #nicontrol.warning_sound()
    speaker = "cDAQ9188-169338EMod2/port0/line0:7"
    speakerstate = [False, False, False, True, False, True, False, False] #all closed except 4 and 6
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(speaker, line_grouping=LineGrouping.CHAN_PER_LINE)
        task.write(speakerstate)

    await asyncio.sleep(fill_time/2) 



    post_fill_solenoids = [False, True, False, False, False, False, False, False] #Solenoid states post fill 
    nicontrol.set_digital_output(post_fill_solenoids)

    await asyncio.sleep(1)

    #Driver Line
    # await asyncio.gather(
    #     connect('A', 0.0), 
    #     connect('B', 0.0),
    #     connect('C', setpointC_driver),
    #     connect('D', setpointD)
    # )

    # await asyncio.sleep(1) #1 second fill for driver gas 

    # await asyncio.gather(
    #     connect('A', 0.0), 
    #     connect('B', 0.0),
    #     connect('C', 0.0),
    #     connect('D', 0.0)
    # )

    print("Fill complete, Ignite and press the standard purge button")
    #Exhaust line and purge line are controlled by DIFFERENT solenoids. Exhaust line is next to manifold and purge line is closest to the table with the computer

async def purge(setpointA, setpointB, setpointC, setpointD):
    purge_solenoids = [False, False, False, False, False, False, False, False]
    nicontrol.set_digital_output(purge_solenoids)
    
    await asyncio.gather(
        connect('A', 0.0), 
        connect('B', 0.0),
        connect('C', 0.0),
        connect('D', 0.0)
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