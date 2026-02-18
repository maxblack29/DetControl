import nidaqmx
from nidaqmx.constants import LineGrouping, AcquisitionType, LoggingMode, LoggingOperation, READ_ALL_AVAILABLE
from random import sample
import numpy as np
import time
from datetime import datetime
import csv


#port = 'port0'


def set_digital_output(states): #for Mod1
    device_name = "cDAQ9188-169338EMod1/port0/line0:7"
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(device_name, line_grouping=LineGrouping.CHAN_PER_LINE)
        task.write(states)

def set_digital_output_2(states): #for Mod2
    device_name = "cDAQ9188-169338EMod2/port0/line0:7"
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(device_name, line_grouping=LineGrouping.CHAN_PER_LINE)
        task.write(states)


#had to write separate function because this one is on Mod2
def set_ignite_read_pressure(testcount, vacuum_pressure, fill_pressure):
    ignite_port = "cDAQ9188-169338EMod2/port6/line0:7"
    ai_channels = "cDAQ9188-169338EMod6/ai0:ai3"
    on_states = [True, False, True, False, False, False, True, False]  # ignite is on port 6
    off_states = [True, False, True, False, False, False, False, False]  # Daq2 states post fill

    # Send signal to ignite
    with nidaqmx.Task() as do_task:
        do_task.do_channels.add_do_chan(ignite_port, line_grouping=LineGrouping.CHAN_PER_LINE)
        do_task.write(on_states)
        time.sleep(0.1)
        do_task.write(off_states)

    # Read pressure transducers (ai0->PT1, ai1->PT2, ai2->PT3, ai3->PT4) over 10 ms
    sample_rate_Hz = 1_000_000  # 1 MS/s
    duration_s = 0.01          # 10 ms
    samples = int(sample_rate_Hz * duration_s)

    with nidaqmx.Task() as ai_task:
        ai_task.ai_channels.add_ai_voltage_chan(ai_channels, min_val=-10, max_val=10)
        ai_task.timing.cfg_samp_clk_timing(
            sample_rate_Hz,
            sample_mode=AcquisitionType.FINITE,
            samps_per_chan=samples
        )
        data = ai_task.read(number_of_samples_per_channel=samples)

    # nidaqmx multi-channel read: shape (samples_per_channel, num_channels)
    data = np.asarray(data, dtype=np.float64)
    if data.ndim == 1:
        data = np.atleast_2d(data).T
    
    n_samples, n_ch = data.shape[0], data.shape[1]
    pt1 = data[:, 0] if n_ch >= 1 else np.zeros(n_samples)
    pt2 = data[:, 1] if n_ch >= 2 else np.zeros(n_samples)
    pt3 = data[:, 2] if n_ch >= 3 else np.zeros(n_samples)
    pt4 = data[:, 3] if n_ch >= 4 else np.zeros(n_samples)

    # One CSV per test: properties in header, then time and PT1–PT4 columns
    filename = f"TestData{testcount}.csv"
    time_s = np.arange(n_samples, dtype=np.float64) / sample_rate_Hz

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        # File properties (same as former TDMS root properties)
        writer.writerow(["TestNumber", testcount])
        writer.writerow(["VacuumPressure_Pa", float(vacuum_pressure)])
        writer.writerow(["PostFillPressure_Pa", float(fill_pressure)])
        writer.writerow(["DateTime", datetime.now().isoformat()])
        writer.writerow(["SampleRate_Hz", sample_rate_Hz])
        writer.writerow([])  # blank line before data
        writer.writerow(["time_s", "PT1", "PT2", "PT3", "PT4"])
        for i in range(n_samples):
            writer.writerow([time_s[i], pt1[i], pt2[i], pt3[i], pt4[i]])


def read_pressure():
    ai_channel = "cDAQ9188-169338EMod3/ai0"
    sample_rate = 1000  # 1 kHz 
    duration = 0.1      # 100 ms
    samples = int(sample_rate * duration)

    with nidaqmx.Task() as ai_task:
        ai_task.ai_channels.add_ai_voltage_chan(ai_channel, min_val=0, max_val=10)
        ai_task.timing.cfg_samp_clk_timing(
            sample_rate, 
            sample_mode=AcquisitionType.FINITE, 
            samps_per_chan=samples
        )
        data = ai_task.read(number_of_samples_per_channel=samples)
        avg = np.mean(data)

    return avg * 103.421 / 10 # Convert voltage to kPa based on sensor specs

def read_vacuum_pressure():
    ai_channel = "cDAQ9188-169338EMod3/ai1"
    sample_rate = 1000  # 1 kHz 
    duration = 0.1      # 100 ms
    samples = int(sample_rate * duration)

    with nidaqmx.Task() as ai_task:
        ai_task.ai_channels.add_ai_voltage_chan(ai_channel, min_val=0, max_val=10)
        ai_task.timing.cfg_samp_clk_timing(
            sample_rate, 
            sample_mode=AcquisitionType.FINITE, 
            samps_per_chan=samples
        )
        data = ai_task.read(number_of_samples_per_channel=samples)
        avg = np.mean(data)

    return avg * 103.421 / 10 # Convert voltage to kPa based on sensor specs