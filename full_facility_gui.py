import sys
from PySide6.QtWidgets import QApplication, QDialog, QLabel
from PySide6.QtCore import QTimer, QThread, Signal, QObject, Slot, QProcess
from PySide6.QtCore import QTimer
import full_facility_run_methods
from plumbingdiagram import Ui_plumbingdiagram
from greenledwidget import GreenLed
import nidaqmx #might not be needed since I imported nicontrol
import nicontrol
from nicontrol import set_digital_output
from nidaqmx.constants import AcquisitionType, READ_ALL_AVAILABLE
import alicatcontrol
import asyncio
#import dataacquisition
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import mfcreadout

import pdb
import pyqtgraph as pg
import matplotlib.pyplot as plt

from ui_full_facility_gui_script import Ui_full_facility_gui
'''This calls the python file that was created FROM the .ui file (ui_full_facility_gui_script.py). 
When updating gui in qt designer, must update the PYTHON file to see the updates.'''



class AutomationWorker(QObject):
    finished = Signal()
    def __init__(self, setpointA, setpointB, setpointC, setpointD, setpointC_driver):
        super().__init__()
        self.setpointA = setpointA
        self.setpointB = setpointB
        self.setpointC = setpointC
        self.setpointD = setpointD
        self.setpointC_driver = setpointC_driver

    def runauto(self):
        asyncio.run(full_facility_run_methods.automatic_test(self.setpointA, self.setpointB, self.setpointC, self.setpointD, self.setpointC_driver))
        self.finished.emit()
 
    def runstanpurge(self):
        asyncio.run(full_facility_run_methods.purge(self.setpointA, self.setpointB, self.setpointC, self.setpointD))
        self.finished.emit()


class SolenoidWorker(QObject):
    finished = Signal()
    def __init__(self, states, testcount):
        super().__init__()
        self.states = states
        self.testcount = testcount

    def runsolenoid(self):
        nicontrol.set_digital_output(self.states)
        self.finished.emit()
    
    def runignite(self):
        nicontrol.set_ignite_read_pressure(self.states, self.testcount) 
        self.finished.emit()




