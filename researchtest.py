import tkinter as tk
from tkinter import ttk
import random
import nicontrol
import pdb
import alicatcontrol
import asyncio
from alicat import FlowController

# Prints default states of the gasses while also creating a dictionary containing actual default settings. 
def get_gui_settings():
    defaults = """
    Default Mass Flow Parameters:

    "A": {"gas": "H2", "setpoint": 0.0, "unit": "SLPM"},
    "B": {"gas": "N2", "setpoint": 0.0, "unit": "SLPM"},
    "C": {"gas": "O2", "setpoint": 0.0, "unit": "SLPM"}
    """
    print(defaults)
    return {
        "A": {"gas": "H2", "setpoint": 0.0, "unit": "SLPM"},
        "B": {"gas": "N2", "setpoint": 0.0, "unit": "SLPM"},
        "C": {"gas": "O2", "setpoint": 0.0, "unit": "SLPM"}
    }
class MFCsetup(tk.Toplevel): #This class creates a setup window for the mass flow rate controllers so that the user can choose how many they are using. 
    def __init__(self, parent, max_mfcs = 9):
        super().__init__(parent) # Initializes the MFC setup window
        self.title("MFC Setup")
        self.value = None 
        
        mfcquestion = tk.Label(self, text = "How many mass flow controllers are you using?")
        mfcquestion.pack()
        self.var = tk.IntVar(value = 3) # Default to 3 MFCs
        answer = tk.Spinbox(self, from_=1, to=max_mfcs, textvariable = self.var, width = 5)
        answer.pack() 

        button1 = tk.Button(self, text = "Ok", command = self.on_ok)
        button1.pack()
        self.grab_set() 
        self.wait_window()

    def on_ok(self):
        self.value = self.var.get()
        self.destroy()

class ChooseGas(tk.Toplevel):
    def __init__(self, parent, num_mfcs, gas_options):
        super().__init__(parent)
        self.title("Choose Gasses")
        self.selected_gasses = []
        self.vars = []
        gasquestion = tk.Label(self, text="Which gasses are currently in use? Please match your gas choice to the correct MFC.")
        gasquestion.pack(pady=5)
        gaswarning = tk.Label(self, text="*Please know the letter of each flow controller and the gas connected to it BEFORE selecting the gasses here. They must match up.*")
        gaswarning.pack(pady=5)
        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10)
        for i in range(num_mfcs):
            label = chr(ord('A') + i)
            tk.Label(frame, text=f"MFC {label}:").grid(row=i, column=0, sticky="e", padx=5, pady=2)
            var = tk.StringVar(value=gas_options[0])
            self.vars.append(var)
            cb = ttk.Combobox(frame, textvariable=var, values=gas_options, state="readonly", width=15)
            cb.grid(row=i, column=1, padx=5, pady=2)
        btn = tk.Button(self, text="OK", command=self.on_ok)
        btn.pack(pady=10)
        self.grab_set()
        self.wait_window()

    def on_ok(self):
        self.selected_gasses = [var.get() for var in self.vars]
        self.destroy()

