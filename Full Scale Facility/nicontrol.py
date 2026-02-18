import nidaqmx
from nidaqmx.constants import LineGrouping, AcquisitionType, LoggingMode, LoggingOperation, READ_ALL_AVAILABLE
from random import sample 
import numpy as np
import time


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
def set_ignite_read_pressure(on_states, testcount, vacuum_pressure, fill_pressure): 
    ignite_device = "cDAQ9188-169338EMod2/port6/line0:7"
    ai_channels =  "cDAQ9188-169338EMod6/ai0:ai3"  
    on_states = [True, False, True, False, False, False, True, False] #ignite is on port 6 
    off_states = [True, False, True, False, False, False, False, False] #Daq2 states post fill  
    
    #send signal to ignite
    with nidaqmx.Task() as do_task:
        do_task.do_channels.add_do_chan(ignite_device, line_grouping=LineGrouping.CHAN_PER_LINE)
        do_task.write(on_states)
        time.sleep(0.1) 
        do_task.write(off_states)

    #read pressure transducers immediately aftr
        sample_rate = 125 * 10^6 #125 MS/s
        duration = 10 * 10^-3  # 10 milliseconds
        samples = sample_rate * duration

        with nidaqmx.Task() as ai_task:
            ai_task.ai_channels.add_ai_voltage_chan(ai_channels, min_val=-10, max_val=10)
            ai_task.timing.cfg_samp_clk_timing(sample_rate, sample_mode=AcquisitionType.FINITE,samps_per_chan=samples)
            filename = f"TestData{testcount}.tdms"
            ai_task.in_stream.configure_logging(filename, LoggingMode.LOG_AND_READ, operation=LoggingOperation.CREATE_OR_REPLACE)

            data = ai_task.read(number_of_samples_per_channel=samples)
          
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