class MyDialog(QDialog):
    def __init__(self, plumbing_diagram=None):
        #MyDialog starts the GUI. this first secion is for initializing and connecting buttons. 
        super().__init__()
        self.ui = Ui_full_facility_gui()
        self.ui.setupUi(self)
        #self.plumbing_diagram = plumbing_diagram
        
        self.solenoids = [False, False, False, False, False, False, False, False] #Sets a bool array for 8 channels, last channel is empty
        nicontrol.set_digital_output(self.solenoids) #Sets the digital output to the solenoid states

        self.testcount = 0 #zeroes the test count for data acquisition when gui is opened

        #Connect each open and close button
        self.ui.openS1.clicked.connect(lambda: self.toggle_solenoid(0, True))
        self.ui.closeS1.clicked.connect(lambda: self.toggle_solenoid(0, False))
        self.ui.openS2.clicked.connect(lambda: self.toggle_solenoid(1, True))
        self.ui.closeS2.clicked.connect(lambda: self.toggle_solenoid(1, False))
        self.ui.openS3.clicked.connect(lambda: self.toggle_solenoid(2, True))
        self.ui.closeS3.clicked.connect(lambda: self.toggle_solenoid(2, False))
        self.ui.openS4.clicked.connect(lambda: self.toggle_solenoid(3, False))  # Normally open
        self.ui.closeS4.clicked.connect(lambda: self.toggle_solenoid(3, True))  
        self.ui.openS5.clicked.connect(lambda: self.toggle_solenoid(4, True))
        self.ui.closeS5.clicked.connect(lambda: self.toggle_solenoid(4, False))
        self.ui.openS6.clicked.connect(lambda: self.toggle_solenoid(5, False)) # Normally open
        self.ui.closeS6.clicked.connect(lambda: self.toggle_solenoid(5, True))  
        self.ui.openS7.clicked.connect(lambda: self.toggle_solenoid(6, True))
        self.ui.closeS7.clicked.connect(lambda: self.toggle_solenoid(6, False))

        #Connects the update setpoints button
        self.ui.updatesetpoints.clicked.connect(self.save_setpoints)

        #Connects the reset flow button 
        self.ui.resetmfc.clicked.connect(self.reset_flow) #Might not need this

        #Retrieves the gas setpoints from the GUI 
        self.ui.mfcAsetpoint.returnPressed.connect(lambda: self.save_setpoints('A', float(self.ui.mfcAsetpoint.text())))
        self.ui.mfcBsetpoint.returnPressed.connect(lambda: self.save_setpoints('B', float(self.ui.mfcBsetpoint.text())))
        self.ui.mfcCsetpoint.returnPressed.connect(lambda: self.save_setpoints('C', float(self.ui.mfcCsetpoint.text())))
        self.ui.mfcDsetpoint.returnPressed.connect(lambda: self.save_setpoints('D', float(self.ui.mfcDsetpoint.text())))

        
        #Retrieves the gas type from the GUI
        self.ui.mfcAgas.currentTextChanged.connect(self.change_gas)
        self.ui.mfcBgas.currentTextChanged.connect(self.change_gas)
        self.ui.mfcCgas.currentTextChanged.connect(self.change_gas)
        self.ui.mfcDgas.currentTextChanged.connect(self.change_gas)

        #Connects the automation and purge buttons
        self.ui.testautomation.clicked.connect(self.begin_testing)
        self.ui.purgebutton.clicked.connect(self.purge)
        self.ui.igniteButton.clicked.connect(self.ignite)

        #Connect lcd displays with the SLPM readout
        
        # #COMMENT BELOW OUT IF CODE NOT WORKING
        # self.mfc_timer = QTimer(self)
        # self.mfc_timer.timeout.connect(self.update_mfc_lcds)
        # self.mfc_timer.start(2000)  # Update every 1000 ms (1 second)
        # #COMMENT ABOVE OUT IF CODE NOT WORKING

        #connects pressure display with the pressure input 
        self.pressure_timer = QTimer(self)
        self.pressure_timer.timeout.connect(self.update_pressure)
        self.pressure_timer.start(1000)  # Update every 1

        #connects vacuum pressure display with the pressure input 
        self.vacuum_pressure_timer = QTimer(self)
        self.vacuum_pressure_timer.timeout.connect(self.update_vacuum_pressure)
        self.vacuum_pressure_timer.start(1000)  # Update every 1
    
    def save_setpoints(self):
        #This function can be used to update the setpoints
        reset_button = self.ui.resetmfc
        set_flow_button = self.ui.updatesetpoints

        if set_flow_button.isEnabled():
            set_flow_button.setStyleSheet("background-color: green; color: white;")
        
            reset_button.setStyleSheet("")

        QTimer.singleShot(500, lambda:set_flow_button.setStyleSheet(""))

        setpointA = float(self.ui.mfcAsetpoint.text())
        setpointB = float(self.ui.mfcBsetpoint.text())
        setpointC = float(self.ui.mfcCsetpoint.text())
        setpointD = float(self.ui.mfcDsetpoint.text())
        asyncio.run(alicatcontrol.change_rate('A', setpointA))
        asyncio.run(alicatcontrol.change_rate('B', setpointB))
        asyncio.run(alicatcontrol.change_rate('C', setpointC))
        asyncio.run(alicatcontrol.change_rate('D', setpointD))

        self.ui.updatesetpoints.clicked.connect(self.save_setpoints)

    #This function will reset the flow setpoints to 0.0 SLPM for all gas controllers. 
    def reset_flow(self):
        reset_button = self.ui.resetmfc
        set_flow_button = self.ui.updatesetpoints
        if reset_button.isEnabled():
           reset_button.setStyleSheet("background-color: green; color: white;")
           set_flow_button.setStyleSheet("")

        QTimer.singleShot(500, lambda: reset_button.setStyleSheet(""))

        self.ui.mfcAsetpoint.setText("0.0")
        self.ui.mfcBsetpoint.setText("0.0")
        self.ui.mfcCsetpoint.setText("0.0")
        self.ui.mfcDsetpoint.setText("0.0")
        asyncio.run(alicatcontrol.change_rate('A', 0.0))
        asyncio.run(alicatcontrol.change_rate('B', 0.0))
        asyncio.run(alicatcontrol.change_rate('C', 0.0))
        asyncio.run(alicatcontrol.change_rate('D', 0.0))
        print("All gas setpoints reset to 0.0 SLPM.")
    

    #Figure out how to do a change_gas function
    def change_gas(self):
        #This function will change the gas type for each controller
        self.ui.mfcAgas.currentText()
        self.ui.mfcBgas.currentText()
        self.ui.mfcCgas.currentText()
        self.ui.mfcDgas.currentText()

        asyncio.run(alicatcontrol.set_gas('A', self.ui.mfcAgas.currentText()))
        asyncio.run(alicatcontrol.set_gas('B', self.ui.mfcBgas.currentText()))
        asyncio.run(alicatcontrol.set_gas('C', self.ui.mfcCgas.currentText()))
        #asyncio.run(alicatcontrol.set_gas('D', self.ui.mfcDgas.currentText()))

    #Toggles the solenoid states based on button clicks from the GUI. Will highlight the active state green based on user input.
    def toggle_solenoid(self, index, state):
         
        # Handle specific cases for S4 and S6
        if index == 3:  # S4
            state = not state  
        elif index == 5:  # S6
            state = not state  
        
        
        self.solenoids[index] = state #pulls state of current solenoid from button click
        open_button = getattr(self.ui, f"openS{index+1}")
        close_button = getattr(self.ui, f"closeS{index+1}")

        if state:
            open_button.setStyleSheet("background-color: green; color: white;")
            QTimer.singleShot(500, lambda: open_button.setStyleSheet(""))
            if open_button.isEnabled():
                open_button.setEnabled(False)
                close_button.setStyleSheet("")
        else:
            open_button.setStyleSheet("")
            close_button.setEnabled(False)
            close_button.setStyleSheet("background-color: green; color: white;")
            QTimer.singleShot(500, lambda: close_button.setStyleSheet(""))

        solenoid_worker = SolenoidWorker(self.solenoids, self.testcount)
        solenoid_thread = QThread()
        solenoid_worker.moveToThread(solenoid_thread)
        solenoid_thread.started.connect(solenoid_worker.runsolenoid)
        solenoid_worker.finished.connect(solenoid_thread.quit)
        solenoid_worker.finished.connect(lambda: self.reenable(open_button))
        solenoid_worker.finished.connect(lambda: self.reenable(close_button))

        # keep the worker alive so it's not garbage collected while running 
        if not hasattr(self, "_solenoid_threads"): 
            self._solenoid_threads = []
        self._solenoid_threads.append((solenoid_thread, solenoid_worker))

        solenoid_thread.start()
        if(index == 0):
            print(f"Solenoid S{index+1} {'Open' if state else 'Closed'}.")
        if(index == 1):
            print(f"Solenoid S{index+1} {'Open' if state else 'Closed'}.")
        if(index == 2):
            print(f"Solenoid S{index+1} {'Open' if state else 'Closed'}.")
        if(index == 3):
            print(f"Solenoid S{index+1} {'Open' if state else 'Closed'}.")
        if(index == 4):
            print(f"Solenoid S{index+1} {'Open' if state else 'Closed'}.")
        if(index == 5):
            print(f"Solenoid S{index+1} {'Open' if state else 'Closed'}.")
        if(index == 6):
            print(f"Solenoid S{index+1} {'Open' if state else 'Closed'}.")
        if(index == 7):
            print(f"Solenoid S{index+1} {'Open' if state else 'Closed'}.") 

  
    stop_test = False

    def begin_testing(self, stop_test):
        button = self.ui.testautomation
        button.setEnabled(False)
        self.ui.testautomation.setStyleSheet("")
        self.ui.purgebutton.setStyleSheet("")

        setpointA = float(self.ui.mfcAsetpoint.text())
        setpointB = float(self.ui.mfcBsetpoint.text())
        setpointC = float(self.ui.mfcCsetpoint.text())
        setpointC2 = float(self.ui.mfcCsetpoint_2.text())
        setpointD = float(self.ui.mfcDsetpoint.text())


        #Michael change: now gives automation its own worker/thread
        automation_worker = AutomationWorker(setpointA, setpointB, setpointC, setpointD, setpointC2)
        automation_thread = QThread()
        automation_worker.moveToThread(automation_thread)
        automation_thread.started.connect(automation_worker.runauto)
        automation_worker.finished.connect(automation_thread.quit)
        automation_worker.finished.connect(lambda: self.reenable(button))

        #keep the worker alive so it's not garbage collected while running 
        if not hasattr(self, "_automation_threads"):
            self._automation_threads = []
        self._automation_threads.append((automation_thread, automation_worker))

        automation_thread.start()
    
    def ignite(self): 
        button = self.ui.igniteButton
        button.setEnabled(False)
        self.ui.testautomation.setStyleSheet("")
        self.ui.purgebutton.setStyleSheet("")
        self.ui.igniteButton.setStyleSheet("")


        #CHANGE LATER WHEN WIRED 
        ignite_state = [False, False, False, False, False, False, False, False] #Set the ignite solenoid state to True
        testcount = self.testcount 
        ignite_worker = SolenoidWorker(ignite_state, testcount)
        ignite_thread = QThread()
        ignite_worker.moveToThread(ignite_thread)
        ignite_thread.started.connect(ignite_worker.runignite)
        ignite_worker.finished.connect(ignite_thread.quit)
        ignite_worker.finished.connect(lambda: self.reenable(button))

        # keep the worker alive so it's not garbage collected while running 
        if not hasattr(self, "_solenoid_threads"): 
            self._ignite_threads = []
        self._ignite_threads.append((ignite_thread, ignite_worker))

        ignite_thread.start()

    def purge(self):
        button = self.ui.purgebutton

        button.setEnabled(False)
        self.ui.testautomation.setStyleSheet("")
        self.ui.purgebutton.setStyleSheet("")

        setpointA = 0.0
        setpointB = 0.0
        setpointC = 0.0
        setpointC2 = 0.0
        setpointD = 0.0

        purge_worker = AutomationWorker(setpointA, setpointB, setpointC, setpointD, setpointC2)
        purge_thread = QThread()
        purge_worker.moveToThread(purge_thread)
        purge_thread.started.connect(purge_worker.runstanpurge)
        purge_worker.finished.connect(purge_thread.quit)
        purge_worker.finished.connect(lambda: self.reenable(button))

        # keep a reference so it's not garbage collected and prematurely closed 
        if not hasattr(self, "_automation_threads"):
            self._automation_threads = []
        self._automation_threads.append((purge_thread, purge_worker))

        purge_thread.start()

    def reenable(self, button):
        button.setEnabled(True)
        button.setStyleSheet("")


    async def update_mfc_lcds_async(self):
        flowA, flowB, flowC = await mfcreadout.read_flow_rates()
        self.ui.mfcAreadout.display(flowA)
        self.ui.mfcBreadout.display(flowB)
        self.ui.mfcCreadout.display(flowC)

    def update_mfc_lcds(self):
        asyncio.create_task(self.update_mfc_lcds_async())


    def update_pressure(self):
        pressure = nicontrol.read_pressure()
        self.ui.pressure_readout.display(pressure)

    def update_vacuum_pressure(self):
        vacuum_pressure = nicontrol.read_vacuum_pressure()
        self.ui.vacuum_pressure_readout.display(vacuum_pressure)    


    # def data_acquisition(self):
    #     with nidaqmx.Task() as task:
    #         task.ai_channels.add_ai_voltage_chan("cdaq9188-169338emod6/port0/ai0", min_val = -10, max_val = 10)
    #         task.timing.cfg_samp_clk_timing(1000, sample_mode= acquisitiontype.finite, samps_per_chan=1000)
    #         data = task.read(read_all_available)
    #         fig = figure(figsize=(4,4))
    #         ax = fig.add_subplot()
    #         ax.plot(data)
        


#main: whats actually running  
if __name__ == "__main__":
    def load_stylesheet(filename):
        with open(filename, "r") as f:
            return f.read()
    stylesheet = load_stylesheet("/Users/dedic-lab/source/repos/maxblack29/DetControl/Combinear.qss")
    #stylesheet = load_stylesheet("/Users/maxbl/OneDrive - University of Virginia/DetControl/Combinear.qss")
    #for lab computer, use: stylesheet = load_stylesheet("/Users/dedic-lab/source/repos/maxblack29/DetControl/Combinear.qss")
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec())