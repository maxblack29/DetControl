import nidaqmx
from nidaqmx.constants import LineGrouping, AcquisitionType, Edge, TerminalConfiguration
import numpy as np
import threading
import time
from datetime import datetime
import csv

import bnc_box_control

# MFC analog mapping and scale limits (0–5 V corresponds to max SLPM)
MFC_MAX_SLPM = {"A": 20.0, "B": 20.0, "C": 50.0, "D": 50.0}
MFC_AO_CHANNELS = "cDAQ9188-169338EMod7/ao0:3"
MFC8_DEVICE = "cDAQ9188-169338EMod8"
FILL_GAUGE_AI_CHANNEL = "cDAQ9188-169338EMod3/ai0"

_FILL_LOG_N_AI_CH = 5  # Mod3 gauge + Mod8 ai0..3 (order below)

_daq1_state = [False] * 8
_daq2_state = [False] * 8
_ai_read_lock = threading.Lock()


# Mod1 port0: 0=S2 fuel mix, 1=S1 fuel, 2=S3 ox, 3=S5 reactant mix, 4=S4 ox mix,
# 5=S9 vacuum valve, 6=S6 purge (NO), 7=unused.
# Mod2 port0: 0=S7 exhaust (NO), 1=S8 gauge, 3=S10 vacuum pump; 6=timing out, 7=speaker.
DAQ2_LINE_TIMING_OUTPUT = 6
DAQ2_LINE_SPEAKER = 7

#DAQ1 controller 
def set_digital_output(states):
    global _daq1_state
    device_name = "cDAQ9188-169338EMod1/port0/line0:7"
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(device_name, line_grouping=LineGrouping.CHAN_PER_LINE)
        task.write(states)
    _daq1_state = list(states)

#DAQ2 controller
def set_digital_output_2(states):
    global _daq2_state
    device_name = "cDAQ9188-169338EMod2/port0/line0:7"
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(device_name, line_grouping=LineGrouping.CHAN_PER_LINE)
        task.write(states)
    _daq2_state = list(states)


#used for GUI updating
def get_daq_states():
    return _daq1_state[:], _daq2_state[:]


def _slpm_to_volts(setpoint_slpm, max_slpm):
    # Inverse of voltage→SLPM in acquire_fill_mfc_log: commanded SLPM → V to the AO channels.
    setpoint = max(0.0, min(float(setpoint_slpm), float(max_slpm)))
    return 5.0 * setpoint / float(max_slpm)


def set_mfc_setpoints_analog(setpoint_a, setpoint_b, setpoint_c, setpoint_d=0.0):
    voltages = [
        _slpm_to_volts(setpoint_a, MFC_MAX_SLPM["A"]),
        _slpm_to_volts(setpoint_b, MFC_MAX_SLPM["B"]),
        _slpm_to_volts(setpoint_c, MFC_MAX_SLPM["C"]),
        _slpm_to_volts(setpoint_d, MFC_MAX_SLPM["D"]),
    ]
    with nidaqmx.Task() as ao_task:
        ao_task.ao_channels.add_ao_voltage_chan(MFC_AO_CHANNELS, min_val=0.0, max_val=5.0)
        ao_task.write(voltages, auto_start=True)


# Output: time_s, pressure_kPa, flow_a–d (numpy arrays). fill_log_csv adds phase/event and writes CSV.
def acquire_fill_mfc_log(duration_s, sample_rate_hz):
    duration_s = float(duration_s)
    sr = float(sample_rate_hz)
    empty = {
        "time_s": np.array([]),
        "pressure_kpa": np.array([]),
        "flow_a": np.array([]),
        "flow_b": np.array([]),
        "flow_c": np.array([]),
        "flow_d": np.array([]),
        "duration_s": 0.0,
        "sample_rate_hz": sr,
    }

    #this part checks if the duration and sample rate are valid
    if duration_s <= 0 or sr <= 0:
        return empty
    n = max(2, int(round(sr * duration_s)))
    timeout_s = max(duration_s + 15.0, 5.0)

    with _ai_read_lock:
        with nidaqmx.Task() as ai_task:
            # Mod3 gauge + Mod8 ai0:3 (row 0 = gauge, 1–4 = MFC A–D).
            ai_task.ai_channels.add_ai_voltage_chan(FILL_GAUGE_AI_CHANNEL, min_val=0, max_val=10)
            for suffix in ("ai0", "ai1", "ai2", "ai3"):
                ai_task.ai_channels.add_ai_voltage_chan(
                    f"{MFC8_DEVICE}/{suffix}",
                    min_val=0.0,
                    max_val=5.0,
                    terminal_config=TerminalConfiguration.RSE,
                )
            ai_task.timing.cfg_samp_clk_timing(
                sr,
                sample_mode=AcquisitionType.FINITE,
                samps_per_chan=n,
            )
            #this reads the data from the task
            data = ai_task.read(number_of_samples_per_channel=n, timeout=timeout_s)

    data = np.asarray(data, dtype=np.float64) #converts the data to a numpy array

    #this part checks if the data is in the correct format
    # Usually (5, n); if you ever see (n, 5), flip once so row 0 stays the gauge.
    if (
        data.ndim == 2
        and data.shape[0] != _FILL_LOG_N_AI_CH
        and data.shape[1] == _FILL_LOG_N_AI_CH
    ):
        data = data.T
    if data.ndim != 2 or data.shape[0] != _FILL_LOG_N_AI_CH:
        raise RuntimeError(
            f"acquire_fill_mfc_log: expected {_FILL_LOG_N_AI_CH} channels x samples, got {data.shape}"
        )

    # Per-sample conversion: gauge uses facility kPa scale; each MFC uses V × (full_scale_SLPM / 5 V).
    v_g = data[0] #gauge voltage
    va, vb, vc, vd = data[1], data[2], data[3], data[4] #mfc voltages
    p_kpa = v_g * 103.421 / 10.0
    fa = va * MFC_MAX_SLPM["A"] / 5.0
    fb = vb * MFC_MAX_SLPM["B"] / 5.0
    fc = vc * MFC_MAX_SLPM["C"] / 5.0
    fd = vd * MFC_MAX_SLPM["D"] / 5.0
    time_s = np.arange(n, dtype=np.float64) / sr #time array from the number of samples and the sample rate
    
    return {
        "time_s": time_s,
        "pressure_kpa": p_kpa,
        "flow_a": fa,
        "flow_b": fb,
        "flow_c": fc,
        "flow_d": fd,
        "duration_s": float(n / sr),
        "sample_rate_hz": sr,
    }


