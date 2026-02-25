# Test automation script for intiator testing without data acquisition (for now)
import csv
import os
import nidaqmx
from nidaqmx.constants import LineGrouping
import nicontrol
import asyncio
import alicatcontrol
import time
import gc

# Same base path as detonation test data CSV
FILL_LOG_DIR = r"C:\Users\dedic-lab\Documents\Detonation_Facility_Testing"
FILL_LOG_INTERVAL_S = 0.5  # log flow rates every 0.5 s during fill


def _set_mfc_rates(setpoint_a, setpoint_b, setpoint_c):
    """Set flow rates via the persistent MFC manager (no per-call COM open/close)."""
    manager = alicatcontrol.get_manager()
    manager.set_flow_rate("A", setpoint_a)
    manager.set_flow_rate("B", setpoint_b)
    manager.set_flow_rate("C", setpoint_c)


async def automatic_test(setpointA, setpointB, setpointC, setpointD, setpointC_driver, on_fill_complete=None, on_mfc_setpoints_changed=None, testcount=None):

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
    fill_volume = 14.2 / 1000  # 14.2 L full facility volume → 0.0142 m³

    # Moles needed to fill the volume to 10 kPa absolute at 298 K
    P_target = 10000 # Pa
    T_gas = 298       # K

    n_needed = P_target * fill_volume / (R * T_gas)  # mol

    # Time required to fill (s)
    fill_time = n_needed / total_molar_flow_rate

    print(fill_time) 

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

    #2: Fill — set rates and log time / setpoint / actual flow every FILL_LOG_INTERVAL_S
    _set_mfc_rates(setpointA, setpointB, setpointC)
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(setpointA, setpointB, setpointC)

    manager = alicatcontrol.get_manager()
    fill_log_rows = []
    start_fill = time.perf_counter()
    speaker_done = False
    speaker_on_daq_2 = [True, True, True, False, False, False, False, False]

    while True:
        elapsed = time.perf_counter() - start_fill
        flows = manager.read_flows()
        fill_log_rows.append((
            round(elapsed, 3),
            setpointA, flows.get("A", 0.0),
            setpointB, flows.get("B", 0.0),
            setpointC, flows.get("C", 0.0),
        ))
        if elapsed >= fill_time / 2 and not speaker_done:
            speaker_done = True
            nicontrol.set_digital_output_2(speaker_on_daq_2)
        if elapsed >= fill_time:
            break
        await asyncio.sleep(min(FILL_LOG_INTERVAL_S, fill_time - elapsed))

    if testcount is not None and fill_log_rows:
        os.makedirs(FILL_LOG_DIR, exist_ok=True)
        path = os.path.join(FILL_LOG_DIR, f"fill_flow_rates_test{testcount}.csv")
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["time_s", "setpoint_A_SLPM", "flow_A_SLPM", "setpoint_B_SLPM", "flow_B_SLPM", "setpoint_C_SLPM", "flow_C_SLPM"])
            w.writerows(fill_log_rows)

    #read pressure
    if on_fill_complete is not None:
        on_fill_complete()

    # #Zero MFCs and Close Fill Solenoids
    post_fill_daq1 = [False, False, True, True, False, False, False, False] #Daq1 states post fill 
    nicontrol.set_digital_output(post_fill_daq1)
    post_fill_daq2 = [True, False, True, False, False, False, False, False] #Daq2 states post fill 
    nicontrol.set_digital_output_2(post_fill_daq2)
    

    #Driver Line
    # await asyncio.gather(
    #     connect('A', 0.0), 
    #     connect('B', 0.0),
    #     connect('C', setpointC_driver),
    #     connect('D', setpointD)
    # )

    # await asyncio.sleep(1) #1 second fill for driver gas 

    _set_mfc_rates(0.0, 0.0, 0.0)
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(0.0, 0.0, 0.0)

    await asyncio.sleep(1)

    print("Fill complete, Ignite and press the standard purge button")
   

async def purge(setpointA, setpointB, setpointC, setpointD, on_mfc_setpoints_changed=None):
    _set_mfc_rates(0.0, 0.0, 0.0)
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(0.0, 0.0, 0.0)

    purge_daq1 = [False, False, False, False, False, False, False, False]
    nicontrol.set_digital_output(purge_daq1)
    purge_daq2 = [False, False, False, False, False, False, False, False]
    nicontrol.set_digital_output_2(purge_daq2)
    
    print("Purging...")
    await asyncio.sleep(5)

    purge_complete_daq1 = [False, False, True, False, False, False, False, False]
    nicontrol.set_digital_output(purge_complete_daq1)
    purge_complete_daq2 = [True, True, False, False, False, False, False, False]
    nicontrol.set_digital_output_2(purge_complete_daq2)
    
    print("Purge complete!")