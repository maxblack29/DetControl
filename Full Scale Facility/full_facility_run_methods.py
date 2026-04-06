import csv
import os
import nicontrol
import asyncio
import threading
import time

import klinger_control

FILL_LOG_DIR = r"C:\Users\dedic-lab\Documents\Detonation_Facility_Testing"
FILL_LOG_INTERVAL_S = 0.1

# Mod1: S1–S4 on 0–3, S5 purge (NO) on 6. Mod2: S6 on 0, S7 gauge on 1; timing 6, speaker 7.
#
# Fill / post-fill DAQ snapshots (see nicontrol line indices):
# - FILL_START: reactant path to facility open; gauge line on; MFCs commanded during loop below.
# - POST_FILL_AFTER_REACTANT_ONLY: end state for Begin Testing (reactant fill only): isolate fill, safe idle before ignite/purge.
# - POST_FILL_BEFORE_DRIVER: after reactant fill, before driver solenoids: keeps facility isolated while switching to driver path.
# - END_TEST: after driver sequence (driver button): driver lines closed, same “safe end” posture as other flows need.


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

purge_daq1 = [True, False, False, True, False, False, False, False]
purge_daq2 = [False] * 8

PURGE_COMPLETE_DAQ1 = [False, False, False, True, False, False, True, False]
PURGE_COMPLETE_DAQ2 = [True, True, False, False, False, False, False, False]