# This is a simple GUI for a combustion chamber system with solenoids, pressure sensors, and gas inputs.
class CombustionChamberGUI:
    def __init__(self, root, num_mfcs, selected_gasses):
        self.root = root
        self.num_mfcs = num_mfcs
        self.selected_gasses = selected_gasses
        self.root.title("Combustion Chamber System")
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        self.canvas_frame = tk.Frame(self.main_frame)
        self.canvas_frame.pack(side="left", fill="both", expand=True)
        self.canvas = tk.Canvas(self.canvas_frame, width=1055, height=700, bg="white")
        self.canvas.pack()
        self.draw_sections()
        self.create_pressure_sensors()
        self.create_photo_detectors()
        self.create_solenoids()
        #pdb.set_trace()
        self.positions = [
            (28, 590), (105, 502), (103, 590),
            (152, 150), (235, 590), (935, 150),
            (775, 590), (775, 150), (835, 650),
        ]
        self.buttons = []
        for i in range(len(self.solenoids)):
            state = "OFF"
            color = "red"
            button = tk.Button(
                self.canvas,
                text=f"{state} {i+1}",
                width=4, height=1,
                font=("Arial", 7, "bold"),
                bg=color,
                command=lambda idx=i: self.toggle_button(idx)
            )
            x, y = self.positions[i]
            self.canvas.create_window(x, y, window=button)
            self.buttons.append(button)
        self.controls_frame = tk.Frame(self.main_frame)
        self.controls_frame.pack(side="left", fill="y", padx=10, pady=10)
        #self.update_button = ttk.Button(self.controls_frame, text="Manually Update Readouts", command=self.update_readouts)
        #self.update_button.pack(pady=10)
        self.create_gas_inputs()
        self.ni_states = [False] * 8  
        self.update_values_loop()
     

        # Initialize the NI-9474 digital output module, sets up main window and frames for GUI

    def toggle_button(self, index):
        solenoid = self.solenoids[index]
        solenoid['switch_state'] = not solenoid['switch_state']
        if solenoid['switch_state']:
            self.buttons[index].config(text=f"ON {index+1}", bg="green")
        else:
            self.buttons[index].config(text=f"OFF {index+1}", bg="red")
        arrow_state = solenoid['switch_state'] if solenoid['arrow_default'] else not solenoid['switch_state']
        self.draw_arrow(solenoid['x0'], solenoid['y0'], solenoid['size'], solenoid['orient'], arrow_state, index, solenoid['arrow_orient'])
        print(f"Solenoid {index} switch_state: {solenoid['switch_state']}")
        self.get_solenoid_states()

        self.ni_states[index] = solenoid['switch_state']
        sandbox.set_all_digital_outputs(self.ni_states)


    def draw_sections(self):
        self.canvas.create_rectangle(20, 250, 150, 450, outline="black", width=2)
        self.canvas.create_text(85, 235, text="Initiator", font=("Arial", 12))
        self.canvas.create_rectangle(150, 250, 775, 450, outline="black", width=2)
        self.canvas.create_text(462, 235, text="Standard", font=("Arial", 12))
        x1, y1 = 760, 320
        x2, y2 = 810, 350
        x3, y3 = 760, 380
        x4, y4 = 710, 350
        self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, outline="blue", width=2)
        self.canvas.create_rectangle(775, 250, 905, 450, outline="black", width=2)
        self.canvas.create_rectangle(800, 300, 880, 390, outline="black", width=2)
        self.canvas.create_text(840, 235, text="Optical", font=("Arial", 12))
        self.canvas.create_rectangle(905, 250, 1035, 450, outline="black", width=2)
        self.canvas.create_text(970, 235, text="Vacuum", font=("Arial", 12))
        self.canvas.create_rectangle(79, 455, 87, 480, outline="blue", width=2)
        self.canvas.create_rectangle(270, 220, 278, 245, outline="blue", width=2)
        self.canvas.create_rectangle(290, 220, 298, 245, outline="blue", width=2)
        self.canvas.create_rectangle(270, 455, 278, 480, outline="blue", width=2)
        self.canvas.create_rectangle(290, 455, 298, 480, outline="blue", width=2)
        self.canvas.create_rectangle(490, 455, 498, 480, outline="blue", width=2)
        self.canvas.create_rectangle(916, 220, 924, 245, outline="blue", width=2)
        self.canvas.create_oval(950, 50, 1000, 100, outline="black", width=2)
        # Draws graphical representations of different sections of the combustion chamber

    def create_pressure_sensors(self):
        self.initiator_pressures = []
        for i in range(3):
            self.create_sensor_entry(75, 300 + i * 60, f"(I) P{i+1}", self.initiator_pressures)
        self.standard_pressures = []
        for i in range(6):
            self.create_sensor_entry(200 + i * 100, 420, f"(S) P{i+1}", self.standard_pressures)
        self.optical_pressure = []
        self.create_sensor_entry(830, 420, "(O) P1", self.optical_pressure)
        self.vacuum_pressure = []
        self.create_sensor_entry(960, 420, "(V) P1", self.vacuum_pressure)
        #Creates labels and readouts for pressure sensors in the GUI. Values are periodically updated to mimic real sensor readings. 

    def create_photo_detectors(self):
        self.photo_detectors = []
        for i in range(4):
            self.create_sensor_entry(300 + i * 100, 300, f"(S) D{i+1}", self.photo_detectors)
            #Adds labels and readouts for photo detectors in the Standard section

    def create_sensor_entry(self, x, y, label, sensor_list):
        lbl = ttk.Label(self.canvas, text=label)
        readout = ttk.Label(self.canvas, text="0", width=5, relief="sunken", padding=(5, 5))
        sensor_list.append((lbl, readout))
        self.canvas.create_window(x - 20, y, window=lbl)
        self.canvas.create_window(x + 30, y, window=readout)
    #Creates a label and readout for each sensor, adding them to the specified sensor list for later use

    
    #BEFORE TESTING, COME BACK AND CHANGE THE NI_CHANNEL TO THE CORRECT ONE FOR THE SOLENOID, YOU DON'T KNOW WHICH ONE IT IS YET
    def create_solenoids(self):
        self.solenoids = [
            {'x0': 45, 'y0': 570, 'size': 30, 'orient': 'r', 'arrow_default': True, 'arrow_orient': 'n'},
            {'x0': 83, 'y0': 520, 'size': 30, 'orient': 'u', 'arrow_default': True, 'arrow_orient': 'n'},
            {'x0': 120, 'y0': 570, 'size': 30, 'orient': 'r', 'arrow_default': True, 'arrow_orient': 'n'},
            {'x0': 220, 'y0': 160, 'size': 30, 'orient': 'u', 'arrow_default': True, 'arrow_orient': 'r'},
            {'x0': 300, 'y0': 600, 'size': 30, 'orient': 'r', 'arrow_default': True, 'arrow_orient': 'n'},
            #{'x0': 1000, 'y0': 160, 'size': 30, 'orient': 'u', 'arrow_default': False, 'arrow_orient': 'r', 'ni_channel':5},
            {'x0': 840, 'y0': 600, 'size': 30, 'orient': 'r', 'arrow_default': True, 'arrow_orient': 'r'},
            {'x0': 840, 'y0': 160, 'size': 30, 'orient': 'r', 'arrow_default': True, 'arrow_orient': 'n'},
            #{'x0': 900, 'y0': 660, 'size': 30, 'orient': 'r', 'arrow_default': False, 'arrow_orient': 'n'},
        ]
        for i, solenoid in enumerate(self.solenoids):
            solenoid['switch_state'] = False
            x0 = solenoid['x0']
            y0 = solenoid['y0']
            size = solenoid['size']
            orient = solenoid['orient']
            arrow_orient = solenoid['arrow_orient']
            self.draw_solenoid(x0, y0, size, orient)
            arrow_state = solenoid['switch_state'] if solenoid['arrow_default'] else not solenoid['switch_state']
            self.draw_arrow(x0, y0, size, orient, arrow_state, i, arrow_orient)
        # Initializes solenoids with their positions, sizes, orientations, and arrow states.Draws solenoids and their corresponding arrows to indicate flow direction.


    def draw_solenoid(self, x0, y0, size, orient):
        if orient == 'u':
            self.canvas.create_polygon(
                x0, y0,
                x0 - size/2, y0 - size + 10,
                x0 + size/2, y0 - size + 10,
                fill='black', outline='black'
            )
            self.canvas.create_polygon(
                x0, y0,
                x0 - size/2, y0 + size - 10,
                x0 + size/2, y0 + size - 10,
                fill='black', outline='black'
            )
            self.canvas.create_rectangle(
                x0 - (size*0.44) - 10, y0 - (size*0.44)/2,
                x0 - 10, y0 + (size*0.44)/2,
                fill='black', outline='black'
            )
        elif orient == 'r':
            self.canvas.create_polygon(
                x0, y0,
                x0 + 10 - size, y0 + size/2,
                x0 + 10 - size, y0 - size/2,
                fill='black', outline='black'
            )
            self.canvas.create_polygon(
                x0, y0,
                x0 - 10 + size, y0 + size/2,
                x0 - 10 + size, y0 - size/2,
                fill='black', outline='black'
            )
            self.canvas.create_rectangle(
                x0 - (size*0.5)/2, y0 - 10 - (size*0.5),
                x0 + (size*0.5)/2, y0 - 5 - (size*0.5)/2,
                fill='black', outline='black'
            )
    # Draws a solenoid at the specified position with the given size and orientation.
    # Draws an arrow to indicate flow direction based on solenoid state and orientation.
    def draw_arrow(self, x0, y0, size, orient, flow_on, index, arrow_orient):
        tag = f"arrow{index}"
        self.canvas.delete(tag)
        color = "green" if flow_on else "gray"
        if orient == 'r':
            if arrow_orient == 'n':
                start_x = x0 - size/2
                end_x = x0 + size/2
                self.canvas.create_line(start_x, y0, end_x, y0, arrow=tk.LAST, fill=color, width=2, tags=tag)
            else:
                start_x = x0 + size/2
                end_x = x0 - size/2
                self.canvas.create_line(start_x, y0, end_x, y0, arrow=tk.LAST, fill=color, width=2, tags=tag)
        elif orient == 'u':
            if arrow_orient == 'n':
                start_y = y0 + size/2
                end_y = y0 - size/2
                self.canvas.create_line(x0, start_y, x0, end_y, arrow=tk.LAST, fill=color, width=2, tags=tag)
            else:
                start_y = y0 - size/2
                end_y = y0 + size/2
                self.canvas.create_line(x0, start_y, x0, end_y, arrow=tk.LAST, fill=color, width=2, tags=tag)
    # Updates the readouts of pressure sensors and photo detectors with simulated values.
    # Draws arrows to indicate flow direction based on solenoid states.
    def update_readouts(self):
        for _, readout in self.initiator_pressures:
            simulated_value = random.randint(50, 150)
            readout.config(text=str(simulated_value))
        for _, readout in self.standard_pressures:
            simulated_value = random.randint(70, 160)
            readout.config(text=str(simulated_value))
        simulated_value = random.randint(80, 120)
        self.optical_pressure[0][1].config(text=str(simulated_value))
        simulated_value = random.randint(30, 80)
        self.vacuum_pressure[0][1].config(text=str(simulated_value))
        for _, readout in self.photo_detectors:
            simulated_value = random.randint(10, 30)
            readout.config(text=str(simulated_value))
    # Periodically updates the readouts every second.
    def update_values_loop(self):
        self.update_readouts()
        self.root.after(1000, self.update_values_loop)
    # Creates gas input fields for the combustion chamber, allowing users to set gas types, setpoints, and units.
    def create_gas_inputs(self):
        self.gas_frame = ttk.LabelFrame(self.controls_frame, text="Gas Settings", padding=(10, 10))
        self.gas_frame.pack(pady=10)
        self.gas_vars = {}
        self.setpoint_vars = {}
        self.unit_vars = {}
        gas_options = ['Air', 'Ar', 'CH4', 'CO', 'CO2', 'C2H6', 'H2', 'He',
                       'N2', 'N2O', 'Ne', 'O2', 'C3H8', 'n-C4H10', 'C2H2',
                       'C2H4', 'i-C2H10', 'Kr', 'Xe', 'SF6', 'C-25', 'C-10',
                       'C-8', 'C-2', 'C-75', 'A-75', 'A-25', 'A1025', 'Star29',
                       'P-5']
        settings = get_gui_settings()
        row = 0
        ttk.Label(self.gas_frame, text="Label").grid(row=row, column=0, padx=5, pady=5)
        ttk.Label(self.gas_frame, text="Gas").grid(row=row, column=1, padx=5, pady=5)
        ttk.Label(self.gas_frame, text="Setpoint").grid(row=row, column=2, padx=5, pady=5)
        ttk.Label(self.gas_frame, text="Unit").grid(row=row, column=3, padx=5, pady=5)
        row += 1
        for i in range(self.num_mfcs):
            label = chr(ord('A') + i)
            ttk.Label(self.gas_frame, text=label).grid(row=row, column=0, padx=5, pady=5)
            default_gas = self.selected_gasses[i] if self.selected_gasses and i < len(self.selected_gasses) else gas_options[0]
            gas_var = tk.StringVar(value=default_gas)
            setpoint_var = tk.DoubleVar(value=0.0)
            unit_var = tk.StringVar(value="SLPM")
            gas_entry = ttk.Combobox(self.gas_frame, textvariable=gas_var, width=10, values=gas_options, state="readonly")
            gas_entry.grid(row=row, column=1, padx=5, pady=5)
            setpoint_entry = ttk.Entry(self.gas_frame, textvariable=setpoint_var, width=10)
            setpoint_entry.grid(row=row, column=2, padx=5, pady=5)
            unit_entry = ttk.Entry(self.gas_frame, textvariable=unit_var, width=10)
            unit_entry.grid(row=row, column=3, padx=5, pady=5)
            self.gas_vars[label] = gas_var
            self.setpoint_vars[label] = setpoint_var
            self.unit_vars[label] = unit_var
            row += 1
        save_btn = ttk.Button(self.gas_frame, text="Save Gas Settings", command=self.save_gas_settings)
        save_btn.grid(row=row, column=0, columnspan=4, pady=10)
        # New Reset Button to zero only the 4 mass flow controllers (A, B, C, D)
        reset_btn = ttk.Button(self.gas_frame, text="Reset Mass Flow", command=self.reset_mass_flow)
        reset_btn.grid(row=row+1, column=0, columnspan=4, pady=10)
    # Saves the gas settings from the input fields and prints them to the console.

   
    def save_gas_settings(self):
        print("Saved!")
        for label in self.gas_vars.keys():
            gas = self.gas_vars[label].get()
            setpoint = self.setpoint_vars[label].get()
            unit = self.unit_vars[label].get()
            print(f"{label}: {{'gas': '{gas}', 'setpoint': {setpoint}, 'unit': '{unit}'}}")
            async def set_flow_rate(label, setpoint):
                async with FlowController(address = 'COM3', unit = label) as mfc:
                    await mfc.set_flow_rate(setpoint)
                    print(f'Set to {setpoint} SLPM for controller {unit}')
                    await asyncio.sleep(1)
            asyncio.run(set_flow_rate(label,setpoint))

        print("")
    # Resets the mass flow controllers to zero and prints the current settings.
    def reset_mass_flow(self):
        self.setpoint_vars['A'].set(0.0)
        self.setpoint_vars['B'].set(0.0)
        self.setpoint_vars['C'].set(0.0)
        #self.setpoint_vars['D'].set(0.0)
        print("Mass flow controllers reset")
        for label in self.gas_vars.keys():
            gas = self.gas_vars[label].get()
            setpoint = self.setpoint_vars[label].get()
            unit = self.unit_vars[label].get()
            print(f"{label}: {{'gas': '{gas}', 'setpoint': {setpoint}, 'unit': '{unit}'}}")
            async def zero():
               async with FlowController(address = 'COM3', unit = label) as mfc:
                   await mfc.set_flow_rate(0.0)
                   print('Mass flow controllers have been reset to 0.0 SLPM')
            asyncio.run(zero())
        print("")
    # Retrieves the states of the solenoids and prints them to the console.
    def get_solenoid_states(self):
        states = [s['switch_state'] for s in self.solenoids]
        print("Solenoid States:", states)
        return states

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide main window during setup dialog
    dialog = MFCsetup(root)
    num_mfcs = dialog.value if dialog.value else 3  # Default to 3 if dialog closed
    gas_options = ['Air', 'Ar', 'CH4', 'CO', 'CO2', 'C2H6', 'H2', 'He',
                   'N2', 'N2O', 'Ne', 'O2', 'C3H8', 'n-C4H10', 'C2H2',
                   'C2H4', 'i-C2H10', 'Kr', 'Xe', 'SF6', 'C-25', 'C-10',
                   'C-8', 'C-2', 'C-75', 'A-75', 'A-25', 'A1025', 'Star29',
                   'P-5']
    gas_dialog = ChooseGas(root, num_mfcs, gas_options)
    selected_gasses = gas_dialog.selected_gasses
    print("Selected Gasses:", selected_gasses)
    root.deiconify()  # Show main window
    app = CombustionChamberGUI(root, num_mfcs,selected_gasses)
    root.mainloop()

