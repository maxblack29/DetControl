import nidaqmx
from nidaqmx.constants import LineGrouping, AcquisitionType, LoggingMode, LoggingOperation, READ_ALL_AVAILABLE, Edge
from random import sample
import numpy as np
import time
from datetime import datetime
import csv
import nidaqmx.system

system = nidaqmx.system.System.local()


# Track last DAQ output states so the GUI can show current solenoid status.
_daq1_state = [False] * 8
_daq2_state = [False] * 8


def set_digital_output(states):  # for Mod1
    global _daq1_state
    device_name = "cDAQ9188-169338EMod1/port0/line0:7"
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(device_name, line_grouping=LineGrouping.CHAN_PER_LINE)
        task.write(states)
    _daq1_state = list(states)


def set_digital_output_2(states):  # for Mod2
    global _daq2_state
    device_name = "cDAQ9188-169338EMod2/port0/line0:7"
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(device_name, line_grouping=LineGrouping.CHAN_PER_LINE)
        task.write(states)
    _daq2_state = list(states)


def get_daq_states():
    """Return the last written DAQ1 and DAQ2 digital output states."""
    return _daq1_state[:], _daq2_state[:]


#had to write separate function because this one is on Mod2
def set_ignite_read_pressure(testcount, vacuum_pressure, fill_pressure):
    ignite_port = "cDAQ9188-169338EMod2/port0/line0:7"
    on_states = [True, False, True, False, False, False, True, False]  # ignite is on port 6
    off_states = [True, False, True, False, False, False, False, False]  # Daq2 states post fill



    # Send signal to ignite
    with nidaqmx.Task() as do_task:
        do_task.do_channels.add_do_chan(ignite_port, line_grouping=LineGrouping.CHAN_PER_LINE)
        do_task.write(on_states)
        time.sleep(0.010) #half a ms pulse 
        do_task.write(off_states)
    print("timing box signal sent")

         # Read 8 pressure transducers over 10 ms (Mod5 PT1–PT4, Mod6 PT5–PT8) in one synchronized task
    sample_rate_Hz = 1_000_000  # 1 MS/s
    duration_s = 0.1          # 10 ms
    samples = int(sample_rate_Hz * duration_s)
    mod5_channels = "cDAQ9188-169338EMod5/ai0:3"   # PT1, PT2, PT3, PT4
    mod6_channels = "cDAQ9188-169338EMod6/ai0:3"   # PT5, PT6, PT7, PT8

    # with nidaqmx.Task() as ai_task:
    #     ai_task.ai_channels.add_ai_voltage_chan(mod5_channels, min_val=-10, max_val=10)
    #     ai_task.ai_channels.add_ai_voltage_chan(mod6_channels, min_val=-10, max_val=10)
    #     ai_task.timing.cfg_samp_clk_timing(
    #         sample_rate_Hz,
    #         sample_mode=AcquisitionType.FINITE,
    #         samps_per_chan=samples
    #     )
    #     data = ai_task.read(number_of_samples_per_channel=samples)

    # # nidaqmx multi-channel read: shape (n_channels, samples_per_channel) -> PT1..PT8
    # data = np.asarray(data, dtype=np.float64)
    


    for dev in system.devices:

        if "9188" in dev.product_type:

            print(f"Chassis Name: {dev.name}")

            # Look specifically for PFI terminals

            pfi_terms = [t for t in dev.terminals if "PFI" in t]

            print(f"Available PFI terminals: {pfi_terms}")

    with nidaqmx.Task() as ai_task:
        ai_task.ai_channels.add_ai_voltage_chan(mod5_channels, min_val=-10, max_val=10)
        ai_task.ai_channels.add_ai_voltage_chan(mod6_channels, min_val=-10, max_val=10)
        ai_task.timing.cfg_samp_clk_timing(
            sample_rate_Hz,
            source="OnboardClock",
            sample_mode=AcquisitionType.FINITE,
            samps_per_chan=samples
        )
        ai_task.triggers.start_trigger.cfg_dig_edge_start_trig(
            trigger_source="/cDAQ9188-169338E/PFI1",
            # trigger_level=1.5,
            trigger_edge=Edge.FALLING
        )
        print("Waiting for trigger on PFI1")
        data = ai_task.read(number_of_samples_per_channel=samples,timeout=10.0)
        print("trigger recieved")
   
    # nidaqmx multi-channel read: shape (n_channels, samples_per_channel) -> PT1..PT8
    data = np.asarray(data, dtype=np.float64)



    if data.ndim == 1:
        pt1 = data
        n_samples = pt1.shape[0]
        pt2 = pt3 = pt4 = pt5 = pt6 = pt7 = pt8 = np.zeros(n_samples)
    else:
        n_ch, n_samples = data.shape
        pt1 = data[0] if n_ch >= 1 else np.zeros(n_samples)
        pt2 = data[1] if n_ch >= 2 else np.zeros(n_samples)
        pt3 = data[2] if n_ch >= 3 else np.zeros(n_samples)
        pt4 = data[3] if n_ch >= 4 else np.zeros(n_samples)
        pt5 = data[4] if n_ch >= 5 else np.zeros(n_samples)
        pt6 = data[5] if n_ch >= 6 else np.zeros(n_samples)
        pt7 = data[6] if n_ch >= 7 else np.zeros(n_samples)
        pt8 = data[7] if n_ch >= 8 else np.zeros(n_samples)

    # One CSV per test: properties in header, then time and PT1–PT8 columns
    filename = f"C:\\Users\\dedic-lab\\Documents\\Detonation_Facility_Testing\\TestData{testcount}.csv"
    time_s = np.arange(n_samples, dtype=np.float64) / sample_rate_Hz

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["TestNumber", testcount])
        writer.writerow(["VacuumPressure_Pa", float(vacuum_pressure)])
        writer.writerow(["PostFillPressure_Pa", float(fill_pressure)])
        writer.writerow(["DateTime", datetime.now().isoformat()])
        writer.writerow(["SampleRate_Hz", sample_rate_Hz])
        writer.writerow([])
        writer.writerow(["time_s", "PT1", "PT2", "PT3", "PT4", "PT5", "PT6", "PT7", "PT8"])
        for i in range(n_samples):
            writer.writerow([time_s[i], pt1[i], pt2[i], pt3[i], pt4[i], pt5[i], pt6[i], pt7[i], pt8[i]])


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

    return avg * 103.421 / 10 # Convert voltage to kPa based on sensor specs (10 V = 15 psi) 

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

    return avg * 0.013332 # Convert voltage to kPa based on sensor specs (10 V = 1 tor)