#needed separate function for threading. just calls the acquire_fill_mfc_log function and stores the result in the result_container
def fill_log_acquisition_thread_target(result_container, duration_s, sample_rate_hz, key="acq"):
    """Store one continuous Mod3+Mod8 log in result_container[key]. Use as threading.Thread(target=...)."""
    result_container[key] = acquire_fill_mfc_log(duration_s, sample_rate_hz)


#ignites the facility and reads the pressure taps
def set_ignite_read_pressure(testcount, vacuum_pressure, fill_pressure):
    ignite_port = "cDAQ9188-169338EMod2/port0/line0:7"
    _, d2 = get_daq_states()
    base = list((d2 + [False] * 8)[:8])
    on_states = list(base)
    on_states[DAQ2_LINE_TIMING_OUTPUT] = True
    off_states = list(base)
    off_states[DAQ2_LINE_TIMING_OUTPUT] = False

    bnc_box_control.switch_preset(12) #switches bnc box to triggered single shot for PLIF 
    bnc_box_control.arm("ON") #ensures BNC box is armed for trigger signal 

    with nidaqmx.Task() as do_task:
        do_task.do_channels.add_do_chan(ignite_port, line_grouping=LineGrouping.CHAN_PER_LINE)
        do_task.write(on_states)
        time.sleep(0.010)
        do_task.write(off_states)
    global _daq2_state
    _daq2_state = off_states
    print("timing box signal sent")

    sample_rate_Hz = 1_000_000
    duration_s = 0.1
    samples = int(sample_rate_Hz * duration_s)
    mod5_channels = "cDAQ9188-169338EMod5/ai0:3"
    mod6_channels = "cDAQ9188-169338EMod6/ai0:3"

    with nidaqmx.Task() as ai_task:
        ai_task.ai_channels.add_ai_voltage_chan(mod5_channels, min_val=-10, max_val=10)
        ai_task.ai_channels.add_ai_voltage_chan(mod6_channels, min_val=-10, max_val=10)
        ai_task.timing.cfg_samp_clk_timing(
            sample_rate_Hz,
            source="OnboardClock",
            sample_mode=AcquisitionType.FINITE,
            samps_per_chan=samples,
        )
        ai_task.triggers.start_trigger.cfg_dig_edge_start_trig(
            trigger_source="/cDAQ9188-169338E/PFI1",
            trigger_edge=Edge.FALLING,
        )
        print("Waiting for trigger on PFI1")
        data = ai_task.read(number_of_samples_per_channel=samples, timeout=10.0)
        print("acquisition complete")

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

    filename = f"C:\\Users\\dedic-lab\\Documents\\Detonation_Facility_Testing\\TestData{testcount}.csv"
    time_axis = np.arange(n_samples, dtype=np.float64) / sample_rate_Hz
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
            writer.writerow(
                [time_axis[i], pt1[i], pt2[i], pt3[i], pt4[i], pt5[i], pt6[i], pt7[i], pt8[i]]
            )
    
    bnc_box_control.switch_preset(9) #switches bnc box back to continuous mode 
    


#reads the pressure from the fill gauge
def read_pressure():
    ai_channel = FILL_GAUGE_AI_CHANNEL
    sample_rate = 1000
    duration = 0.1
    samples = int(sample_rate * duration)
    with _ai_read_lock:
        with nidaqmx.Task() as ai_task:
            ai_task.ai_channels.add_ai_voltage_chan(ai_channel, min_val=0, max_val=10)
            ai_task.timing.cfg_samp_clk_timing(
                sample_rate,
                sample_mode=AcquisitionType.FINITE,
                samps_per_chan=samples,
            )
            data = ai_task.read(number_of_samples_per_channel=samples)
            avg = np.mean(data)
    return avg * 103.421 / 10


#reads the pressure from the vacuum gauge
def read_vacuum_pressure():
    ai_channel = "cDAQ9188-169338EMod3/ai1"
    sample_rate = 1000
    duration = 0.1
    samples = int(sample_rate * duration)
    with _ai_read_lock:
        with nidaqmx.Task() as ai_task:
            ai_task.ai_channels.add_ai_voltage_chan(ai_channel, min_val=0, max_val=10)
            ai_task.timing.cfg_samp_clk_timing(
                sample_rate,
                sample_mode=AcquisitionType.FINITE,
                samps_per_chan=samples,
            )
            data = ai_task.read(number_of_samples_per_channel=samples)
            avg = np.mean(data)
    return avg * 13.332 #returns pascals