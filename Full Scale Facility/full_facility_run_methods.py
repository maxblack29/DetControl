import csv
import os
import nicontrol
import asyncio
import threading

import klinger_control


FILL_LOG_DIR = r"C:\Users\dedic-lab\Documents\Detonation_Facility_Testing"
# Hardware sample clock for fill CSV (Hz). Row spacing = 1 / FILL_LOG_SAMPLE_RATE_HZ.
FILL_LOG_SAMPLE_RATE_HZ = 1000.0
# Driver valve segments (fuel / ox); mix uses GUI driver_fill_time.
DRIVER_FUEL_OX_S = 2.0

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


def _csv_rows_from_acquisition(
    acq,
    time_offset_s,
    phase,
    event_first_row,
    sp_a,
    sp_b,
    sp_c,
    sp_d,
):
    """Build CSV rows from nicontrol.acquire_fill_mfc_log() result."""
    rows = []
    t = acq["time_s"]
    n = len(t)
    if n == 0:
        return rows
    p = acq["pressure_kpa"]
    fa, fb, fc, fd = acq["flow_a"], acq["flow_b"], acq["flow_c"], acq["flow_d"]
    for i in range(n):
        ev = event_first_row if i == 0 else ""
        rows.append(
            [
                float(t[i]) + time_offset_s,
                phase,
                ev,
                float(p[i]),
                sp_a,
                float(fa[i]),
                sp_b,
                float(fb[i]),
                sp_c,
                float(fc[i]),
                sp_d,
                float(fd[i]),
            ]
        )
    return rows


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
    print(f"Using fill time input: {fill_time:.2f} s; MFC log rate {FILL_LOG_SAMPLE_RATE_HZ:.0f} Hz")
    print("Vacuum down complete. Starting fill sequence...")

    nicontrol.set_digital_output(_pad8(FILL_START_DAQ1))
    nicontrol.set_digital_output_2(_pad8(FILL_START_DAQ2))
    _set_mfc_rates(setpointA, setpointB, setpointC, 0.0)
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(setpointA, setpointB, setpointC, 0.0)

    fill_rows = []
    t_off = 0.0
    if fill_time > 0:
        acq = await asyncio.to_thread(
            nicontrol.acquire_fill_mfc_log,
            fill_time,
            FILL_LOG_SAMPLE_RATE_HZ,
        )
        fill_rows.extend(
            _csv_rows_from_acquisition(
                acq,
                t_off,
                "reactant_fill",
                "",
                setpointA,
                setpointB,
                setpointC,
                0.0,
            )
        )

    if testcount is not None and len(fill_rows) > 0:
        os.makedirs(FILL_LOG_DIR, exist_ok=True)
        path = os.path.join(FILL_LOG_DIR, f"fill_flow_rates_test{testcount}.csv")
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(CSV_HEADER)
            w.writerows(fill_rows)

    if on_fill_complete is not None:
        on_fill_complete()

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
    driver_fill_time_s=0.0,  # GUI: driver_fill_time box — mix segment duration only
    on_fill_complete=None,
    on_mfc_setpoints_changed=None,
):
    """Reactant fill, then driver solenoid sequence (no MFC flow): fuel 2 s, oxidizer 2 s, mix for driver_fill_time_s."""
    _ = (setpointD, setpointC_driver)
    driver_mix_time_s = max(0.0, float(driver_fill_time_s))

    print("Vacuum down complete. Starting fill sequence...")
    print("Fill + driver sequence starting (reactant fill, then driver valves).")

    try:
        threading.Thread(target=klinger_control.move_to_negative_29500, daemon=True).start()
    except Exception as e:
        print("Klinger move to -29500 could not start:", e)

    fill_time = max(0.0, float(fill_time_s))
    print(
        f"Using fill time input: {fill_time:.2f} s; driver mix segment: {driver_mix_time_s:.2f} s; "
        f"MFC log rate {FILL_LOG_SAMPLE_RATE_HZ:.0f} Hz"
    )

    nicontrol.set_digital_output(_pad8(FILL_START_DAQ1))
    nicontrol.set_digital_output_2(_pad8(FILL_START_DAQ2))
    _set_mfc_rates(setpointA, setpointB, setpointC, 0.0)
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(setpointA, setpointB, setpointC, 0.0)

    fill_rows = []
    t_off = 0.0

    if fill_time > 0:
        acq = await asyncio.to_thread(
            nicontrol.acquire_fill_mfc_log,
            fill_time,
            FILL_LOG_SAMPLE_RATE_HZ,
        )
        fill_rows.extend(
            _csv_rows_from_acquisition(
                acq,
                t_off,
                "reactant_fill",
                "",
                setpointA,
                setpointB,
                setpointC,
                0.0,
            )
        )
        t_off += acq["duration_s"]

    if on_fill_complete is not None:
        on_fill_complete()

    nicontrol.set_digital_output(_pad8(POST_FILL_BEFORE_DRIVER_DAQ1))
    nicontrol.set_digital_output_2(_pad8(POST_FILL_BEFORE_DRIVER_DAQ2))
    _set_mfc_rates(0.0, 0.0, 0.0, 0.0)
    if on_mfc_setpoints_changed is not None:
        on_mfc_setpoints_changed(0.0, 0.0, 0.0, 0.0)

    d1, d2 = nicontrol.get_daq_states()
    d1 = _pad8(d1)
    d2 = _pad8(d2)
    first_driver_segment = True

    d1[1] = True
    nicontrol.set_digital_output(d1)
    nicontrol.set_digital_output_2(d2)
    acq = await asyncio.to_thread(
        nicontrol.acquire_fill_mfc_log,
        DRIVER_FUEL_OX_S,
        FILL_LOG_SAMPLE_RATE_HZ,
    )
    fill_rows.extend(
        _csv_rows_from_acquisition(
            acq,
            t_off,
            "driver",
            "driver_start" if first_driver_segment else "",
            0.0,
            0.0,
            0.0,
            0.0,
        )
    )
    first_driver_segment = False
    t_off += acq["duration_s"]
    d1[1] = False
    nicontrol.set_digital_output(d1)

    d1[2] = True
    nicontrol.set_digital_output(d1)
    acq = await asyncio.to_thread(
        nicontrol.acquire_fill_mfc_log,
        DRIVER_FUEL_OX_S,
        FILL_LOG_SAMPLE_RATE_HZ,
    )
    fill_rows.extend(
        _csv_rows_from_acquisition(
            acq,
            t_off,
            "driver",
            "",
            0.0,
            0.0,
            0.0,
            0.0,
        )
    )
    t_off += acq["duration_s"]
    d1[2] = False
    nicontrol.set_digital_output(d1)

    d1[0] = True
    nicontrol.set_digital_output(d1)
    if driver_mix_time_s > 0:
        acq = await asyncio.to_thread(
            nicontrol.acquire_fill_mfc_log,
            driver_mix_time_s,
            FILL_LOG_SAMPLE_RATE_HZ,
        )
        fill_rows.extend(
            _csv_rows_from_acquisition(
                acq,
                t_off,
                "driver",
                "",
                0.0,
                0.0,
                0.0,
                0.0,
            )
        )
        t_off += acq["duration_s"]
    d1[0] = False
    nicontrol.set_digital_output(d1)

    if testcount is not None and len(fill_rows) > 0:
        os.makedirs(FILL_LOG_DIR, exist_ok=True)
        path = os.path.join(FILL_LOG_DIR, f"fill_flow_rates_test{testcount}.csv")
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(CSV_HEADER)
            w.writerows(fill_rows)

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
