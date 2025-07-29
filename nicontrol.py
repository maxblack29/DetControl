import nidaqmx
from nidaqmx.constants import LineGrouping
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

        '''
k = 0
while k < 5:
    state = np.logical_not(state)
    k = k+1
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(device_name, line_grouping=LineGrouping.CHAN_PER_LINE)
        task.write(state)
    time.sleep(1)

    '''