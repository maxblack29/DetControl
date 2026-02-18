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

import pdb
import pyqtgraph as pg
import matplotlib.pyplot as plt

from ui_full_facility_gui_script import Ui_full_facility_gui
'''This calls the python file that was created FROM the .ui file (ui_full_facility_gui_script.py). 
When updating gui in qt designer, must update the PYTHON file to see the updates.'''



class AutomationWorker(QObject):
    finished = Signal()
    fill_phase_complete = Signal()
    mfc_readouts_updated = Signal(float, float, float)

    def __init__(self, setpointA, setpointB, setpointC, setpointD, setpointC_driver):
        super().__init__()
        self.setpointA = setpointA
        self.setpointB = setpointB
        self.setpointC = setpointC
        self.setpointD = setpointD
        self.setpointC_driver = setpointC_driver

    def runauto(self):
        asyncio.run(full_facility_run_methods.automatic_test(
            self.setpointA, self.setpointB, self.setpointC, self.setpointD, self.setpointC_driver,
            on_fill_complete=self.fill_phase_complete.emit,
            on_mfc_setpoints_changed=self.mfc_readouts_updated.emit
        ))
        self.finished.emit()

    def runstanpurge(self):
        asyncio.run(full_facility_run_methods.purge(
            self.setpointA, self.setpointB, self.setpointC, self.setpointD,
            on_mfc_setpoints_changed=self.mfc_readouts_updated.emit
        ))
        self.finished.emit()


class SolenoidWorker(QObject):
    finished = Signal()
    def __init__(self, daq1, daq2, testcount, vacuum_pressure, post_fill_pressure):
        super().__init__()
        self.daq1 = daq1 
        self.daq2 = daq2 
        self.testcount = testcount
        self.vacuum_pressure = vacuum_pressure
        self.post_fill_pressure = post_fill_pressure

    def runsolenoid(self):
        nicontrol.set_digital_output(self.daq1)
        nicontrol.set_digital_output_2(self.daq2)
        self.finished.emit()
    
    def runignite(self):
        nicontrol.set_ignite_read_pressure(self.testcount, self.vacuum_pressure, self.post_fill_pressure) 
        self.finished.emit()




