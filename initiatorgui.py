import sys
from PySide6.QtWidgets import QApplication, QDialog, QLabel
from PySide6.QtCore import QTimer, QThread, Signal, QObject
from combustionchamber import Ui_Dialog
import combustionchamber
from PySide6.QtCore import QTimer
from initiatortesting import Ui_Initiatorgui
import initiatortesting
from plumbingdiagram import Ui_plumbingdiagram
from greenledwidget import GreenLed
import nidaqmx #might not be needed since I imported nicontrol
import nicontrol
from nicontrol import set_digital_output
from nidaqmx.constants import AcquisitionType, READ_ALL_AVAILABLE
import alicatcontrol
import asyncio
import diagram_rc
#import dataacquisition
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import initiator
from initiator import test_initiator

import pdb
import pyqtgraph as pg
import matplotlib.pyplot as plt

'''This calls the python file that was created FROM the .ui file (combustionchamber.py). 
When updating gui in qt designer, must update the PYTHON file to see the updates.'''


class AutomationWorker(QObject):
    finished = Signal()
    def __init__(self, setpointA, setpointB, setpointC):
        super().__init__()
        self.setpointA = setpointA
        self.setpointB = setpointB
        self.setpointC = setpointC

    def run(self):
        import initiator
        asyncio.run(initiator.test_initiator(self.setpointA, self.setpointB, self.setpointC))
        self.finished.emit()

class StandardPurgeWorker(QObject):
    finished = Signal()
    def run(self):
        import initiator
        asyncio.run(initiator.stanpurge())
        self.finished.emit()

class EmergencyPurgeWorker(QObject):
    finished = Signal()
    def run(self):
        import initiator
        asyncio.run(initiator.emerpurge())
        self.finished.emit()


class MyDialog(QDialog):
    def __init__(self, plumbing_diagram):
        super().__init__()
        self.ui = Ui_Initiatorgui()
        self.ui.setupUi(self)
        self.plumbing_diagram = plumbing_diagram
        
        self.solenoids = [False, False, False, False, False, False, False, False] #Sets a bool array for 8 channels, last channel is empty
       

        #Connect each open and close button
        self.ui.openS1.clicked.connect(lambda: self.toggle_solenoid(0,True))
        self.ui.closeS1.clicked.connect(lambda: self.toggle_solenoid(0, False))
        self.ui.openS2.clicked.connect(lambda: self.toggle_solenoid(1, True))
        self.ui.closeS2.clicked.connect(lambda: self.toggle_solenoid(1, False))

        #Connects the update setpoints button
        self.ui.updatesetpoints.clicked.connect(self.save_setpoints)

        #Connects the reset flow button 
        self.ui.resetmfc.clicked.connect(self.reset_flow) #Might not need this

        #Retrieves the gas setpoints from the GUI 
        self.ui.mfcAsetpoint.returnPressed.connect(lambda: self.save_setpoints('A', float(self.ui.mfcAsetpoint.text())))
        self.ui.mfcBsetpoint.returnPressed.connect(lambda: self.save_setpoints('B', float(self.ui.mfcBsetpoint.text())))
        self.ui.mfcCsetpoint.returnPressed.connect(lambda: self.choosegas('C', float(self.ui.mfcCsetpoint.text())))
        
        #Retrieves the gas type from the GUI
        self.ui.mfcAgas.currentTextChanged.connect(self.change_gas)
        self.ui.mfcBgas.currentTextChanged.connect(self.change_gas)
        self.ui.mfcCgas.currentTextChanged.connect(self.change_gas)

        #Connects the automation and purge buttons
        self.ui.testautomation.clicked.connect(self.auto_purge)
        self.ui.emergencypurge.clicked.connect(self.auto_purge)
        self.ui.standardpurge.clicked.connect(self.auto_purge)
    
    def save_setpoints(self):
        #This function can be used to update the setpoints
        reset_button = self.ui.resetmfc
        set_flow_button = self.ui.updatesetpoints

        if set_flow_button.isEnabled():
            set_flow_button.setStyleSheet("background-color: green; color: white;")
        
            reset_button.setStyleSheet("")

        QTimer.singleShot(500, lambda:set_flow_button.setStyleSheet(""))

        self.ui.mfcAsetpoint.text()
        self.ui.mfcBsetpoint.text()
        self.ui.mfcCsetpoint.text()

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
        asyncio.run(alicatcontrol.change_rate('A', 0.0))
        asyncio.run(alicatcontrol.change_rate('B', 0.0))
        asyncio.run(alicatcontrol.change_rate('C', 0.0))
        print("All gas setpoints reset to 0.0 SLPM.")
    

    #Figure out how to do a change_gas function
    def change_gas(self):
        #This function will change the gas type for each controller
        self.ui.mfcAgas.currentText()
        self.ui.mfcBgas.currentText()
        self.ui.mfcCgas.currentText()
        asyncio.run(alicatcontrol.set_gas('A', self.ui.mfcAgas.currentText()))
        asyncio.run(alicatcontrol.set_gas('B', self.ui.mfcBgas.currentText()))
        asyncio.run(alicatcontrol.set_gas('C', self.ui.mfcCgas.currentText()))

    #Toggles the solenoid states based on button clicks from the GUI. Will highlight the active state green based on user input.
    def toggle_solenoid(self, index, state):
        self.solenoids[index] = state
        open_button = getattr(self.ui, f"openS{index+1}")
        close_button = getattr(self.ui, f"closeS{index+1}")

        if state:
            open_button.setStyleSheet("background-color: green; color: white;")
            QTimer.singleShot(500, lambda: open_button.setStyleSheet(""))
            if open_button.isEnabled():
                close_button.setStyleSheet("")
        else:
            open_button.setStyleSheet("")
            close_button.setStyleSheet("background-color: green; color: white;")
            QTimer.singleShot(500, lambda: close_button.setStyleSheet(""))

        #Control the LED state for each solenoid    
        if 0 <= index < 7:  # Only 7 LEDs
            self.plumbing_diagram.set_solenoid_led(index, state)
        
        nicontrol.set_digital_output(self.solenoids) #commented out until I can test it with lab computer
        print(f"Solenoid S{index+1} {'opened' if state else 'closed'}.")

    #This function will eventually handle the automation of the purge sequence, testing, and emergency purge sequence
    def auto_purge(self):
        pressed_button = self.sender()

        pressed_button.setEnabled(False)
        #pressed_button.clicked.disconnect(self.auto_purge)
        #pressed_button.setStyleSheet("background-color: orange; color: white;")
        self.ui.testautomation.setStyleSheet("")
        self.ui.emergencypurge.setStyleSheet("")
        self.ui.standardpurge.setStyleSheet("")
        
        if pressed_button == self.ui.testautomation:
            setpointA = float(self.ui.mfcAsetpoint.text())
            setpointB = float(self.ui.mfcBsetpoint.text())
            setpointC = float(self.ui.mfcCsetpoint.text())

            self.worker = AutomationWorker(setpointA, setpointB, setpointC)
            self.thread = QThread()
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            #self.worker.finished.connect(lambda: pressed_button.setStyleSheet(""))
            self.worker.finished.connect(lambda: self.reenable(pressed_button))
            self.thread.start()
        elif pressed_button == self.ui.emergencypurge:
            self.eme_worker = EmergencyPurgeWorker()
            self.eme_thread = QThread()
            self.eme_worker.moveToThread(self.eme_thread)
            self.eme_thread.started.connect(self.eme_worker.run)
            self.eme_worker.finished.connect(self.eme_thread.quit)
            self.eme_worker.finished.connect(lambda: self.reenable(pressed_button))
            self.eme_thread.start()

        else:
            self.std_worker = StandardPurgeWorker()
            self.std_thread = QThread()
            self.std_worker.moveToThread(self.std_thread)
            self.std_thread.started.connect(self.std_worker.run)
            self.std_worker.finished.connect(self.std_thread.quit)
            self.std_worker.finished.connect(lambda: self.reenable(pressed_button))
            self.std_thread.start()
    def reenable(self, button):
        button.setEnabled(True)
        button.setStyleSheet("")
        '''
        def data_acquisition(self):
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan("cDAQ9188-169338EMod6/port0/ai0", min_val = -10, max_val = 10)
            task.timing.cfg_samp_clk_timing(1000, sample_mode= AcquisitionType.FINITE, samps_per_chan=1000)
            data = task.read(READ_ALL_AVAILABLE)
            #fig = Figure(figsize=(4,4))
            #ax = fig.add_subplot()
            #ax.plot(data)
        '''