CSV_HEADER = (
    "time_s",
    "phase",
    "event",
    "pressure_kPa",
    "setpoint_A_SLPM",
    "flow_A_SLPM",
    "setpoint_B_SLPM",
    "flow_B_SLPM",
    "setpoint_C_SLPM",
    "flow_C_SLPM",
    "setpoint_D_SLPM",
    "flow_D_SLPM",
)


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
    print(f"Using fill time input: {fill_time:.2f} s")
    print("Vacuum down complete. Starting fill sequence...")

    # Phase: open reactant routing, enable gauge; MFC setpoints apply for the timed fill below.
    nicontrol.set_digital_output(_pad8(FILL_START_DAQ1))
    nicontrol.set_digital_output_2(_pad8(FILL_START_DAQ2))
    _set_mfc_rates(setpointA, setpointB, setpointC, 0.0)
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(setpointA, setpointB, setpointC, 0.0)

    # Phase: reactant_fill — hold for fill_time_s; log pressure/MFC feedback; speaker at ~half fill (timing cue).
    fill_rows = []
    start_fill = time.perf_counter()
    speaker_done = False
    while True:
        elapsed = time.perf_counter() - start_fill
        p = nicontrol.read_pressure()
        fa, fb, fc, fd = nicontrol.read_mfc_flows_analog_once()
        fill_rows.append(
            [elapsed, "reactant_fill", "", p, setpointA, fa, setpointB, fb, setpointC, fc, 0.0, fd]
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
            w.writerow(CSV_HEADER)
            w.writerows(fill_rows)

    if on_fill_complete is not None:
        on_fill_complete()

    # Phase: post fill — zero MFCs, close reactant feed, safe idle (operator may ignite / later purge).
    nicontrol.set_digital_output(_pad8(POST_FILL_AFTER_REACTANT_ONLY_DAQ1))
    nicontrol.set_digital_output_2(_pad8(POST_FILL_AFTER_REACTANT_ONLY_DAQ2))
    _set_mfc_rates(0.0, 0.0, 0.0, 0.0)
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(0.0, 0.0, 0.0, 0.0)

    print("Reactant fill complete. Ignite when ready; use Purge when done.")


async def fill_and_driver_sequence(
    setpointA, setpointB, setpointC, setpointD, setpointC_driver,
    fill_time_s=0.0,  # GUI: fill_time box
    testcount=None,
    driver_fill_time_s=0.0,  # GUI: driver_fill_time box — duration of the driver *mix* segment only (fuel/ox are fixed 2 s each)
    on_fill_complete=None,
    on_mfc_setpoints_changed=None,
):
    """Reactant fill (same as Begin Testing), then driver solenoid sequence (no MFC flow): fuel 2 s, oxidizer 2 s, mix for driver_fill_time_s."""
    _ = (setpointD, setpointC_driver)
    driver_mix_time_s = max(0.0, float(driver_fill_time_s))

    print("Fill + driver sequence starting (reactant fill, then driver valves).")
    try:
        threading.Thread(target=klinger_control.move_to_negative_29500, daemon=True).start()
    except Exception as e:
        print("Klinger move to -29500 could not start:", e)

    fill_time = max(0.0, float(fill_time_s))
    print(f"Using fill time input: {fill_time:.2f} s; driver mix segment: {driver_mix_time_s:.2f} s")

    # Phase: open reactant routing (same as automatic_test).
    nicontrol.set_digital_output(_pad8(FILL_START_DAQ1))
    nicontrol.set_digital_output_2(_pad8(FILL_START_DAQ2))
    _set_mfc_rates(setpointA, setpointB, setpointC, 0.0)
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(setpointA, setpointB, setpointC, 0.0)

    # Phase: reactant_fill — timed hold; speaker at ~half fill; then we always run the driver valve train.
    fill_rows = []
    start_fill = time.perf_counter()
    speaker_done = False
    while True:
        elapsed = time.perf_counter() - start_fill
        p = nicontrol.read_pressure()
        fa, fb, fc, fd = nicontrol.read_mfc_flows_analog_once()
        fill_rows.append(
            [elapsed, "reactant_fill", "", p, setpointA, fa, setpointB, fb, setpointC, fc, 0.0, fd]
        )
        if (not speaker_done) and elapsed >= (fill_time / 2.0):
            nicontrol.set_daq2_line(nicontrol.DAQ2_LINE_SPEAKER, True)
            speaker_done = True
        if elapsed >= fill_time:
            break
        await asyncio.sleep(min(FILL_LOG_INTERVAL_S, max(0.0, fill_time - elapsed)))

    # Reactant fill finished — callback before any driver motion (pressure sample / UI).
    if on_fill_complete is not None:
        on_fill_complete()

    # Phase: isolate after fill, prep for driver path (do not print “ignite” until driver is done).
    nicontrol.set_digital_output(_pad8(POST_FILL_BEFORE_DRIVER_DAQ1))
    nicontrol.set_digital_output_2(_pad8(POST_FILL_BEFORE_DRIVER_DAQ2))
    _set_mfc_rates(0.0, 0.0, 0.0, 0.0)
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(0.0, 0.0, 0.0, 0.0)

    # Phase: driver — valve-only timing: Mod1 index 1 = fuel driver, 2 = ox driver, 0 = mix; no MFC setpoints.
    d1, d2 = nicontrol.get_daq_states()
    d1 = _pad8(d1)
    d2 = _pad8(d2)
    first_driver = True

    d1[1] = True
    nicontrol.set_digital_output(d1)
    nicontrol.set_digital_output_2(d2)
    t_end = time.perf_counter() + 2.0
    while time.perf_counter() < t_end:
        elapsed = time.perf_counter() - start_fill
        p = nicontrol.read_pressure()
        fa, fb, fc, fd = nicontrol.read_mfc_flows_analog_once()
        ev = "driver_start" if first_driver else ""
        first_driver = False
        fill_rows.append([elapsed, "driver", ev, p, 0.0, fa, 0.0, fb, 0.0, fc, 0.0, fd])
        rem = t_end - time.perf_counter()
        if rem <= 0:
            break
        await asyncio.sleep(min(FILL_LOG_INTERVAL_S, rem))
    d1[1] = False
    nicontrol.set_digital_output(d1)

    d1[2] = True
    nicontrol.set_digital_output(d1)
    t_end = time.perf_counter() + 2.0
    while time.perf_counter() < t_end:
        elapsed = time.perf_counter() - start_fill
        p = nicontrol.read_pressure()
        fa, fb, fc, fd = nicontrol.read_mfc_flows_analog_once()
        fill_rows.append([elapsed, "driver", "", p, 0.0, fa, 0.0, fb, 0.0, fc, 0.0, fd])
        rem = t_end - time.perf_counter()
        if rem <= 0:
            break
        await asyncio.sleep(min(FILL_LOG_INTERVAL_S, rem))
    d1[2] = False
    nicontrol.set_digital_output(d1)

    d1[0] = True
    nicontrol.set_digital_output(d1)
    t_end = time.perf_counter() + driver_mix_time_s
    while time.perf_counter() < t_end:
        elapsed = time.perf_counter() - start_fill
        p = nicontrol.read_pressure()
        fa, fb, fc, fd = nicontrol.read_mfc_flows_analog_once()
        fill_rows.append([elapsed, "driver", "", p, 0.0, fa, 0.0, fb, 0.0, fc, 0.0, fd])
        rem = t_end - time.perf_counter()
        if rem <= 0:
            break
        await asyncio.sleep(min(FILL_LOG_INTERVAL_S, rem))
    d1[0] = False
    nicontrol.set_digital_output(d1)

    if testcount is not None and len(fill_rows) > 0:
        os.makedirs(FILL_LOG_DIR, exist_ok=True)
        path = os.path.join(FILL_LOG_DIR, f"fill_flow_rates_test{testcount}.csv")
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(CSV_HEADER)
            w.writerows(fill_rows)

    # Phase: end — driver lines safe; same end posture as other tests for ignite / purge.
    nicontrol.set_digital_output(_pad8(END_TEST_DAQ1))
    nicontrol.set_digital_output_2(_pad8(END_TEST_DAQ2))
    _set_mfc_rates(0.0, 0.0, 0.0, 0.0)
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(0.0, 0.0, 0.0, 0.0)

    print("Reactant fill and driver valve sequence complete. Ignite when ready; use Purge when done.")


async def purge(setpointA, setpointB, setpointC, setpointD, on_mfc_setpoints_changed=None):
    _ = (setpointA, setpointB, setpointC, setpointD)
    _set_mfc_rates(0.0, 0.0, 0.0, 0.0)
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(0.0, 0.0, 0.0, 0.0)

    nicontrol.set_digital_output(purge_daq1)
    nicontrol.set_digital_output_2(purge_daq2)

    print("Purging...")
    await asyncio.sleep(60)

    nicontrol.set_digital_output(_pad8(PURGE_COMPLETE_DAQ1))
    nicontrol.set_digital_output_2(_pad8(PURGE_COMPLETE_DAQ2))

    print("Purge complete!")
