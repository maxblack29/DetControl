import nidaqmx
from nidaqmx.constants import LineGrouping

class NI9474Controller:
    def __init__(self, device_name="Dev1", port="port0"):
        self.device_name = device_name
        self.port = port

    def set_line(self, line_number, state):
        """
        Set the specified line (0-7) to the given state (True=ON, False=OFF).
        """
        line_name = f"{self.device_name}/{self.port}/line{line_number}"
        with nidaqmx.Task() as task:
            task.do_channels.add_do_chan(line_name)
            task.write(state)

    def set_multiple_lines(self, states):
        """
        Set all 8 lines at once. 'states' should be a list of 8 booleans.
        """
        line_names = [f"{self.device_name}/{self.port}/line{i}" for i in range(8)]
        with nidaqmx.Task() as task:
            task.do_channels.add_do_chan(','.join(line_names))
            task.write(states)

# Example usage:
# controller = NI9474Controller(device_name="Dev1", port="port0")
# controller.set_line(0, True)   # Turn ON line 0
# controller.set_line(1, False)  # Turn OFF line 1
# controller.set_multiple_lines([True, False, False, True, False, False, False, False])
