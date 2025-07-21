import nidaqmx
from nidaqmx.constants import AcquisitionType, READ_ALL_AVAILABLE
import matplotlib.pyplot as plt #Weird import stuff, this works
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("cDAQ9188-169338EMod8/ai0", min_val = -10, max_val = 10)  # Creates channels to read voltage
    task.timing.cfg_samp_clk_timing(1000, sample_mode = AcquisitionType.FINITE, samps_per_chan=1000) #Hardware timing
    #task.in_stream.configure_logging("TestData.tdms", LoggingMode.LOG_AND_READ, operation=LoggingOperation.CREATE_OR_REPLACE)
    data = task.read(READ_ALL_AVAILABLE)
    print(f"Data read from the channel: {data}")
    plt.plot(data)
    plt.ylabel("Voltage")
    plt.title("Test data")
    plt.show()
'''
device_name = "cDAQ9188-169338EMod6/port0/line0:3"
import nidaqmx
from nidaqmx.constants import AcquisitionType, READ_ALL_AVAILABLE
with nidaqmx.Task() as task:
    '''
#AIChannel(name=cDAQ9188-169338EMod6/port0/ai0) 
