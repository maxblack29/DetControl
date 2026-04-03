# Test automation script for intiator testing without data acquisition (for now)
import csv
import os
import nicontrol
import asyncio
import threading
import time

import klinger_control

# Same base path as detonation test data CSV
FILL_LOG_DIR = r"C:\Users\dedic-lab\Documents\Detonation_Facility_Testing"
FILL_LOG_INTERVAL_S = 0.1  # target dt for analog logging during fill

# Mod1: S1–S4 on 0–3, S5 purge (NO) on 6. Mod2: S6 exhaust (NO) on 0, S7 gauge on 1; timing on 6, speaker on 7.
# True = NC open; NO valves: True = closed, False = open.

def _pad8(x):
    return list((list(x) + [False] * 8)[:8])


# Start reactant fill: driver lines closed, reactant mix open, purge closed, exhaust closed, gauge open.
FILL_START_DAQ1 = [False, False, False, True, False, False, True, False]
FILL_START_DAQ2 = [True, True, False, False, False, False, False, False]

# After fill: reactant mix closed; speaker off (line 7 False).
POST_FILL_DAQ1 = [False, False, False, False, False, False, True, False]
POST_FILL_DAQ2 = [True, True, False, False, False, False, False, False]

# Idle / post-purge: same as GUI startup default.
PURGE_COMPLETE_DAQ1 = [False, False, False, True, False, False, True, False]
PURGE_COMPLETE_DAQ2 = [True, True, False, False, False, False, False, False]


def _set_mfc_rates(setpoint_a, setpoint_b, setpoint_c, setpoint_d=0.0):
    """Set flow rates through analog output (Mod7 ao0:3, 0–5 V)."""
    nicontrol.set_mfc_setpoints_analog(setpoint_a, setpoint_b, setpoint_c, setpoint_d)


async def automatic_test(
    setpointA, setpointB, setpointC, setpointD, setpointC_driver,
    on_fill_complete=None, on_mfc_setpoints_changed=None, fill_time_s=0.0, testcount=None,
):

    print("Test starting")

    try:
        threading.Thread(target=klinger_control.move_to_negative_29500, daemon=True).start()
    except Exception as e:
        print("Klinger automatic-test move to -29500 could not start:", e)

    fill_time = max(0.0, float(fill_time_s))
    print(f"Using fill time input: {fill_time:.2f} s")

    print("Vacuum down complete. Starting fill sequence...")

    nicontrol.set_digital_output(_pad8(FILL_START_DAQ1))
    nicontrol.set_digital_output_2(_pad8(FILL_START_DAQ2))

    _set_mfc_rates(setpointA, setpointB, setpointC, 0.0)
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(setpointA, setpointB, setpointC, 0.0)

    fill_rows = []
    start_fill = time.perf_counter()
    speaker_done = False

    while True:
        elapsed = time.perf_counter() - start_fill
        flow_a, flow_b, flow_c, flow_d = nicontrol.read_mfc_flows_analog_once()
        fill_rows.append(
            [elapsed, setpointA, flow_a, setpointB, flow_b, setpointC, flow_c, 0.0, flow_d]
        )

        if (not speaker_done) and elapsed >= (fill_time / 2.0):
            nicontrol.set_daq2_line(nicontrol.DAQ2_LINE_SPEAKER, True)
            speaker_done = True
        if elapsed >= fill_time:
            break
        await asyncio.sleep(min(FILL_LOG_INTERVAL_S, max(0.0, fill_time - elapsed)))

    if testcount is not None and len(fill_rows) > 0:
        os.makedirs(FILL_LOG_DIR, exist_ok=True)
        path = os.path.join(FILL_LOG_DIR, f"fill_flow_rates_test{testcount}.csv")
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(
                [
                    "time_s",
                    "setpoint_A_SLPM",
                    "flow_A_SLPM",
                    "setpoint_B_SLPM",
                    "flow_B_SLPM",
                    "setpoint_C_SLPM",
                    "flow_C_SLPM",
                    "setpoint_D_SLPM",
                    "flow_D_SLPM",
                ]
            )
            w.writerows(fill_rows)

    if on_fill_complete is not None:
        on_fill_complete()

    nicontrol.set_digital_output(_pad8(POST_FILL_DAQ1))
    nicontrol.set_digital_output_2(_pad8(POST_FILL_DAQ2))

    _set_mfc_rates(0.0, 0.0, 0.0, 0.0)
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(0.0, 0.0, 0.0, 0.0)

    print("Fill complete. Run driver sequence if needed, then Ignite; use Purge when done.")


async def driver_sequence(
    setpoint_d,
    setpoint_c_ox,
    driver_fill_time_s,
    on_mfc_setpoints_changed=None,
):
    """Driver line: MFC D carrier, S2 fuel pulse, S3 oxidizer (MFC C setpoint 2), S1 mix for driver_fill_time."""
    d1, d2 = nicontrol.get_daq_states()
    d1 = _pad8(d1)
    d2 = _pad8(d2)

    t_mix = max(0.0, float(driver_fill_time_s))

    _set_mfc_rates(0.0, 0.0, 0.0, float(setpoint_d))
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(0.0, 0.0, 0.0, float(setpoint_d))
    await asyncio.sleep(0.05)

    # Driver fuel 2 s
    d1[1] = True
    nicontrol.set_digital_output(d1)
    nicontrol.set_digital_output_2(d2)
    await asyncio.sleep(2.0)
    d1[1] = False
    nicontrol.set_digital_output(d1)

    # Driver oxidizer (same MFC C gas, second setpoint) 2 s
    _set_mfc_rates(0.0, 0.0, float(setpoint_c_ox), float(setpoint_d))
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(0.0, 0.0, float(setpoint_c_ox), float(setpoint_d))
    d1[2] = True
    nicontrol.set_digital_output(d1)
    await asyncio.sleep(2.0)
    d1[2] = False
    nicontrol.set_digital_output(d1)
    _set_mfc_rates(0.0, 0.0, 0.0, float(setpoint_d))
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(0.0, 0.0, 0.0, float(setpoint_d))

    # Driver mix for driver_fill_time
    d1[0] = True
    nicontrol.set_digital_output(d1)
    await asyncio.sleep(t_mix)
    d1[0] = False
    nicontrol.set_digital_output(d1)

    _set_mfc_rates(0.0, 0.0, 0.0, 0.0)
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(0.0, 0.0, 0.0, 0.0)

    print("Driver sequence complete. You may Ignite.")


async def purge(setpointA, setpointB, setpointC, setpointD, on_mfc_setpoints_changed=None):
    _set_mfc_rates(0.0, 0.0, 0.0, 0.0)
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(0.0, 0.0, 0.0, 0.0)

    purge_daq1 = [False] * 8
    purge_daq2 = [False] * 8
    nicontrol.set_digital_output(purge_daq1)
    nicontrol.set_digital_output_2(purge_daq2)

    print("Purging...")
    await asyncio.sleep(60)

    nicontrol.set_digital_output(_pad8(PURGE_COMPLETE_DAQ1))
    nicontrol.set_digital_output_2(_pad8(PURGE_COMPLETE_DAQ2))

    print("Purge complete!")
