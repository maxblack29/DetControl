import sys
from PySide6.QtWidgets import QApplication, QDialog, QLabel
from PySide6.QtCore import QTimer
from combustionchamber import Ui_Dialog
import combustionchamber
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


import pdb
import pyqtgraph as pg
import matplotlib.pyplot as plt

'''This calls the python file that was created FROM the .ui file (combustionchamber.py). 
When updating gui in qt designer, must update the PYTHON file to see the updates.'''


class MyDialog(QDialog):
    def __init__(self, plumbing_diagram):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.plumbing_diagram = plumbing_diagram
        
        self.solenoids = [False, False, False, False, False, False, False, False] #Sets a bool array for 8 channels, last channel is empty
        '''
        fig = Figure(figsize=(4,4))
        canvas = FigureCanvas(fig)
        self.plot_layout = QVBoxLayout(self.ui.plotWidget)
        self.plot_layout.addWidget(canvas)
        '''
        self.xx = np.linspace(0, 2*np.pi, 100)
        self.yy = np.sin(self.xx)
        self.ui.test_plot.clear()
        self.ui.test_plot.setBackground('w')
        #self.curve = pg.PlotCurveItem(self.xx, self.yy, pen='g')
        self.curve = pg.PlotDataItem()
        pen = pg.mkPen(color='r', width=2)
        self.curve.setData(self.xx, self.yy, pen=pen)
        self.ui.test_plot.addItem(self.curve)
        self.ui.test_plot.getViewBox().autoRange()
   
        #self.ui.test_plot.getPlotItem.draw()
        #self.ui.test_plot.show()
        #self.ui.test_plot.update()
       
     
        #self.ui.test_plot.fig.show()

        #Connect each open and close button
        self.ui.openS1.clicked.connect(lambda: self.toggle_solenoid(0,True))
        self.ui.closeS1.clicked.connect(lambda: self.toggle_solenoid(0, False))
        self.ui.openS2.clicked.connect(lambda: self.toggle_solenoid(1, True))
        self.ui.closeS2.clicked.connect(lambda: self.toggle_solenoid(1, False))
        self.ui.openS3.clicked.connect(lambda: self.toggle_solenoid(2, True))
        self.ui.closeS3.clicked.connect(lambda: self.toggle_solenoid(2, False))
        self.ui.openS4.clicked.connect(lambda: self.toggle_solenoid(3, True))
        self.ui.closeS4.clicked.connect(lambda: self.toggle_solenoid(3, False))
        self.ui.openS5.clicked.connect(lambda: self.toggle_solenoid(4,True))
        self.ui.closeS5.clicked.connect(lambda: self.toggle_solenoid(4, False))
        self.ui.openS6.clicked.connect(lambda: self.toggle_solenoid(5, True))
        self.ui.closeS6.clicked.connect(lambda: self.toggle_solenoid(5, False)) 
        self.ui.openS7.clicked.connect(lambda: self.toggle_solenoid(6, True))
        self.ui.closeS7.clicked.connect(lambda: self.toggle_solenoid(6, False))

        #Connects the update setpoints button
        self.ui.updatesetpoints.clicked.connect(self.update_setpoints)

        #Connects the reset flow button 
        self.ui.resetmfc.clicked.connect(self.reset_flow)

        #Retrieves the gas setpoints from the GUI 
        self.ui.mfcAsetpoint.returnPressed.connect(lambda: self.choosegas('A', float(self.ui.mfcAsetpoint.text())))
        self.ui.mfcBsetpoint.returnPressed.connect(lambda: self.choosegas('B', float(self.ui.mfcBsetpoint.text())))
        self.ui.mfcCsetpoint.returnPressed.connect(lambda: self.choosegas('C', float(self.ui.mfcCsetpoint.text())))
        self.ui.mfcDsetpoint.returnPressed.connect(lambda: self.choosegas('D', float(self.ui.mfcDsetpoint.text())))
        
        #Retrieves the gas type from the GUI
        self.ui.mfcAgas.currentTextChanged.connect(self.change_gas)
        self.ui.mfcBgas.currentTextChanged.connect(self.change_gas)
        self.ui.mfcCgas.currentTextChanged.connect(self.change_gas)
        #self.ui.mfcDgas.currentTextChanged.connect(self.change_gas)

        #Connects the automation and purge buttons
        self.ui.testautomation.clicked.connect(self.auto_purge)
        self.ui.emergencypurge.clicked.connect(self.auto_purge)
        self.ui.standardpurge.clicked.connect(self.auto_purge)
    
    def update_setpoints(self):
        #This function can be used to update the setpoints

        reset_button = self.ui.resetmfc
        set_flow_button = self.ui.updatesetpoints

        #if set_flow_button.isEnabled():
            #print("This works.")
            #set_flow_button.setStyleSheet("background-color: green; color: white;")
            
            #reset_button.setStyleSheet("")

        QTimer.singleShot(500, lambda:set_flow_button.setStyleSheet(""))

        self.ui.mfcAsetpoint.text()
        asyncio.run(alicatcontrol.change_rate('A', float(self.ui.mfcAsetpoint.text())))
        self.ui.mfcBsetpoint.text()
        asyncio.run(alicatcontrol.change_rate('B', float(self.ui.mfcBsetpoint.text())))
        self.ui.mfcCsetpoint.text()
        asyncio.run(alicatcontrol.change_rate('C', float(self.ui.mfcCsetpoint.text())))
        self.ui.mfcDsetpoint.text()
        #asyncio.run(alicatcontrol.change_rate('D', float(self.ui.mfcDsetpoint.text())))
        #Commented out until mfc D is connected to alicat hub

        self.ui.updatesetpoints.clicked.connect(self.update_setpoints)

    #This function will reset the flow setpoints to 0.0 SLPM for all gas controllers. 
    def reset_flow(self):
        reset_button = self.ui.resetmfc
        set_flow_button = self.ui.updatesetpoints
        #if reset_button.isEnabled():
        #   reset_button.setStyleSheet("background-color: green; color: white;")
        #   set_flow_button.setStyleSheet("")

        QTimer.singleShot(500, lambda: reset_button.setStyleSheet(""))

        self.ui.mfcAsetpoint.setText("0.0")
        self.ui.mfcBsetpoint.setText("0.0")
        self.ui.mfcCsetpoint.setText("0.0")
        self.ui.mfcDsetpoint.setText("0.0")
        asyncio.run(alicatcontrol.change_rate('A', 0.0))
        asyncio.run(alicatcontrol.change_rate('B', 0.0))
        asyncio.run(alicatcontrol.change_rate('C', 0.0))
        #asyncio.run(alicatcontrol.change_rate('D', 0.0)) #Commented out until mfc D is connected to alicat hub
        print("All gas setpoints reset to 0.0 SLPM.")
    

    #Figure out how to do a change_gas function
    def change_gas(self):
        #This function will change the gas type for each controller
        self.ui.mfcAgas.currentText()
        self.ui.mfcBgas.currentText()
        self.ui.mfcCgas.currentText()
        #self.ui.mfcDgas.currentTextChanged()
        asyncio.run(alicatcontrol.set_gas('A', self.ui.mfcAgas.currentText()))
        asyncio.run(alicatcontrol.set_gas('B', self.ui.mfcBgas.currentText()))
        asyncio.run(alicatcontrol.set_gas('C', self.ui.mfcCgas.currentText()))
        #asyncio.run(alicatcontrol.change_gas('D', self.ui.mfcDgas.currentText())) #Commented out until mfc D is connected to alicat hub

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
        self.ui.testautomation.clicked.connect(self.auto_purge)
        self.ui.emergencypurge.clicked.connect(self.auto_purge)
        self.ui.standardpurge.clicked.connect(self.auto_purge)

        pressed_button = getattr(self.ui, self.sender().objectName())

        if pressed_button == self.ui.testautomation:
            pressed_button.setStyleSheet("background-color: green; color: white;")
            self.ui.emergencypurge.setStyleSheet("")
            self.ui.standardpurge.setStyleSheet("")
            QTimer.singleShot(500, lambda: pressed_button.setStyleSheet(""))
            #Will add the automation sequence here once we're ready
        elif pressed_button == self.ui.emergencypurge:
            pressed_button.setStyleSheet("background-color: green; color: white;")
            self.ui.testautomation.setStyleSheet("")
            self.ui.standardpurge.setStyleSheet("")
            QTimer.singleShot(500, lambda: pressed_button.setStyleSheet(""))
            #Will add the automation sequence here once we're ready
        else: 
            pressed_button.setStyleSheet("background-color: green; color: white;")
            self.ui.testautomation.setStyleSheet("")
            self.ui.emergencypurge.setStyleSheet("")
            QTimer.singleShot(500, lambda: pressed_button.setStyleSheet(""))
            #Will add the automation sequence here once we're ready

        #How can I get print statements to not loop?
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
    stylesheet = load_stylesheet("/Users/dedic-lab/source/repos/maxblack29/DetControl/Combinear.qss")
    #stylesheet = load_stylesheet("/Users/maxbl/OneDrive - University of Virginia/DetControl/Combinear.qss")
    #for lab computer, use: stylesheet = load_stylesheet("/Users/dedic-lab/source/repos/maxblack29/DetControl/Combinear.qss")
    #for personal computer, use: stylesheet = load_stylesheet("/Users/maxbl/OneDrive - University of Virginia/DetControl/Combinear.qss")
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    dialog2 = PlumbingDiagram()
    dialog = MyDialog(dialog2)
    dialog.show()
    dialog2.show()

    dialog.ui.test_plot.setXRange(0, 2*np.pi)
    dialog.ui.test_plot.setYRange(-1, 1)
    dialog.ui.test_plot.showGrid(True, True)
    dialog.curve.setData(dialog.xx, dialog.yy)
    #dialog.ui.test_plot.clear()
    #dialog.ui.test_plot.repaint()
    #dialog.ui.test_plot.update()
    #dialog.curve.setZValue(1000)
    #print(dialog.curve.isVisible())
    #data = dialog.curve.getData()
    #print(data[0])
    #print(data[1])
    #plt.plot(data[0], data[1])
    #plt.show()
    #dialog.ui.test_plot.update()
    #QApplication.processEvents()
    #dialog.curve.update()
    dialog.ui.test_plot.show()
    sys.exit(app.exec())