class MyDialog(QDialog):
    def __init__(self, plumbing_diagram=None):
        #MyDialog starts the GUI. this first secion is for initializing and connecting buttons. 
        super().__init__()
        self.ui = Ui_full_facility_gui()
        self.ui.setupUi(self)
        #self.plumbing_diagram = plumbing_diagram
        
        self.daq1 = [False, False, True, False, False, False, False, False] #Startup DAQ1 States
        nicontrol.set_digital_output(self.daq1) #Sets the digital output to the daq1

        self.daq2 = [True, True, False, False, False, False, False, False] #Startup DAQ2 States
        nicontrol.set_digital_output_2(self.daq2) #Sets the digital output to the daq2 

        self.testcount = 0 #zeroes the test count for data acquisition when gui is opened

        #Connect each open and close button
        self.ui.openS1.clicked.connect(lambda: self.toggle_solenoid(0, True))
        self.ui.closeS1.clicked.connect(lambda: self.toggle_solenoid(0, False))
        self.ui.openS2.clicked.connect(lambda: self.toggle_solenoid(1, True))
        self.ui.closeS2.clicked.connect(lambda: self.toggle_solenoid(1, False))
        self.ui.openS3.clicked.connect(lambda: self.toggle_solenoid(2, True))
        self.ui.closeS3.clicked.connect(lambda: self.toggle_solenoid(2,False))  
        self.ui.openS4.clicked.connect(lambda: self.toggle_solenoid(3, True))  
        self.ui.closeS4.clicked.connect(lambda: self.toggle_solenoid(3, False)) 
        self.ui.openS5.clicked.connect(lambda: self.toggle_solenoid(4, True))  
        self.ui.closeS5.clicked.connect(lambda: self.toggle_solenoid(4, False)) 


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

        self.vacuum_pressure = 0
        self.post_fill_pressure = 0
    
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
        #asyncio.run(alicatcontrol.change_rate('D', setpointD))
        
        #update last sent flow rates display
        self.ui.mfcAreadout.display(setpointA)
        self.ui.mfcBreadout.display(setpointB)
        self.ui.mfcCreadout.display(setpointC)

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
        #asyncio.run(alicatcontrol.change_rate('D', 0.0))

        #update last sent flow rates display
        self.ui.mfcAreadout.display("0.0")
        self.ui.mfcBreadout.display("0.0")
        self.ui.mfcCreadout.display("0.0")


        print("All gas setpoints reset to 0.0 SLPM.")
    


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
        # Update the correct DAQ based on the solenoid index
        if index == 3:  # S4 is now on daq2
            self.daq2[index - 3] = not state  # Invert state for S4 (Open -> False, Close -> True)
        elif index == 4:  #S5 is on DAQ2 port 1
            self.daq2[1] = state  
        elif index == 2:  # S3 is on daq1
            self.daq1[index] = not state  # Invert state for S3 (Open -> False, Close -> True)
        else:
            self.daq1[index] = state  # Directly update daq1 for other solenoids

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

        # Pass the updated DAQ states to the SolenoidWorker
        solenoid_worker = SolenoidWorker(self.daq1, self.daq2, self.testcount)
        solenoid_thread = QThread()
        solenoid_worker.moveToThread(solenoid_thread)
        solenoid_thread.started.connect(solenoid_worker.runsolenoid)
        solenoid_worker.finished.connect(solenoid_thread.quit)
        solenoid_worker.finished.connect(lambda: self.reenable(open_button))
        solenoid_worker.finished.connect(lambda: self.reenable(close_button))

        # Keep the worker alive so it's not garbage collected while running
        if not hasattr(self, "_solenoid_threads"):
            self._solenoid_threads = []
        self._solenoid_threads.append((solenoid_thread, solenoid_worker))

        solenoid_thread.start()

        # Print the state of the solenoid
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


        self.testcount+=1

        # Update vacuum gauge once when automatic test starts
        self.update_vacuum_pressure()

        #Michael change: now gives automation its own worker/thread
        automation_worker = AutomationWorker(setpointA, setpointB, setpointC, setpointD, setpointC2)
        automation_thread = QThread()
        automation_worker.moveToThread(automation_thread)
        automation_thread.started.connect(automation_worker.runauto)
        automation_worker.finished.connect(automation_thread.quit)
        automation_worker.finished.connect(lambda: self.reenable(button))
        automation_worker.fill_phase_complete.connect(self.update_pressure)
        automation_worker.mfc_readouts_updated.connect(self.update_mfc_readouts)

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

        testcount = self.testcount 
        ignite_worker = SolenoidWorker(testcount, vacuum_pressure, )
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
        purge_worker.mfc_readouts_updated.connect(self.update_mfc_readouts)

        # keep a reference so it's not garbage collected and prematurely closed 
        if not hasattr(self, "_automation_threads"):
            self._automation_threads = []
        self._automation_threads.append((purge_thread, purge_worker))

        purge_thread.start()

    def reenable(self, button):
        button.setEnabled(True)
        button.setStyleSheet("")

    #is run at end of fill phase
    def update_pressure(self):
        pressure = nicontrol.read_pressure()
        self.ui.pressure_readout.display(pressure)

    #is run at start of automatic test
    def update_vacuum_pressure(self):
        vacuum_pressure = nicontrol.read_vacuum_pressure()
        self.ui.vacuum_pressure_readout.display(vacuum_pressure)

    def update_mfc_readouts(self, setpoint_a, setpoint_b, setpoint_c):
        """Update MFC A/B/C readout displays (e.g. when setpoints change in automatic test or purge)."""
        self.ui.mfcAreadout.display(setpoint_a)
        self.ui.mfcBreadout.display(setpoint_b)
        self.ui.mfcCreadout.display(setpoint_c)



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