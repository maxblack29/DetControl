import sys
from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtCore import QTimer, QThread, Signal, QObject
import full_facility_run_methods
import bnc_box_control
import nidaqmx  # might not be needed since I imported nicontrol
import nicontrol
from nidaqmx.constants import AcquisitionType, READ_ALL_AVAILABLE
import alicatcontrol
import klinger_control
import asyncio
#import dataacquisition
import numpy as np
import threading
import time

import audio_player
# import win32gui
# import win32console

from ui_full_facility_gui_script import Ui_full_facility_gui
'''This calls the python file that was created FROM the .ui file (ui_full_facility_gui_script.py). 
When updating gui in qt designer, must update the PYTHON file to see the updates.'''

# Same numeric units as self.vacuum_pressure / vacuum_pressure_readout (see update_vacuum_pressure).
VACUUM_AUDIO_THRESHOLD_PA = 0.5
VACUUM_AUDIO_INTERVAL_S = 30.0


# GUI S1–S10 → (which_daq: 1=Mod1 / 2=Mod2, channel 0–7, invert_line_for_normally_open).
SOLENOID_GUI_MAP = [
    (1, 1, False),  # S1 driver fuel
    (1, 0, False),  # S2 driver fuel mix
    (1, 2, False),  # S3 driver ox
    (1, 4, False),  # S4 driver ox mix
    (1, 3, False),  # S5 reactant mix
    (1, 6, True),   # S6 purge NO
    (2, 0, True),   # S7 exhaust NO
    (2, 1, False),  # S8 gauge cluster
    (1, 5, False),  # S9 vacuum valve
    (2, 3, False),  # S10 vacuum pump
]


def _solenoid_line_seems_open(line_high, invert):
    """High DAQ line vs logical OPEN for status labels (matches toggle_solenoid)."""
    return (not line_high) if invert else bool(line_high)

# def set_console_position(x, y, width, height):
#     # Get the handle of the current console window
#     hwnd = win32console.GetConsoleWindow()
    
#     if hwnd:
#         # MoveWindow(handle, x, y, width, height, repaint_boolean)
#         win32gui.MoveWindow(hwnd, x, y, width, height, True)
        
#background MFC monitor (Serial)
class MFCMonitorWorker(QObject):
    flows_updated = Signal(float, float, float)
 
    def __init__(self, interval_ms=100):
        super().__init__()
        self.interval_s = interval_ms / 1000.0
        self._running = True
        self._paused = False
 
    def stop(self):
        self._running = False
 
    def pause(self):
        self._paused = True
 
    def resume(self):
        self._paused = False
 
    def run(self):
        while self._running:
            if not self._paused:
                try:
                    flows = alicatcontrol.get_manager().read_flows()
                    a = flows.get("A", 0.0)
                    b = flows.get("B", 0.0)
                    c = flows.get("C", 0.0)
                    self.flows_updated.emit(a, b, c)
 
                except Exception:
                    pass
            time.sleep(self.interval_s)

class AutomationWorker(QObject):
    finished = Signal()
    fill_phase_complete = Signal()
    mfc_readouts_updated = Signal(float, float, float, float)

    def __init__(self, setpointA, setpointB, setpointC, setpointD, setpointC_driver, fill_time_s, testcount=None):
        super().__init__()
        self.setpointA = setpointA
        self.setpointB = setpointB
        self.setpointC = setpointC
        self.setpointD = setpointD
        self.setpointC_driver = setpointC_driver
        self.fill_time_s = fill_time_s
        self.testcount = testcount

    def runauto(self):
        asyncio.run(full_facility_run_methods.automatic_test(
            self.setpointA, self.setpointB, self.setpointC, self.setpointD, self.setpointC_driver,
            on_fill_complete=self.fill_phase_complete.emit,
            on_mfc_setpoints_changed=self.mfc_readouts_updated.emit,
            fill_time_s=self.fill_time_s,
            testcount=self.testcount,
        ))
        self.finished.emit()

    def runstanpurge(self):
        asyncio.run(full_facility_run_methods.purge(
            self.setpointA, self.setpointB, self.setpointC, self.setpointD,
            on_mfc_setpoints_changed=self.mfc_readouts_updated.emit
        ))
        self.finished.emit()


