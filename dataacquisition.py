from random import sample
import nidaqmx
from nidaqmx.constants import AcquisitionType, LoggingMode, LoggingOperation, READ_ALL_AVAILABLE
import matplotlib.pyplot as plt #Weird import stuff, this works

#michael change: testing the data acquisition code 
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("cDAQ9188-169338EMod6/ai0", min_val = -10, max_val = 10)  # Creates channels to read voltage
    sample_rate = 1000  # Sample rate in Hz
    duration = 5  # Duration in seconds
    samples = sample_rate * duration  # Total number of samples to acquire  
    task.timing.cfg_samp_clk_timing(sample_rate, sample_mode = AcquisitionType.FINITE, samps_per_chan=samples) #Hardware timing
    task.in_stream.configure_logging("TestData.tdms", LoggingMode.LOG_AND_READ, operation=LoggingOperation.CREATE_OR_REPLACE)
    data = task.read(READ_ALL_AVAILABLE)
    print(f"Data read from the channel: {data}")
    plt.plot(data)
    plt.ylabel("Voltage")
    plt.title("Test data")
    plt.show()

#AIChannel(name=cDAQ9188-169338EMod6/port0/ai0) 

def data_acq_static():
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("cDAQ9188-169338EMod6/port0/ai0", min_val = -10, max_val = 10)
        task.timing.cfg_samp_clk_timing(1000, sample_mode= AcquisitionType.FINITE, samps_per_chan=1000)
        data = task.read(READ_ALL_AVAILABLE)
        plt.plot(data)
        plt.ylabel("Voltage")
        plt.xlabel("Sample Number")
        plt.title("Static Pressure Data Acquisition")
        plt.show()

# def data_acq_dynamic():
#     k=1
#     with nidaqmx.Task() as task:
#         task.ai_channels.add_ai_voltage_chan(#Don't know the channel name yet, don't know the min and max val)
#         task.timing.cfg_samp_clk_timing(1000,sample_mode = AcquisitionType.FINITE, samps_per_chan = 1000)
#         task.in_stream.configure_logging(f"TestData{k}.tdms", LoggingMode.LOG_AND_READ, operation=LoggingOperation.CREATE_OR_REPLACE)
#         k += 1
#         data = task.read(READ_ALL_AVAILABLE)