def read_mfcs(testcount):
    ai_channel = "cDAQ9188-169338EMod3/ai0:3"
    sample_rate = 1000  # 1 kHz 
    duration = 7      # seconds
    samples = int(sample_rate * duration)

    with nidaqmx.Task() as ai_task:
        ai_task.ai_channels.add_ai_voltage_chan(ai_channel, min_val=-10, max_val=10)
        ai_task.timing.cfg_samp_clk_timing(
            sample_rate, 
            sample_mode=AcquisitionType.FINITE, 
            samps_per_chan=samples
        )
        data = ai_task.read(number_of_samples_per_channel=samples, timeout=20)
   

 # nidaqmx multi-channel read: shape (n_channels, samples_per_channel) -> PT1..PT8
    data = np.asarray(data, dtype=np.float64)
    # if data.ndim == 1:
    #     pt1 = data
    #     n_samples = pt1.shape[0]
    #     pt2 = pt3 = pt4 = pt5 = pt6 = pt7 = pt8 = np.zeros(n_samples)
    # else:
    #     n_ch, n_samples = data.shape
    fill = data[0]
    vac = data[1]
    mfc1 = data[2] 
    mfc2 = data[3] 
    n_samples = mfc1.shape[0]


    # One CSV per test: properties in header, then time and PT1–PT8 columns
    filename = f"C:\\Users\\dedic-lab\\Documents\\Detonation_Facility_Testing\\MFCTestData{testcount}.csv"
    time_s = np.arange(n_samples, dtype=np.float64) / sample_rate

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["TestNumber", testcount])
        # writer.writerow(["VacuumPressure_Pa", float(vacuum_pressure)])
        # writer.writerow(["PostFillPressure_Pa", float(fill_pressure)])
        writer.writerow(["DateTime", datetime.now().isoformat()])
        writer.writerow(["SampleRate_Hz", sample_rate])
        writer.writerow([])
        writer.writerow(["time_s", "fill", "vac", "MFC1", "MFC2"])
        for i in range(n_samples):
            writer.writerow([time_s[i], fill[i], vac[i], mfc1[i], mfc2[i]])

   