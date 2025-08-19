import nidaqmx
from nidaqmx.constants import LineGrouping, AcquisitionType, LoggingMode, LoggingOperation, READ_ALL_AVAILABLE
from random import sample 
import numpy as np
import time


#port = 'port0'

def set_all_digital_outputs(states):
    # states: list or array of 8 booleans
    device_name = "cDAQ9188-169338EMod4/port0/line0:7"
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(device_name, line_grouping=LineGrouping.CHAN_PER_LINE)
        task.write(states)

def set_digital_output(states):
    device_name = "cDAQ9188-169338EMod4/port0/line0:7"
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(device_name, line_grouping=LineGrouping.CHAN_PER_LINE)
        task.write(states)


#had to write separate function because this one is on Mod2 
def set_ignite_read_pressure(on_states, testcount): 
    ignite_device = "cDAQ9188-169338EMod2/port0/line0:7"
    ai_channel =  "cDAQ9188-169338EMod6/ai0"  # Replace with your actual AI channel name
    off_states  = [False] * len(on_states)  
    
    #send signal to ignite
    with nidaqmx.Task() as do_task:
        do_task.do_channels.add_do_chan(ignite_device, line_grouping=LineGrouping.CHAN_PER_LINE)
        do_task.write(on_states)
        time.sleep(0.003) 
        do_task.write(off_states)

    # #read pressure transducers 
    # sample_rate = 1000
    # duration = 5
    # samples = sample_rate * duration
    #testcount += 1
    # with nidaqmx.Task() as ai_task:
    #     ai_task.ai_channels.add_ai_voltage_chan(ai_channel, min_val=-10, max_val=10)
    #     ai_task.timing.cfg_samp_clk_timing(sample_rate, sample_mode=AcquisitionType.FINITE,samps_per_chan=samples)
    #     filename = f"TestData{testcount}.tdms"
    #     ai_task.in_stream.configure_logging(filename, LoggingMode.LOG_AND_READ, operation=LoggingOperation.CREATE_OR_REPLACE)

    #     data = ai_task.read(number_of_samples_per_channel=samples)
   
    


#  '''
# k = 0
# while k < 5:
#     state = np.logical_not(state)
#     k = k+1
#     with nidaqmx.Task() as task:
#         task.do_channels.add_do_chan(device_name, line_grouping=LineGrouping.CHAN_PER_LINE)
#         task.write(state)
#     time.sleep(1)

#     '''