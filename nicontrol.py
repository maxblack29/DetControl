import nidaqmx
from nidaqmx.constants import LineGrouping, AcquisitionType, LoggingMode, LoggingOperation, READ_ALL_AVAILABLE
from random import sample 
import numpy as np
import time


#port = 'port0'


def set_digital_output(states): #for Mod4 (plumbing)
    device_name = "cDAQ9188-169338EMod4/port0/line0:7"
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(device_name, line_grouping=LineGrouping.CHAN_PER_LINE)
        task.write(states)

def set_digital_output_2(states): #for Mod2 (pump, speaker)
    device_name = "cDAQ9188-169338EMod2/port0/line0:7"
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(device_name, line_grouping=LineGrouping.CHAN_PER_LINE)
        task.write(states)

def read_vaccuum_state(threshold):
    ai_channel = "cDAQ9188-169338EMod6/ai0"
    sample_rate = 125e6 # 125 MS/s
    duration = 5e-3  # 8 milliseconds
    samples = int(sample_rate * duration)

    with nidaqmx.Task() as ai_task:
        ai_task.ai_channels.add_ai_voltage_chan(ai_channel, min_val=-10, max_val=10)
        ai_task.timing.cfg_samp_clk_timing(sample_rate, sample_mode=AcquisitionType.FINITE, samps_per_chan=samples)
        data = ai_task.read(number_of_samples_per_channel=samples)
        # If any sample is above the threshold, return True
        if np.any(np.array(data) > threshold):
            return True
        return False


#had to write separate function because this one is on Mod2 
def set_ignite_read_pressure(on_states, testcount): 
    ignite_device = "cDAQ9188-169338EMod2/port0/line0:7"
    ai_channel =  "cDAQ9188-169338EMod6/ai0"  
    off_states  = [False] * len(on_states)  
    
    #send signal to ignite
    with nidaqmx.Task() as do_task:
        do_task.do_channels.add_do_chan(ignite_device, line_grouping=LineGrouping.CHAN_PER_LINE)
        do_task.write(on_states)
        time.sleep(0.1) 
        do_task.write(off_states)

# #read pressure transducers 
    # sample_rate = 125 * 10^6 #125 MS/s
    # duration = 8 * 10^-3  # 8 milliseconds
    # samples = sample_rate * duration
    #testcount += 1
    # with nidaqmx.Task() as ai_task:
    #     ai_task.ai_channels.add_ai_voltage_chan(ai_channel, min_val=-10, max_val=10)
    #     ai_task.timing.cfg_samp_clk_timing(sample_rate, sample_mode=AcquisitionType.FINITE,samps_per_chan=samples)
    #     filename = f"TestData{testcount}.tdms"
    #     ai_task.in_stream.configure_logging(filename, LoggingMode.LOG_AND_READ, operation=LoggingOperation.CREATE_OR_REPLACE)

    #     data = ai_task.read(number_of_samples_per_channel=samples)
          
def read_pressure():
    ai_channel = "cDAQ9188-169338EMod8/ai0"
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
    ai_channel = "cDAQ9188-169338EMod8/ai1"
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