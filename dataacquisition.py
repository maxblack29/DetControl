import nidaqmx
from nidaqmx.constants import AcquisitionType, READ_ALL_AVAILABLE
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("cDAQ9188-169338EMod6/port0/ai0")  # Creates channels to read voltage
    task.timing.cfg_samp_clk_timing(1000, sample_mode = AcquisitionType.FINITE, samps_per_chan=1000) #Hardware timing
    data = task.read(READ_ALL_AVAILABLE)

'''
device_name = "cDAQ9188-169338EMod6/port0/line0:3"
import nidaqmx
from nidaqmx.constants import AcquisitionType, READ_ALL_AVAILABLE
with nidaqmx.Task() as task:
    '''
AIChannel(name=cDAQ9188-169338EMod6/port0/ai0) 