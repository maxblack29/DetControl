import sys
from PySide6.QtWidgets import QApplication, QDialog
from combustionchamber import Ui_Dialog
import nidaqmx #might not be needed since I imported nicontrol
import nicontrol
from nicontrol import set_digital_output
import alicatcontrol
import asyncio

'''This calls the python file that was created FROM the .ui file (combustionchamber.py). 
When updating gui in qt designer, must update the PYTHON file to see the updates.'''


class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.solenoids = [False]*8 #Sets a bool array for 8 channels, last channel is empty

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

        #Retrieves the gas setpoints from the GUI 
        self.ui.mfcAsetpoint.returnPressed.connect(lambda: self.choosegas('A', float(self.ui.mfcAsetpoint.text())))
        self.ui.mfcBsetpoint.returnPressed.connect(lambda: self.choosegas('B', float(self.ui.mfcBsetpoint.text())))
        self.ui.mfcCsetpoint.returnPressed.connect(lambda: self.choosegas('C', float(self.ui.mfcCsetpoint.text())))
        self.ui.mfcDsetpoint.returnPressed.connect(lambda: self.choosegas('D', float(self.ui.mfcDsetpoint.text())))
        #Retrieving the gas setpoints from the GUI

        #Connects the automation and purge buttons
        self.ui.begintesting.clicked.connect(self.auto_purge)
        self.ui.emergencypurge.clicked.connect(self.auto_purge)
        self.ui.standardpurge.clicked.connect(self.auto_purge)
    
    def update_setpoints(self):
        #This function can be used to update the setpoints
        self.ui.mfcAsetpoint.text()
        #asyncio.run(alicatcontrol.change_rate('A', float(self.ui.mfcAsetpoint.text())))
        print(f"Controller A set to {self.ui.mfcAsetpoint.text()} SLPM.")
        self.ui.mfcBsetpoint.text()
        #asyncio.run(alicatcontrol.change_rate('B', float(self.ui.mfcAsetpoint.text())))
        print(f"Controller B set to {self.ui.mfcBsetpoint.text()} SLPM.")
        self.ui.mfcCsetpoint.text()
        #asyncio.run(alicatcontrol.change_rate('C', float(self.ui.mfcAsetpoint.text())))
        print(f"Controller C set to {self.ui.mfcCsetpoint.text()} SLPM.")
        self.ui.mfcDsetpoint.text()
        #asyncio.run(alicatcontrol.change_rate('D', float(self.ui.mfcAsetpoint.text())))
        #Commented out until mfc D is connected to alicat hub
        print(f"Controller D set to {self.ui.mfcDsetpoint.text()} SLPM.")

        self.ui.updatesetpoints.clicked.connect(self.update_setpoints)

        #Troubleshoot/look with Aldo. How can you get these print statements not to loop for x amount of setpoint changes?
        #Not the most important thing, just for troubleshooting purposes. This will also be weird with the alicat stuff

    #This function will reset the flow setpoints to 0.0 SLPM for all gas controllers. 
    def reset_flow(self):

        reset_button = self.ui.resetmfc.clicked.connect(self.reset_flow)
        if reset_button.isEnabled():
            reset_button.setStyleSheet("background-color: green; color: white;")

        self.ui.mfcAsetpoint.setText("0.0")
        self.ui.mfcBsetpoint.setText("0.0")
        self.ui.mfcCsetpoint.setText("0.0")
        self.ui.mfcDsetpoint.setText("0.0")
        asyncio.run(alicatcontrol.change_rate('A', 0.0))
        asyncio.run(alicatcontrol.change_rate('B', 0.0))
        asyncio.run(alicatcontrol.change_rate('C', 0.0))
        #asyncio.run(alicatcontrol.change_rate('D', 0.0)) #Commented out until mfc D is connected to alicat hub
        print("All gas setpoints reset to 0.0 SLPM.")

    #Toggles the solenoid states based on button clicks from the GUI. Will highlight the active state green based on user input.
    def toggle_solenoid(self, index, state):
        self.solenoids[index] = state
        open_button = getattr(self.ui, f"openS{index+1}")
        close_button = getattr(self.ui, f"closeS{index+1}")

        if state:
            open_button.setStyleSheet("background-color: green; color: white;")
            if open_button.isEnabled():
                close_button.setStyleSheet("")
        else:
            open_button.setStyleSheet("")
            close_button.setStyleSheet("background-color: green; color: white;")
        #nicontrol.set_digital_output(self.solenoids) #commented out until I can test it with lab computer
        print(f"Solenoid S{index+1} {'opened' if state else 'closed'}.")

    def auto_purge(self):
        self.ui.begintesting.clicked.connect(self.auto_purge)
        self.ui.emergencypurge.clicked.connect(self.auto_purge)
        self.ui.standardpurge.clicked.connect(self.auto_purge)

        pressed_button = getattr(self.ui, self.sender().objectName())

        if pressed_button == self.ui.begintesting:
            pressed_button.setStyleSheet("background-color: green; color: white;")
            if pressed_button.isEnabled():
                self.ui.emergencypurge.setStyleSheet("")
                self.ui.standardpurge.setStyleSheet("")
            print("Beginning testing sequence...")
            #Will add the automation sequence here once we're ready
        elif pressed_button == self.ui.emergencypurge:
            pressed_button.setStyleSheet("background-color: green; color: white;")
            if pressed_button.isEnabled():
                self.ui.begintesting.setStyleSheet("")
                self.ui.standardpurge.setStyleSheet("")
            print("Emergency purge sequence initiated")
            #Will add the automation sequence here once we're ready
        else: 
            pressed_button.setStyleSheet("background-color: green; color: white;")
            if pressed_button.isEnabled():
                self.ui.begintesting.setStyleSheet("")
                self.ui.emergencypurge.setStyleSheet("")
            print("Standard purge sequence initiated")
            #Will add the automation sequence here once we're ready

        #How can I get print statements to not loop?
            

if __name__ == "__main__":
    def load_stylesheet(filename):
        with open(filename, "r") as f:
            return f.read()
    stylesheet = load_stylesheet("/Users/maxbl/OneDrive - University of Virginia/Reacting Flow Git/Combinear.qss")
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec())