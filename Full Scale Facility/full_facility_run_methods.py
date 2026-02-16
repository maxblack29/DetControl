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
        #figure out way to change last sent flow rate from here 
        await mfc.set_flow_rate(setpoint)

async def automatic_test(setpointA, setpointB, setpointC, setpointD, setpointC_driver, on_fill_complete=None, on_mfc_setpoints_changed=None):

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
    #1: Open up valves to MFCs and vacuum down to 60 milTorr (done manually in these first tests)-------------------------------------------------------------------------------------------------

    #print("Vacuuming down...")

    #turn_vacuum_on_array = [True, False, False, False, False, False, False, False] #Solenoid States to turn on vacuum pump
    #nicontrol.set_digital_output_2(turn_vacuum_on_array)

     #vacuum_solenoids = [True, True, True, True, True, True, True, False] #Solenoid States for Vacuuming Down. All open except S4 and S6 (normally closed) 
     #nicontrol.set_digital_output(vacuum_solenoids)

    #check vacuum state
    # vacuum_running = False
    # while vacuum_running:
    #     await(1)
    #     vacuum_running = nicontrol.read_vaccuum_state(threshold = 1) #if receiving voltage above 1, vacuuming is complete

    print("Vacuum down complete. Starting fill sequence...")
        
    daq_1 = [True, True, True, False, False, False, False, False] #DAQ 1 States Post Vacuuming Down. Fuel and Oxidizer/Diluent open, purge closed
    nicontrol.set_digital_output(daq_1)
    daq_2 = [True, True, False, False, False, False, False, False] #DAQ 2 States Post Vacuuming Down. Exhaust closed, Pressure reading open
    nicontrol.set_digital_output_2(daq_2)

    #turn_vacuum_off_array = [False, False, False, False, False, False, False, False] #Solenoid States to turn off vacuum pump
    #nicontrol.set_digital_output_2(turn_vacuum_off_array)

    #2: Fill---------------------------------------------------------------------------------------------------------------------------------------------------
        
    await asyncio.gather(
        connect('A', setpointA),
        connect('B', setpointB),
        connect('C', setpointC),
    )
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(setpointA, setpointB, setpointC)

    #Start Speaker After Half the Fill Time
    await asyncio.sleep(fill_time/2) 
    speaker_on_daq_2 = [True, True, True, False, False, False, False, False] #State for speaker on
    nicontrol.set_digital_output_2(speaker_on_daq_2)

    

    await asyncio.sleep(fill_time/2) 
    # #Zero MFCs and Close Fill Solenoids
    post_fill_daq1 = [False, False, True, True, False, False, False, False] #Daq1 states post fill 
    nicontrol.set_digital_output(post_fill_daq1)
    post_fill_daq2 = [True, False, True, False, False, False, False, False] #Daq2 states post fill 
    nicontrol.set_digital_output_2(post_fill_daq2)
    
    #need to read a pressure here once tap is closed 


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
    )
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(0.0, 0.0, 0.0)

    await asyncio.sleep(1)

    if on_fill_complete is not None:
        on_fill_complete()

    print("Fill complete, Ignite and press the standard purge button")
   

async def purge(setpointA, setpointB, setpointC, setpointD, on_mfc_setpoints_changed=None):

    await asyncio.gather(
        connect('A', 0.0),
        connect('B', 0.0),
        connect('C', 0.0),
    )
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(0.0, 0.0, 0.0)

    purge_daq1 = [False, False, False, False, False, False, False, False]
    nicontrol.set_digital_output(purge_daq1)
    purge_daq2 = [False, False, False, False, False, False, False, False]
    nicontrol.set_digital_output_2(purge_daq2)
    
    print("Purging...")
    await asyncio.sleep(30)

    purge_complete_daq1 = [False, False, True, False, False, False, False, False]
    nicontrol.set_digital_output(purge_complete_daq1)
    purge_complete_daq2 = [False, False, False, False, False, False, False, False]
    nicontrol.set_digital_output_2(purge_complete_daq2)
    
    print("Purge complete!")