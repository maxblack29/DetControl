import nicontrol
import asyncio
import threading

import fill_log_csv
import klinger_control
import bnc_box_control


# Hardware sample clock for fill CSV (Hz). Row spacing = 1 / FILL_LOG_SAMPLE_RATE_HZ.
FILL_LOG_SAMPLE_RATE_HZ = 1000.0
# Pre/post capture around the scripted experiment (aligns with asyncio.sleep below).
FILL_LOG_BUFFER_S = 0.5
# Driver valve segments (fuel / ox); mix uses GUI driver_fill_time.
DRIVER_FUEL_OX_S = 2.0

# Mod1 port0 line map (0-based): 0=S2 driver fuel mix, 1=S1 driver fuel, 2=S3 driver ox,
# 3=S5 reactant mix, 4=S4 driver ox mix, 5=S9 vacuum valve, 6=S6 purge (NO), 7=unused.
# Mod2 port0: 0=S7 exhaust (NO), 1=S8 gauge, 3=S10 vacuum pump; 6=timing out, 7=speaker (nicontrol).
#
# Fill / post-fill DAQ snapshots:
# - FILL_START: reactant mix on; purge line as during prior fill; gauge + exhaust on; vac valve closed, pump off.
# - POST_FILL_* / END_TEST: process valves closed; purge standby; gauge/exhaust per row.
# - purge_*: S6/S7 are NO — line False = path open. Purge opens S2+S4 mixes, S5 reactant, purge, exhaust.

D1_S2_FUEL_MIX = 0
D1_S1_FUEL_DRV = 1
D1_S3_OX_DRV = 2
D1_S5_REACT_MIX = 3
D1_S4_OX_MIX = 4
D1_S9_VAC_VALVE = 5
D1_S6_PURGE = 6

D2_S7_EXHAUST = 0
D2_S8_GAUGE = 1
D2_S10_VAC_PUMP = 3


def _pad8(x):
    return list((list(x) + [False] * 8)[:8])


FILL_START_DAQ1 = [False, False, False, True, False, False, True, False]
FILL_START_DAQ2 = [True, True, False, False, False, False, False, False]

POST_FILL_AFTER_REACTANT_ONLY_DAQ1 = [False, False, False, False, False, False, True, False]
POST_FILL_AFTER_REACTANT_ONLY_DAQ2 = [True, False, False, False, False, False, False, False]

POST_FILL_BEFORE_DRIVER_DAQ1 = [False, False, False, False, False, False, True, False]
POST_FILL_BEFORE_DRIVER_DAQ2 = [True, True, False, False, False, False, False, False]

END_TEST_DAQ1 = [False, False, False, False, False, False, True, False]
END_TEST_DAQ2 = [True, False, False, False, False, False, False, False]

# Purge: S2+S4 driver mixes + S5 reactant open (NC); S6 purge + S7 exhaust path open (NO → line False); S1/S3/S9 off; pump off.
purge_daq1 = [True, False, False, True, True, False, False, False]
purge_daq2 = [False, False, False, False, False, False, False, False]

PURGE_COMPLETE_DAQ1 = [False, False, False, True, False, False, True, False]
PURGE_COMPLETE_DAQ2 = [True, False, False, False, False, False, False, False]

# Begin vacuum: S1–S4 closed; S5 open; S6/S7 closed (NO valves); S8 open; S9 open; S10 on.
# Wire map matches SOLENOID_GUI_MAP / nicontrol Mod1–Mod2 line assignment.
BEGIN_VACUUM_DAQ1 = [True, False, False, True, True, True, True, False]
BEGIN_VACUUM_DAQ2 = [True, True, False, True, False, False, False, False]


def begin_vacuum_sequence():
    """S1–S4 closed; S5 open; S6/S7 closed; S8 open; S9 open; S10 on (vacuum valve + pump)."""
    d1 = list(BEGIN_VACUUM_DAQ1)
    d2 = list(BEGIN_VACUUM_DAQ2)
    nicontrol.set_digital_output(d1)
    nicontrol.set_digital_output_2(d2)
    return d1, d2


async def _pre_fill_vacuum_shutdown():
    """Close vacuum valve (S9), wait 1 s, then turn vacuum pump (S10) off."""
    d1, d2 = nicontrol.get_daq_states()
    d1 = _pad8(d1)
    d2 = _pad8(d2)
    d1[D1_S9_VAC_VALVE] = False
    nicontrol.set_digital_output(d1)
    nicontrol.set_digital_output_2(d2)
    await asyncio.sleep(1.0)
    d1, d2 = nicontrol.get_daq_states()
    d1 = _pad8(d1)
    d2 = _pad8(d2)
    d2[D2_S10_VAC_PUMP] = False
    nicontrol.set_digital_output(d1)
    nicontrol.set_digital_output_2(d2)


