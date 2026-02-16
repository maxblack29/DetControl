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

    P_std = 101300      # Pa
    T_std = 298         # K
    R = 8.314           # J/mol·K

    molar_flow_rate_A = setpointA / 60 * 1e-3 * P_std / (R * T_std)  # mol/s
    molar_flow_rate_B = setpointB / 60 * 1e-3 * P_std / (R * T_std)  # mol/s
    molar_flow_rate_C = setpointC / 60 * 1e-3 * P_std / (R * T_std)  # mol/s

    # Total molar flow rate
    total_molar_flow_rate = molar_flow_rate_A + molar_flow_rate_B + molar_flow_rate_C  # mol/s

    # Volume to be filled (m³)
    fill_volume = 14.2 / 1000  # 14.2 L → 0.0142 m³

    # Moles needed to fill the volume to 10 kPa absolute at 298 K
    P_target = 10000  # Pa
    T_gas = 298       # K

    n_needed = P_target * fill_volume / (R * T_gas)  # mol

    # Time required to fill (s)
    fill_time = n_needed / total_molar_flow_rate

    await asyncio.sleep(1) 

    #BEGIN TEST 
    #1: Open up valves to MFCs and vacuum down to 60 milTorr

    print("Vacuuming down...")

    turn_vacuum_on_array = [True, False, False, False, False, False, False, False] #Solenoid States to turn on vacuum pump
    # nicontrol.set_digital_output_2(turn_vacuum_on_array)

    # vacuum_solenoids = [True, True, True, True, True, True, True, False] #Solenoid States for Vacuuming Down. All open except S4 and S6 (normally closed) 
    # nicontrol.set_digital_output(vacuum_solenoids)

    #check vacuum state
    # vacuum_running = False
    # while vacuum_running:
    #     await(1)
    #     vacuum_running = nicontrol.read_vaccuum_state(threshold = 1) #if receiving voltage above 1, vacuuming is complete

    print("Vacuum down complete. Starting fill sequence...")
        
    # post_vacuum_solenoids = [False, True, True, True, True, True, False, False] #Solenoid States Post Vacuuming Down. S1, S4, S5, S6, S7 closed
    # nicontrol.set_digital_output(post_vacuum_solenoids)

    # turn_vacuum_off_array = [False, False, False, False, False, False, False, False] #Solenoid States to turn off vacuum pump
    # nicontrol.set_digital_output_2(turn_vacuum_off_array)

    #2: Fill 
        
    await asyncio.gather(
        connect('A', setpointA),
        connect('B', setpointB),
        connect('C', setpointC), 
        connect('D', 0.0)  
    )

    await asyncio.sleep(fill_time)
    #Start Speaker 
    # speakerstate = [False, False, False, True, False, True, False, False] 
    # nicontrol.set_digital_output_2(speakerstate)

    # await asyncio.sleep(fill_time/2) 


    # #Zero MFCs and Close Fill Solenoids
    # post_fill_solenoids = [False, True, False, False, False, False, False, False] #Solenoid states post fill 
    # nicontrol.set_digital_output(post_fill_solenoids)

    

    #Driver Line
    # await asyncio.gather(
    #     connect('A', 0.0), 
    #     connect('B', 0.0),
    #     connect('C', setpointC_driver),
    #     connect('D', setpointD)
    # )

    # await asyncio.sleep(1) #1 second fill for driver gas 

    await asyncio.gather(
        connect('A', 0.0), 
        connect('B', 0.0),
        connect('C', 0.0),
        connect('D', 0.0)
    )

    await asyncio.sleep(1)

    print("Fill complete, Ignite and press the standard purge button")
   

async def purge(setpointA, setpointB, setpointC, setpointD):
    
    await asyncio.gather(
        connect('A', 0.0), 
        connect('B', 0.0),
        connect('C', 0.0),
        connect('D', 0.0)
    )
    
    purge_solenoids = [False, False, False, False, False, False, False, False]
    nicontrol.set_digital_output(purge_solenoids)
    
    print("Purging...")
    await asyncio.sleep(5)

    purge_complete_solenoids = [False, True, False, False, False, False, False, False]
    nicontrol.set_digital_output(purge_complete_solenoids)
    

    #Speaker Off 
    speakerstate = [False]*8 
    nicontrol.set_digital_output_2(speakerstate)

    print("Purge complete!")