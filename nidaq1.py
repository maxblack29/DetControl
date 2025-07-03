import nidaqmx
from nidaqmx.constants import LineGrouping
import pdb

ni9474_channel = "cDAQ9188-169338EMod3/port0/line0:7" #Don't know if this is correct, was in Harsh's and Darsh's code

#Import nidaqmx library and LineGrouping constant (might not need LineGrouping)
class NI9474Controller:
    def __init__(self, device_name = ni9474_channel, port = 'port0'):
        self.device_name = device_name
        self.port = port 
    #Sets global variables for device_name and port, which can be used to set the line

    def set_line(self, line_number, state):
        if line_number<0 or line_number>7:
            print("Error: line number must be between 0 and 7")
        else:
            update = f"Setting line {line_number} to {'On' if state else 'Off'}"
            print(update)
            #line_name = f"{self.device_name}/{self.port}/line{line_number}" #error with how the line_name is updating
        #Sets the line name based on the device_name and port, and checks if the line number is valid (0-7)
        #Updates device_name with the line number (ni9474_channel would become "cDAQ9188-169338EMod1/port0/line3" for line_number=3)
            with nidaqmx.Task() as task:
                #task.do_channels.add_do_chan(line_name, line_grouping=LineGrouping.CHAN_PER_LINE)
                task.do_channels.add_do_chan(self.device_name, line_grouping=LineGrouping.CHAN_PER_LINE)
                task.write(state)
        #Writes the state to the specified line using nidaqmx.Task()
    def set_all_lines(self, states):
        if len(states) !=8:
            print("Error: states must be a list of 8 Booleans")
            return
        #checks the length of the states array to ensure that it isn't over or under 8 elements
        else:
            for i in range(8):
                update1 = f"Setting line {i} to {'On' if states[i] else 'Off'}"
                print(update1)
        #Updates the state of each line based on the states array, should flip each line to the corresponding state in the array
    def set_some_lines(self, line_numbers, states):
        #line_numbers should be an array of integers representing the lines to be set
        #States should be an array of Booleans 
        for j in line_numbers:
            if j<0 or j>7:
                print(f"Error: line number {j} must be between 0 and 7")
                return
            elif len(j)==8:
                print("Error, please use set_all_lines function")
                return 
            else:
                update2 = f"Setting line {j} to {'On" if state else "Off'}"
                print(update2)
                return
            return