def _set_mfc_rates(setpoint_a, setpoint_b, setpoint_c, setpoint_d=0.0):
    nicontrol.set_mfc_setpoints_analog(setpoint_a, setpoint_b, setpoint_c, setpoint_d)


async def automatic_test(
    setpointA, setpointB, setpointC, setpointD, setpointC_driver,
    on_fill_complete=None,
    on_mfc_setpoints_changed=None,
    fill_time_s=0.0,  # GUI passes self.fill_time_s from fill_time box; default only if called without it
    testcount=None,
):
    _ = (setpointD, setpointC_driver)
    print("Test starting")

    try:
        threading.Thread(target=klinger_control.move_to_negative_29500, daemon=True).start()
    except Exception as e:
        print("Klinger automatic-test move to -29500 could not start:", e)



    fill_time = max(0.0, float(fill_time_s))
    buf = FILL_LOG_BUFFER_S
    total_duration = buf + fill_time + buf
    print(f"Using fill time input: {fill_time:.2f} s; MFC log {total_duration:.2f} s (incl. {buf:.1f} s buffers); "
          f"{FILL_LOG_SAMPLE_RATE_HZ:.0f} Hz")

    bnc_box_control.switch_preset(9) #ensures bnc box is in continuous mode 
    bnc_box_control.arm("ON") #ensures BNC box is running 

    await _pre_fill_vacuum_shutdown()

    acq_result = {}
    daq_thread = threading.Thread(
        target=nicontrol.fill_log_acquisition_thread_target,
        args=(acq_result, total_duration, FILL_LOG_SAMPLE_RATE_HZ),
        daemon=True,
    )
    daq_thread.start()

    await asyncio.sleep(buf)
    print("Vacuum down complete. Starting fill sequence...")

    nicontrol.set_digital_output(_pad8(FILL_START_DAQ1))
    nicontrol.set_digital_output_2(_pad8(FILL_START_DAQ2))
    _set_mfc_rates(setpointA, setpointB, setpointC, 0.0)
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(setpointA, setpointB, setpointC, 0.0)

    await asyncio.sleep(fill_time)

    nicontrol.set_digital_output(_pad8(POST_FILL_AFTER_REACTANT_ONLY_DAQ1))
    nicontrol.set_digital_output_2(_pad8(POST_FILL_AFTER_REACTANT_ONLY_DAQ2))
    _set_mfc_rates(0.0, 0.0, 0.0, 0.0)
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(0.0, 0.0, 0.0, 0.0)

    if on_fill_complete is not None:
        on_fill_complete()

    await asyncio.sleep(buf)

    daq_thread.join()

    acq = acq_result.get("acq") or {}
    segs = fill_log_csv.segments_for_automatic_test(buf, fill_time, total_duration, setpointA, setpointB, setpointC)
    rows = fill_log_csv.fill_log_rows_from_acquisition(acq, segs)
    fill_log_csv.write_fill_flow_rates_csv(testcount, rows)

    print("DAQ complete. Ignite when ready; use Purge when done.")


