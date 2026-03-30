# Test automation script for intiator testing without data acquisition (for now)
import csv
import os
import nicontrol
import asyncio
import time
# import klinger_control  # analog-branch: Klinger integration deferred for later testing
# import threading

# Same base path as detonation test data CSV
FILL_LOG_DIR = r"C:\Users\dedic-lab\Documents\Detonation_Facility_Testing"
FILL_LOG_INTERVAL_S = 0.1  # target dt for analog logging during fill


def _set_mfc_rates(setpoint_a, setpoint_b, setpoint_c):
    """Set flow rates through analog output (Mod7 ao0:2, 0-5 V)."""
    nicontrol.set_mfc_setpoints_analog(setpoint_a, setpoint_b, setpoint_c)


async def automatic_test(setpointA, setpointB, setpointC, setpointD, setpointC_driver, on_fill_complete=None, on_mfc_setpoints_changed=None, fill_time_s=0.0, testcount=None):

    print("Test starting")

    # P_std = 101300      # Pa
    # T_std = 298         # K
    # R = 8.314           # J/mol·K

    # molar_flow_rate_A = setpointA / 60 * 1e-3 * P_std / (R * T_std)  # mol/s
    # molar_flow_rate_B = setpointB / 60 * 1e-3 * P_std / (R * T_std)  # mol/s
    # molar_flow_rate_C = setpointC / 60 * 1e-3 * P_std / (R * T_std)  # mol/s

    # # Total molar flow rate
    # total_molar_flow_rate = molar_flow_rate_A + molar_flow_rate_B + molar_flow_rate_C  # mol/s


    # # Volume to be filled (m³)
    # fill_volume = 14.2 / 1000  # 14.2 L full facility volume → 0.0142 m³

    # # Moles needed to fill the volume to 10 kPa absolute at 298 K
    # P_target = 10000 # Pa
    # T_gas = 298       # K

    # n_needed = P_target * fill_volume / (R * T_gas)  # mol

    # Time required to fill (s)
    # fill_time = n_needed / total_molar_flow_rate if total_molar_flow_rate > 0 else 0.0
    fill_time = max(0.0, float(fill_time_s))
    print(f"Using fill time input: {fill_time:.2f} s")

    # Move the Klinger stage to zero in the background (don't block the test start).
    # threading.Thread(target=klinger_control.move_to_zero, daemon=True).start()

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

    # Log analog MFC feedback during fill at FILL_LOG_INTERVAL_S
    speaker_on_daq_2 = [True, True, True, False, False, False, False, False]
    fill_rows = []
    start_fill = time.perf_counter()
    speaker_done = False

    while True:
        elapsed = time.perf_counter() - start_fill
        flow_a, flow_b, flow_c = nicontrol.read_mfc_flows_analog_once()
        fill_rows.append([elapsed, setpointA, flow_a, setpointB, flow_b, setpointC, flow_c])

        if (not speaker_done) and elapsed >= (fill_time / 2.0):
            nicontrol.set_digital_output_2(speaker_on_daq_2)
            speaker_done = True
        if elapsed >= fill_time:
            break
        await asyncio.sleep(min(FILL_LOG_INTERVAL_S, max(0.0, fill_time - elapsed)))

    if testcount is not None and len(fill_rows) > 0:
        os.makedirs(FILL_LOG_DIR, exist_ok=True)
        path = os.path.join(FILL_LOG_DIR, f"fill_flow_rates_test{testcount}.csv")
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["time_s", "setpoint_A_SLPM", "flow_A_SLPM", "setpoint_B_SLPM", "flow_B_SLPM", "setpoint_C_SLPM", "flow_C_SLPM"])
            w.writerows(fill_rows)

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
    await asyncio.sleep(60)

    purge_complete_daq1 = [False, False, True, False, False, False, False, False]
    nicontrol.set_digital_output(purge_complete_daq1)
    purge_complete_daq2 = [True, True, False, False, False, False, False, False]
    nicontrol.set_digital_output_2(purge_complete_daq2)
    
    print("Purge complete!")