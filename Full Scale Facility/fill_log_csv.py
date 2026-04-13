"""Fill-flow CSV: segment tagging and writing `fill_flow_rates_test*.csv`."""

import csv
import os

FILL_LOG_DIR = r"C:\Users\dedic-lab\Documents\Detonation_Facility_Testing"

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

#defines the segments for the automatic test
def segments_for_automatic_test(buffer_s, fill_time, total_duration, setpoint_a, setpoint_b, setpoint_c):
    """Timeline segments matching `automatic_test` (pre-buffer → optional reactant → post-buffer)."""
    segs = [(0.0, buffer_s, "buffer", "buffer_start", 0.0, 0.0, 0.0, 0.0)]
    t = buffer_s
    if fill_time > 0:
        segs.append(
            (t, t + fill_time, "reactant_fill", "reactant_fill_start", setpoint_a, setpoint_b, setpoint_c, 0.0)
        )
        t += fill_time
    segs.append((t, total_duration, "post_buffer", "post_buffer_start", 0.0, 0.0, 0.0, 0.0))
    return segs

#segments for the fill and driver sequence
def segments_for_fill_and_driver(
    buffer_s,
    fill_time,
    driver_fuel_ox_s,
    driver_mix_time_s,
    total_duration,
    setpoint_a,
    setpoint_b,
    setpoint_c,
):
    """Timeline segments matching `fill_and_driver_sequence`."""
    segs = [(0.0, buffer_s, "buffer", "buffer_start", 0.0, 0.0, 0.0, 0.0)]
    t = buffer_s
    if fill_time > 0:
        segs.append(
            (t, t + fill_time, "reactant_fill", "reactant_fill_start", setpoint_a, setpoint_b, setpoint_c, 0.0)
        )
        t += fill_time
    segs.append((t, t + driver_fuel_ox_s, "driver_fuel", "driver_fuel_start", 0.0, 0.0, 0.0, 0.0))
    t += driver_fuel_ox_s
    segs.append((t, t + driver_fuel_ox_s, "driver_ox", "driver_ox_start", 0.0, 0.0, 0.0, 0.0))
    t += driver_fuel_ox_s
    segs.append((t, t + driver_mix_time_s, "driver_mix", "driver_mix_start", 0.0, 0.0, 0.0, 0.0))
    t += driver_mix_time_s
    segs.append((t, total_duration, "post_buffer", "post_buffer_start", 0.0, 0.0, 0.0, 0.0))
    return segs

#helper function to get the segment at a given time for fill_log_rows_from_acquisition
def segment_at_time(ti, segments):
    """Return segment tuple (t0, t1, phase, event_label, sp_a..d) for time ti (seconds from acq start)."""
    for seg in segments:
        t0, t1 = seg[0], seg[1]
        if t0 <= ti < t1:
            return seg
    if segments:
        last = segments[-1]
        if last[0] <= ti <= last[1] + 1e-9:
            return last
    return segments[-1]

#helper function to get the rows from the acquisition result and segments the fill and driver sequence
def fill_log_rows_from_acquisition(acq, segments, time_offset_s=0.0):
    """
    One continuous acquire_fill_mfc_log: assign phase / event from segment table.
    segments: list of (t0, t1, phase, event_label_on_entry, sp_a, sp_b, sp_c, sp_d).
    Intervals are half-open [t0, t1) except the last may close at acq end.
    """
    rows = []
    t = acq["time_s"]
    n = len(t)
    if n == 0:
        return rows
    p = acq["pressure_kpa"]
    fa, fb, fc, fd = acq["flow_a"], acq["flow_b"], acq["flow_c"], acq["flow_d"]
    prev_phase = None
    
    #iterates through the acquisition result and segments the fill and driver sequence
    for i in range(n):
        ti = float(t[i]) + time_offset_s
        t_rel = float(t[i]) #relative time from the acquisition start
        seg = segment_at_time(t_rel, segments) #gets the segment at the relative time
        phase = seg[2] #gets the phase from the segment
        ev_label = seg[3] #gets the event label from the segment
        sp_a, sp_b, sp_c, sp_d = seg[4], seg[5], seg[6], seg[7] #gets the setpoints from the segment
        ev = ev_label if phase != prev_phase else "" #gets the event from the segment
        prev_phase = phase #sets the previous phase to the current phase
        rows.append( #appends the row to the rows list
            [
                ti,
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

#helper function to write the rows to a csv file
def write_fill_flow_rates_csv(testcount, rows):
    if testcount is None or len(rows) == 0:
        return
    os.makedirs(FILL_LOG_DIR, exist_ok=True)
    path = os.path.join(FILL_LOG_DIR, f"fill_flow_rates_test{testcount}.csv")
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(CSV_HEADER)
        w.writerows(rows)