class PlumbingDiagram(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_plumbingdiagram()
        self.ui.setupUi(self)

        solenoid_positions = [
        (215, 415),  # S1
        (407, 218),  # S2
        (560, 473),  # S3
        (895, 607),  # S4
        (1000, 392),  # S5
        (813, 161),  # S6
        (997, 150),  # S7
        ]

        self.leds = []
        for i, (x, y) in enumerate(solenoid_positions):
            led = GreenLed(self, diameter=20)
            led.move(x, y)
            led.show()
            self.leds.append(led)
            if i == 3:
                led.turn_on()
            if i == 5:
                led.turn_on()

        self.led_open = GreenLed(self, diameter=22)
        self.led_open.move(1185, 450)  # Adjust position as needed
        self.led_open.turn_on()
        self.led_open.show()

        # Red (Closed)
        self.led_closed = GreenLed(self, diameter=22)
        self.led_closed.move(1185,495)  # Adjust position as needed
        self.led_closed.turn_off()
        self.led_closed.show()

    def set_solenoid_led(self, index, on):
        if 0 <= index < len(self.leds):
            if on:
                self.leds[index].turn_on()
            else:
                self.leds[index].turn_off()
        
if __name__ == "__main__":
    def load_stylesheet(filename):
        with open(filename, "r") as f:
            return f.read()
    #stylesheet = load_stylesheet("/Users/dedic-lab/source/repos/maxblack29/DetControl/Combinear.qss")
    stylesheet = load_stylesheet("/Users/maxbl/OneDrive - University of Virginia/DetControl/Combinear.qss")
    #for lab computer, use: stylesheet = load_stylesheet("/Users/dedic-lab/source/repos/maxblack29/DetControl/Combinear.qss")
    #for personal computer, use: stylesheet = load_stylesheet("/Users/maxbl/OneDrive - University of Virginia/DetControl/Combinear.qss")
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    dialog2 = PlumbingDiagram()
    dialog = MyDialog(dialog2)
    dialog.show()
    dialog2.show()
    sys.exit(app.exec())