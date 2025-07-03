from os import device_encoding
import nidaqmx
from nidaqmx.constants import LineGrouping
import time

device_encoding = "cDAQ9188-169338EMod3/port0/line0:7" 

initial_state = [False, False, False, False, False, False, False, False]
#s1 = initial_state[0]
#s2 = initial_state[1]
#s3 = intial_state[2]
#s4 = intial_state[3]
#s5 = intial_state[4]
#s6 = intial_state[5]
#s7 = initial_state[6]
#empty = intial_state[8]  This might change later as we might add another solenoid to the system


#Make global so that you can import into GUI

# Change this once you know the initial states of the lines. 
def mixing_stage(states):
    for e in states:
        if e == [1, 2, 3, 4, 5, 6]:
            states[i] = False
        else:
            states[i] = True
        return states
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(device_name, line_grouping=LineGrouping.CHAN_PER_LINE)
        task.write(states)
        time.sleep(5) #this is how long the purge is supposed to take? Confirm with Sean
#This first function is for the first stage of the detonation sequence (Fuel injection and Mixing stages)
def driver_injedction(states):
    for k in states:
        if k == [1, 2, 3, 4, 6]:
            states[i] = True
        else:
            states[i] = False
        return states
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(device_name, line_grouping=LineGrouping.CHAN_PER_LINE)
        task.write(states)
        time.sleep(5) #Don't know how long this is supposed to take, 5 is a placeholder
#This second function is for the second stage of the detonation sequence (Driver injection stage)

def vacuumpost(states):
    for i in states:
        if i == [0, 5]:
            states[i] = False
        else:
            states[i] = True
        return states
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(device_name, line_grouping=LineGrouping.CHAN_PER_LINE)
        task.write(states)
        time.sleep(5) #Don't know how long this is supposed to take, 5 is a placeholder
#This thir function is for the third stage of the detonation sequence (Vacuum post stage)

def emer_purge(states):
    for j in states:
        if j == [0, 4, 6]:
            states[j] = False
        else:
            states[j] = True
        return states
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(device_name, line_grouping=LineGrouping.CHAN_PER_LINE)
        task.write(states)
        time.sleep(5) #Don't know how long this is supposed to take, 5 is a placeholder
#This fourth function is for the fourth stage of the detonation sequence (Emergency purge stage)