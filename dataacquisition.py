import nidaqmx
from nidaqmx.constants import AcquisitionType, READ_ALL_AVAILABLE
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")  # Creates channels to read voltage
    task.timing.cfg_samp_clk_timing(1000, sample_mode = AcquisitionType.FINITE, samps_per_chan=1000) #Hardware timing
    data = task.read(READ_ALL_AVAILABLE)

# AIChannel = "Dev1/ai0" is the name of the actual channel