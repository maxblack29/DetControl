import time
import nidaqmx
from nidaqmx.constants import LineGrouping

with nidaqmx.Task() as task:
    task.do_channels.add_do_chan("cDAQ9188-169338EMod2/port0/line0:7", line_grouping=LineGrouping.CHAN_PER_LINE)
    task.write([True, False, False, False, False, False, False, False])
    time.sleep(0.01)
    task.write([False, False, False, False, False, False, False, False])