class DriverWorker(QObject):
    finished = Signal()
    fill_phase_complete = Signal()
    mfc_readouts_updated = Signal(float, float, float, float)

    def __init__(
        self,
        setpointA,
        setpointB,
        setpointC,
        setpointD,
        setpointC_driver,
        fill_time_s,
        testcount,
        driver_fill_time_s,
    ):
        super().__init__()
        self.setpointA = setpointA
        self.setpointB = setpointB
        self.setpointC = setpointC
        self.setpointD = setpointD
        self.setpointC_driver = setpointC_driver
        self.fill_time_s = fill_time_s
        self.testcount = testcount
        self.driver_fill_time_s = driver_fill_time_s

    def run(self):
        asyncio.run(
            full_facility_run_methods.fill_and_driver_sequence(
                self.setpointA,
                self.setpointB,
                self.setpointC,
                self.setpointD,
                self.setpointC_driver,
                fill_time_s=self.fill_time_s,
                testcount=self.testcount,
                driver_fill_time_s=self.driver_fill_time_s,
                on_fill_complete=self.fill_phase_complete.emit,
                on_mfc_setpoints_changed=self.mfc_readouts_updated.emit,
            )
        )
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
        klinger_control.move_to_zero()
        self.finished.emit()




class MyDialog(QDialog):



    def __init__(self, plumbing_diagram=None):
        #MyDialog starts the GUI. this first section is for initializing and connecting buttons. 
        super().__init__()
        self.ui = Ui_full_facility_gui()
        self.ui.setupUi(self)
        #self.plumbing_diagram = plumbing_diagram
        
        # DAQ line map: full_facility_run_methods + nicontrol (Mod2 lines 6–7 = timing / speaker).
        self.daq1 = list(full_facility_run_methods.PURGE_COMPLETE_DAQ1)
        nicontrol.set_digital_output(self.daq1)

        self.daq2 = list(full_facility_run_methods.PURGE_COMPLETE_DAQ2)
        nicontrol.set_digital_output_2(self.daq2)


        # Ensures BNC box is in continuous mode and armed on GUI startup; labels track last commands.
        try:
            bnc_box_control.switch_preset(9)
            bnc_box_control.arm("ON")
            self.ui.bnc_arm_state.setText("ON")
            self.ui.bnc_mode_state.setText("Continuous")
        except Exception as e:
            print("BNC box startup (preset 9 / arm ON) failed:", e)

        self.testcount = 0  # zeroes the test count for data acquisition when gui is opened
        self.automation_running = False
        self.purge_running = False
        self.pressure_timer = None
        self.vacuum_pressure_timer = None
        self._vacuum_audio_next_mono = None  # next 30 s slot from start_auto_read (wall schedule)
        self._solenoid_threads = []
        self._automation_threads = []
        self._driver_threads = []
        self._ignite_threads = []

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
        self.ui.openS6.clicked.connect(lambda: self.toggle_solenoid(5, True))
        self.ui.closeS6.clicked.connect(lambda: self.toggle_solenoid(5, False))
        self.ui.openS7.clicked.connect(lambda: self.toggle_solenoid(6, True))
        self.ui.closeS7.clicked.connect(lambda: self.toggle_solenoid(6, False))
        self.ui.openS8.clicked.connect(lambda: self.toggle_solenoid(7, True))
        self.ui.closeS8.clicked.connect(lambda: self.toggle_solenoid(7, False))
        self.ui.openS9.clicked.connect(lambda: self.toggle_solenoid(8, True))
        self.ui.closeS9.clicked.connect(lambda: self.toggle_solenoid(8, False))
        self.ui.openS10.clicked.connect(lambda: self.toggle_solenoid(9, True))
        self.ui.closeS10.clicked.connect(lambda: self.toggle_solenoid(9, False))

        #Connects the update setpoints button (lambda avoids QAbstractButton.clicked(bool) extra arg).
        self.ui.updatesetpoints.clicked.connect(lambda: self.save_setpoints())

        #Connects the reset flow button 
        self.ui.resetmfc.clicked.connect(self.reset_flow) #Might not need this

        #Retrieves the gas type from the GUI
        self.ui.mfcAgas.currentTextChanged.connect(self.change_gas)
        self.ui.mfcBgas.currentTextChanged.connect(self.change_gas)
        self.ui.mfcCgas.currentTextChanged.connect(self.change_gas)
        self.ui.mfcDgas.currentTextChanged.connect(self.change_gas)

        #Connects the automation and purge buttons
        self.ui.testautomation.clicked.connect(self.begin_testing)
        self.ui.purgebutton.clicked.connect(self.purge)
        self.ui.igniteButton.clicked.connect(self.ignite)
        self.ui.driverButton.clicked.connect(self.begin_driver_sequence)

        self.ui.begin_vacuum.clicked.connect(self.begin_vacuum_down)

        self.ui.bnc_arm_on.clicked.connect(self._bnc_gui_arm_on)
        self.ui.bnc_arm_off.clicked.connect(self._bnc_gui_arm_off)
        self.ui.bnc_continuous_mode.clicked.connect(self._bnc_gui_continuous_mode)
        self.ui.bnc_single_mode.clicked.connect(self._bnc_gui_single_mode)

        # Pressure auto-read controls (vacuum phase helper)
        self.ui.start_auto_read.clicked.connect(self.start_auto_read)
        self.ui.stop_auto_read.clicked.connect(self.stop_auto_read)

        self.vacuum_pressure = 0
        self.post_fill_pressure = 0
        self.ui.test_num_readout.setText("0")

        # Start persistent MFC manager (one COM connection per controller, kept open).
        try:
            alicatcontrol.start_manager()
        except Exception as e:
            print("MFC manager failed to start (check COM3 / Alicat):", e)

        #background MFC monitor (Serial)
        self.mfc_monitor_worker = MFCMonitorWorker(interval_ms=1000)
        self.mfc_monitor_thread = QThread()
        self.mfc_monitor_worker.moveToThread(self.mfc_monitor_thread)
        self.mfc_monitor_worker.flows_updated.connect(self.update_mfc_flow_readouts)
        self.mfc_monitor_thread.started.connect(self.mfc_monitor_worker.run)
        self.mfc_monitor_thread.start()

        # Periodically refresh solenoid status labels from last DAQ states
        self.solenoid_label_timer = QTimer(self)
        self.solenoid_label_timer.timeout.connect(self.update_solenoid_labels)
        self.solenoid_label_timer.start(500)
        self.update_solenoid_labels()

        try:
            self.update_mfc_readouts(
                float(self.ui.mfcAsetpoint.text()),
                float(self.ui.mfcBsetpoint.text()),
                float(self.ui.mfcCsetpoint.text()),
                float(self.ui.mfcDsetpoint.text()),
            )
        except ValueError:
            pass

    
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

        # Set MFC setpoints via analog output (Mod7 ao0:3).
        nicontrol.set_mfc_setpoints_analog(setpointA, setpointB, setpointC, setpointD)
        self.update_mfc_readouts(setpointA, setpointB, setpointC, setpointD)

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
        self.ui.mfcCsetpoint_2.setText("0.0")

        nicontrol.set_mfc_setpoints_analog(0.0, 0.0, 0.0, 0.0)
        self.update_mfc_readouts(0.0, 0.0, 0.0, 0.0)
        self.update_vacuum_pressure()
        self.update_pressure()

        print("All gas setpoints reset to 0.0 SLPM.")
    

    def change_gas(self):
        # Each combo is connected to this slot; only update the MFC whose combo changed.
        # Serial commands only go to units listed in alicatcontrol.UNITS (e.g. ["B"] while A/C are off).
        combo = self.sender()
        manager = alicatcontrol.get_manager()
        U = alicatcontrol.UNITS
        if combo is self.ui.mfcAgas and "A" in U:
            manager.set_gas("A", self.ui.mfcAgas.currentText())
        elif combo is self.ui.mfcBgas and "B" in U:
            manager.set_gas("B", self.ui.mfcBgas.currentText())
        elif combo is self.ui.mfcCgas and "C" in U:
            manager.set_gas("C", self.ui.mfcCgas.currentText())
        elif combo is self.ui.mfcDgas and "D" in U:
            manager.set_gas("D", self.ui.mfcDgas.currentText())

    #Toggles the solenoid states based on button clicks from the GUI. Will highlight the active state green based on user input.
    def toggle_solenoid(self, index, state):
        # Sync local DAQ state with the last values actually written by nicontrol,
        # so we don't revert all lines to startup states when changing one solenoid
        try:
            daq1, daq2 = nicontrol.get_daq_states()
            daq1 = (daq1 + [False] * 8)[:8]
            daq2 = (daq2 + [False] * 8)[:8]
            self.daq1, self.daq2 = daq1, daq2
        except Exception:
            pass

        if index < 0 or index >= len(SOLENOID_GUI_MAP):
            print(f"Solenoid index {index} out of range.")
            return
        board, ch, invert = SOLENOID_GUI_MAP[index]
        wire = (not state) if invert else state
        if board == 1:
            self.daq1[ch] = wire
        else:
            self.daq2[ch] = wire

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
        solenoid_worker = SolenoidWorker(self.daq1, self.daq2, self.testcount, 0, 0)
        solenoid_thread = QThread()
        solenoid_worker.moveToThread(solenoid_thread)
        solenoid_thread.started.connect(solenoid_worker.runsolenoid)
        solenoid_worker.finished.connect(solenoid_thread.quit)
        solenoid_worker.finished.connect(lambda: self.reenable(open_button))
        solenoid_worker.finished.connect(lambda: self.reenable(close_button))

        self._solenoid_threads.append((solenoid_thread, solenoid_worker))

        solenoid_thread.start()

        # Print the state of the solenoid
        print(f"Solenoid S{index+1} {'Open' if state else 'Closed'}.")

    def update_solenoid_labels(self):
        """Update solenoid status labels from last DAQ states (see nicontrol line map)."""
        try:
            daq1, daq2 = nicontrol.get_daq_states()
        except AttributeError:
            daq1, daq2 = self.daq1, self.daq2

        daq1 = (daq1 + [False] * 8)[:8]
        daq2 = (daq2 + [False] * 8)[:8]

        s_open = [
            _solenoid_line_seems_open(daq1[1], False),
            _solenoid_line_seems_open(daq1[0], False),
            _solenoid_line_seems_open(daq1[2], False),
            _solenoid_line_seems_open(daq1[4], False),
            _solenoid_line_seems_open(daq1[3], False),
            _solenoid_line_seems_open(daq1[6], True),
            _solenoid_line_seems_open(daq2[0], True),
            _solenoid_line_seems_open(daq2[1], False),
            _solenoid_line_seems_open(daq1[5], False),
            _solenoid_line_seems_open(daq2[3], False),
        ]
        for i, o in enumerate(s_open):
            getattr(self.ui, f"S{i + 1}_state").setText("OPEN" if o else "CLOSED")

    def begin_vacuum_down(self):
        self.daq1, self.daq2 = full_facility_run_methods.begin_vacuum_sequence()
        self.update_solenoid_labels()

    def _bnc_gui_arm_on(self):
        try:
            bnc_box_control.arm("ON")
            self.ui.bnc_arm_state.setText("ON")
        except Exception as e:
            print("BNC arm ON failed:", e)

    def _bnc_gui_arm_off(self):
        try:
            bnc_box_control.arm("OFF")
            self.ui.bnc_arm_state.setText("OFF")
        except Exception as e:
            print("BNC arm OFF failed:", e)

    def _bnc_gui_continuous_mode(self):
        try:
            bnc_box_control.switch_preset(9)
            self.ui.bnc_mode_state.setText("Continuous (preset 9)")
        except Exception as e:
            print("BNC continuous mode failed:", e)

    def _bnc_gui_single_mode(self):
        try:
            bnc_box_control.switch_preset(12)
            self.ui.bnc_mode_state.setText("Single shot (preset 12)")
        except Exception as e:
            print("BNC single-shot mode failed:", e)

  
    stop_test = False

    def begin_testing(self, stop_test):
        button = self.ui.testautomation
        button.setEnabled(False)
        self.ui.testautomation.setStyleSheet("")
        self.ui.purgebutton.setStyleSheet("")

        # During automatic test, prevent manual pressure auto-read from interfering
        self.automation_running = True
        self.ui.driverButton.setEnabled(False)
        self.ui.start_auto_read.setEnabled(False)
        self.ui.stop_auto_read.setEnabled(False)
        # Ensure any running auto-read timers are stopped
        self.stop_auto_read()

        setpointA = float(self.ui.mfcAsetpoint.text())
        setpointB = float(self.ui.mfcBsetpoint.text())
        setpointC = float(self.ui.mfcCsetpoint.text())
        setpointC2 = float(self.ui.mfcCsetpoint_2.text())
        setpointD = float(self.ui.mfcDsetpoint.text())


        # Keep editable QLineEdit behavior: use current text if valid, then increment.
        try:
            current_test_num = int(self.ui.test_num_readout.text())
        except ValueError:
            current_test_num = 0
        self.testcount = current_test_num + 1
        self.ui.test_num_readout.setText(str(self.testcount))

        try:
            fill_time_s = float(self.ui.fill_time.text())
        except ValueError:
            fill_time_s = 0.0

        # Update vacuum gauge once when automatic test starts
        self.update_vacuum_pressure()

        #Michael change: now gives automation its own worker/thread
        automation_worker = AutomationWorker(
            setpointA, setpointB, setpointC, setpointD, setpointC2,
            fill_time_s=fill_time_s,
            testcount=self.testcount
        )
        automation_thread = QThread()
        automation_worker.moveToThread(automation_thread)
        automation_thread.started.connect(automation_worker.runauto)
        automation_worker.finished.connect(automation_thread.quit)
        automation_worker.finished.connect(lambda: self.reenable(button))
        # automation_worker.fill_phase_complete.connect(self.update_pressure)
        automation_worker.mfc_readouts_updated.connect(self.update_mfc_readouts)

        self._automation_threads.append((automation_thread, automation_worker))

        automation_thread.start()

    def begin_driver_sequence(self):
        button = self.ui.driverButton
        button.setEnabled(False)
        self.ui.testautomation.setEnabled(False)

        # Same as begin_testing: stop periodic pressure reads so they do not contend with
        # fill_and_driver_sequence (NI-DAQmx: "The specified resource is reserved").
        self.automation_running = True
        self.ui.start_auto_read.setEnabled(False)
        self.ui.stop_auto_read.setEnabled(False)
        self.stop_auto_read()

        setpointA = float(self.ui.mfcAsetpoint.text())
        setpointB = float(self.ui.mfcBsetpoint.text())
        setpointC = float(self.ui.mfcCsetpoint.text())
        setpointC_driver = float(self.ui.mfcCsetpoint_2.text())
        setpointD = float(self.ui.mfcDsetpoint.text())

        try:
            current_test_num = int(self.ui.test_num_readout.text())
        except ValueError:
            current_test_num = 0
        self.testcount = current_test_num + 1
        self.ui.test_num_readout.setText(str(self.testcount))

        try:
            fill_time_s = float(self.ui.fill_time.text())
        except ValueError:
            fill_time_s = 0.0

        try:
            driver_fill_s = float(self.ui.driver_fill_time.text())
        except ValueError:
            driver_fill_s = 0.0

        self.update_vacuum_pressure()

        driver_worker = DriverWorker(
            setpointA,
            setpointB,
            setpointC,
            setpointD,
            setpointC_driver,
            fill_time_s,
            self.testcount,
            driver_fill_s,
        )
        driver_thread = QThread()
        driver_worker.moveToThread(driver_thread)
        driver_thread.started.connect(driver_worker.run)
        driver_worker.finished.connect(driver_thread.quit)
        driver_worker.finished.connect(lambda: self.reenable(button))
        driver_worker.finished.connect(lambda: self.ui.testautomation.setEnabled(True))
        driver_worker.fill_phase_complete.connect(self.update_pressure)
        driver_worker.mfc_readouts_updated.connect(self.update_mfc_readouts)

        self._driver_threads.append((driver_thread, driver_worker))

        driver_thread.start()
    
    def ignite(self): 
        button = self.ui.igniteButton
        button.setEnabled(False)
        self.ui.testautomation.setStyleSheet("")
        self.ui.purgebutton.setStyleSheet("")
        self.ui.igniteButton.setStyleSheet("")

        testcount = self.testcount 
        ignite_worker = SolenoidWorker(0,0, testcount, self.vacuum_pressure, self.post_fill_pressure)
        ignite_thread = QThread()
        ignite_worker.moveToThread(ignite_thread)
        ignite_thread.started.connect(ignite_worker.runignite)
        ignite_worker.finished.connect(ignite_thread.quit)
        ignite_worker.finished.connect(lambda: self.reenable(button))

        self._ignite_threads.append((ignite_thread, ignite_worker))

        ignite_thread.start()

    def purge(self):
        button = self.ui.purgebutton

        button.setEnabled(False)
        self.purge_running = True
        self.ui.driverButton.setEnabled(False)
        self.ui.testautomation.setStyleSheet("")
        self.ui.purgebutton.setStyleSheet("")

        setpointA = 0.0
        setpointB = 0.0
        setpointC = 0.0
        setpointC2 = 0.0
        setpointD = 0.0

        purge_worker = AutomationWorker(setpointA, setpointB, setpointC, setpointD, setpointC2, fill_time_s=0.0)
        purge_thread = QThread()
        purge_worker.moveToThread(purge_thread)
        purge_thread.started.connect(purge_worker.runstanpurge)
        purge_worker.finished.connect(purge_thread.quit)
        purge_worker.finished.connect(lambda: self.reenable(button))
        purge_worker.mfc_readouts_updated.connect(self.update_mfc_readouts)

        self._automation_threads.append((purge_thread, purge_worker))

        purge_thread.start()

    #is run at end of fill phase
    def update_pressure(self):
        pressure = nicontrol.read_pressure()
        self.post_fill_pressure = pressure
        self.ui.pressure_readout.display(pressure)

    #is run at start of automatic test
    def update_vacuum_pressure(self):
        vacuum_pressure = nicontrol.read_vacuum_pressure() * 1000
        #print(vacuum_pressure)
        self.vacuum_pressure = vacuum_pressure
        self.ui.vacuum_pressure_readout.display(vacuum_pressure)


        #runs the audio player at designated interval if auto read is on and vacuum pressure is below threshold
        auto_on = (
            self.vacuum_pressure_timer is not None
            and self.vacuum_pressure_timer.isActive()
            and not self.automation_running
        )
        if auto_on and self._vacuum_audio_next_mono is not None:
            now = time.monotonic()
            if now >= self._vacuum_audio_next_mono:
                self._vacuum_audio_next_mono += VACUUM_AUDIO_INTERVAL_S
                if vacuum_pressure < VACUUM_AUDIO_THRESHOLD_PA:
                    threading.Thread(
                        target=audio_player.vacuum_audio_indicator, daemon=True #calls the audio player function for the vacuum in audio_player.py
                    ).start()


    #starts auto read during vacuum phase
    def start_auto_read(self):
        """Begin periodically updating vacuum and fill pressures (for manual/vacuum phase)."""
        if self.automation_running:
            return  # ignore during automatic test
        if self.vacuum_pressure_timer is None:
            self.vacuum_pressure_timer = QTimer(self)
            self.vacuum_pressure_timer.timeout.connect(self.update_vacuum_pressure)
        if self.pressure_timer is None:
            self.pressure_timer = QTimer(self)
            self.pressure_timer.timeout.connect(self.update_pressure)
        self.vacuum_pressure_timer.start(500)
        self.pressure_timer.start(500)
        self._vacuum_audio_next_mono = time.monotonic() + VACUUM_AUDIO_INTERVAL_S
        # Take an immediate reading so the user sees it without waiting
        self.update_vacuum_pressure()
        self.update_pressure()


    #stops auto read during vacuum phase
    def stop_auto_read(self):
        """Stop auto-updating pressures; displays hold last values."""
        if self.vacuum_pressure_timer is not None:
            self.vacuum_pressure_timer.stop()
        if self.pressure_timer is not None:
            self.pressure_timer.stop()
        self._vacuum_audio_next_mono = None

    #reenables the pressure auto-read controls after automatic test or purge is finished
    def reenable(self, button):
            button.setEnabled(True)
            button.setStyleSheet("")
            if button is self.ui.testautomation:
                self.automation_running = False
                self.ui.start_auto_read.setEnabled(True)
                self.ui.stop_auto_read.setEnabled(True)
                if hasattr(self.ui, "driverButton"):
                    self.ui.driverButton.setEnabled(True)
            if button is self.ui.purgebutton:
                self.purge_running = False
                if hasattr(self.ui, "driverButton"):
                    self.ui.driverButton.setEnabled(True)
            if hasattr(self.ui, "driverButton") and button is self.ui.driverButton:
                self.automation_running = False
                self.ui.start_auto_read.setEnabled(True)
                self.ui.stop_auto_read.setEnabled(True)


    def update_mfc_flow_readouts(self, flow_a, flow_b, flow_c):
        """Measured flows from Alicat serial poll → main flow LCDs."""
        self.ui.mfcAreadout.display(flow_a)
        self.ui.mfcBreadout.display(flow_b)
        self.ui.mfcCreadout.display(flow_c)

    def update_mfc_readouts(self, setpoint_a, setpoint_b, setpoint_c, _setpoint_d=0.0):
        """Last commanded MFC setpoints on mfc*_last_setpoint LCDs (not Alicat flow readouts)."""
        self.ui.mfcA_last_setpoint.display(setpoint_a)
        self.ui.mfcB_last_setpoint.display(setpoint_b)
        self.ui.mfcC_last_setpoint.display(setpoint_c)



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
    dialog.move(0,0)

    # set_console_position(0, 0, 800, 600)
    # print("Console window moved to (0,0)")
    # input("Press Enter to exit...")

    sys.exit(app.exec())






