import tkinter as tk
from tkinter import ttk
import random
import asyncio
from alicat import FlowController
import pdb

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
        gaswarning1 = tk.Label(self, text = "You also must know the com port of the MFCs before using this program. If you don't, you can find it in the flowvision software when searching for the devices.")
        gaswarning1.pack(pady=5)
        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10)
        for i in range(num_mfcs):
            label = chr(ord('A') + i)
            tk.Label(frame, text=f"MFC {label}:").grid(row=i, column=0, sticky="e", padx=5, pady=2)
            var = tk.StringVar(value=gas_options[0])
            self.vars.append(var)
            cb = ttk.Combobox(frame, textvariable=var, values=gas_options, state="readonly", width=15)
            cb.grid(row=i, column=1, padx=5, pady=2)
        comlist = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9']
        self.com_var = tk.StringVar(value='COM1')
        tk.Label(frame, text="COM Port:").grid(row=num_mfcs, column=0, sticky="e", padx=5, pady=10)
        cb2 = ttk.Combobox(frame, textvariable=self.com_var, values=comlist, state="readonly", width=15)
        cb2.grid(row=num_mfcs, column=1, padx=5, pady=10)
        btn = tk.Button(self, text="OK", command=self.on_ok)
        btn.pack(pady=10)
        self.grab_set()
        self.wait_window()
    def on_ok(self):
        self.selected_gasses = [var.get() for var in self.vars]
        self.selected_com = self.com_var.get()
        self.destroy()

class mfcGUI:
    def __init__(self, root, num_mfcs, selected_gasses):
        self.root = root
        self.num_mfcs = num_mfcs
        self.selected_gasses = selected_gasses
        self.root.title("MFC Control System")
        self.controls_frame = tk.Frame()
        self.controls_frame.pack(padx=10, pady=10)
        self.create_gas_inputs()

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
                async with FlowController(address = selected_com, unit = label) as mfc:
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
               async with FlowController(address = selected_com, unit = label) as mfc:
                   await mfc.set_flow_rate(0.0)
                   print('Mass flow controllers have been reset to 0.0 SLPM')
            asyncio.run(zero())
        print("")

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
    selected_com = gas_dialog.selected_com
    print("Selected Gasses:", selected_gasses)
    root.deiconify()  # Show main window
    app = mfcGUI(root, num_mfcs, selected_gasses)
    root.mainloop()