async def fill_and_driver_sequence(
    setpointA, setpointB, setpointC, setpointD, setpointC_driver,
    fill_time_s=0.0,  # GUI: fill_time box
    testcount=None,
    driver_fill_time_s=0.0,  # GUI: driver_fill_time box — mix segment duration only
    on_fill_complete=None,
    on_mfc_setpoints_changed=None,
):
    """Reactant fill, then driver solenoid sequence (no MFC flow): fuel 2 s, oxidizer 2 s,
    then S2+S4 driver mix lines together for driver_fill_time_s."""
    _ = (setpointD, setpointC_driver)
    driver_mix_time_s = float(driver_fill_time_s)

    await _pre_fill_vacuum_shutdown()

    print("Vacuum down complete")

    #threads the klinger motor to the negative 29500 position
    try:
        threading.Thread(target=klinger_control.move_to_negative_29500, daemon=True).start()
    except Exception as e:
        print("Klinger move to -29500 could not start:", e)

    bnc_box_control.switch_preset(9) #ensures bnc box is in continuous mode 
    bnc_box_control.arm("ON") #ensures BNC box is running 

    #sets the fill time and buffer time then prints the total duration and sample rate
    fill_time = max(0.0, float(fill_time_s))
    buf = FILL_LOG_BUFFER_S
    experiment_core = fill_time + 2.0 * DRIVER_FUEL_OX_S + driver_mix_time_s
    total_duration = buf + experiment_core + buf
    print(
        f"Using fill time input: {fill_time:.2f} s; driver mix segment: {driver_mix_time_s:.2f} s; "
        f"MFC log {total_duration:.2f} s (incl. {buf:.1f} s buffers); {FILL_LOG_SAMPLE_RATE_HZ:.0f} Hz"
    )

    #starts the fill logging data acquisition thread
    acq_result = {}
    daq_thread = threading.Thread(
        target=nicontrol.fill_log_acquisition_thread_target,
        args=(acq_result, total_duration, FILL_LOG_SAMPLE_RATE_HZ),
        daemon=True,
    )
    daq_thread.start()

    await asyncio.sleep(buf)
    print("Fill + driver sequence starting (reactant fill, then driver valves).")

    #reactant fill start
    nicontrol.set_digital_output(_pad8(FILL_START_DAQ1))
    nicontrol.set_digital_output_2(_pad8(FILL_START_DAQ2))
    _set_mfc_rates(setpointA, setpointB, setpointC, 0.0)
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(setpointA, setpointB, setpointC, 0.0)

    await asyncio.sleep(fill_time)

    #driver fill start
    nicontrol.set_digital_output(_pad8(POST_FILL_BEFORE_DRIVER_DAQ1))
    nicontrol.set_digital_output_2(_pad8(POST_FILL_BEFORE_DRIVER_DAQ2))
    _set_mfc_rates(0.0, 0.0, 0.0, 0.0)
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(0.0, 0.0, 0.0, 0.0)

    if on_fill_complete is not None:
        on_fill_complete()

    d1, d2 = nicontrol.get_daq_states()
    d1 = _pad8(d1)
    d2 = _pad8(d2)

    #driver fuel fill
    d1[D1_S1_FUEL_DRV] = True
    nicontrol.set_digital_output(d1)
    nicontrol.set_digital_output_2(d2)
    await asyncio.sleep(DRIVER_FUEL_OX_S)

    d1[D1_S1_FUEL_DRV] = False
    nicontrol.set_digital_output(d1)

    #driver ox fill
    d1[D1_S3_OX_DRV] = True
    nicontrol.set_digital_output(d1)
    await asyncio.sleep(DRIVER_FUEL_OX_S)

    d1[D1_S3_OX_DRV] = False
    nicontrol.set_digital_output(d1)

    #driver mix fill
    d1[D1_S2_FUEL_MIX] = True
    d1[D1_S4_OX_MIX] = True
    nicontrol.set_digital_output(d1)
    await asyncio.sleep(driver_mix_time_s)
    d1[D1_S2_FUEL_MIX] = False
    d1[D1_S4_OX_MIX] = False
    nicontrol.set_digital_output(d1)

    nicontrol.set_digital_output(_pad8(END_TEST_DAQ1))
    nicontrol.set_digital_output_2(_pad8(END_TEST_DAQ2))
    _set_mfc_rates(0.0, 0.0, 0.0, 0.0)
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(0.0, 0.0, 0.0, 0.0)

    await asyncio.sleep(buf)

    daq_thread.join() #joins the daq thread to the main thread
 
    #gets the acquisition result and segments the fill and driver sequence
    acq = acq_result.get("acq") or {}
    segs = fill_log_csv.segments_for_fill_and_driver(
        buf,
        fill_time,
        DRIVER_FUEL_OX_S,
        driver_mix_time_s,
        total_duration,
        setpointA,
        setpointB,
        setpointC,
    )
    rows = fill_log_csv.fill_log_rows_from_acquisition(acq, segs) #gets the rows from the acquisition result and segments the fill and driver sequence
    fill_log_csv.write_fill_flow_rates_csv(testcount, rows) #writes the rows to a csv file

    print("Reactant fill and driver valve sequence complete. Ignite when ready; use Purge when done.")


async def purge(setpointA, setpointB, setpointC, setpointD, on_mfc_setpoints_changed=None):
    _ = (setpointA, setpointB, setpointC, setpointD)
    _set_mfc_rates(0.0, 0.0, 0.0, 0.0)
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(0.0, 0.0, 0.0, 0.0)

    nicontrol.set_digital_output(_pad8(purge_daq1))
    nicontrol.set_digital_output_2(_pad8(purge_daq2))

    print("Purging...")
    await asyncio.sleep(60)

    nicontrol.set_digital_output(_pad8(PURGE_COMPLETE_DAQ1))
    nicontrol.set_digital_output_2(_pad8(PURGE_COMPLETE_DAQ2))

    print("Purge complete!")
