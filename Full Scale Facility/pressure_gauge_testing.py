"""
Standalone script to test the post-fill (low) and vacuum pressure gauges.
Reads both at 1–2 Hz until the user presses Enter. Saves results to a CSV.
Run from the 'Full Scale Facility' directory so 'nicontrol' is importable.
"""
import csv
import time
import threading
from datetime import datetime

import nicontrol


READING_INTERVAL_S = 0.5   # 1 reading every 0.5 s → 2 Hz (use 1.0 for 1 Hz)


def wait_for_stop(stop_event):
    input()
    stop_event.set()


def main():
    print("Pressure gauge test (post-fill + vacuum)")
    print("Readings at ~{} Hz. Press Enter to stop.".format(1.0 / READING_INTERVAL_S))
    input("Press Enter to start the test... ")

    stop_event = threading.Event()
    thread = threading.Thread(target=wait_for_stop, args=(stop_event,), daemon=True)
    thread.start()

    start_time = time.perf_counter()
    start_iso = datetime.now().isoformat(timespec="seconds")
    rows = []

    print("Testing... (press Enter to stop)")
    try:
        while not stop_event.is_set():
            t_elapsed = time.perf_counter() - start_time
            post_fill_kPa = nicontrol.read_pressure()
            vacuum_kPa = nicontrol.read_vacuum_pressure()
            timestamp = datetime.now().isoformat(timespec="milliseconds")
            rows.append((timestamp, t_elapsed, post_fill_kPa, vacuum_kPa))
            print("  {:.1f}s  post_fill={:.2f} kPa  vacuum={:.2f} kPa".format(
                t_elapsed, post_fill_kPa, vacuum_kPa))
            stop_event.wait(READING_INTERVAL_S)
    except KeyboardInterrupt:
        print("\nStopped by Ctrl+C.")

    if not rows:
        print("No data recorded.")
        return

    filename = "pressure_gauge_test_{}.csv".format(
        datetime.now().strftime("%Y%m%d_%H%M%S"))
    with open(filename, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["timestamp_iso", "elapsed_s", "post_fill_pressure_kPa", "vacuum_pressure_kPa"])
        w.writerows(rows)

    print("Test ended. Data saved to {} ({} readings).".format(filename, len(rows)))


if __name__ == "__main__":
    main()
