import tkinter as tk
import tkinter.ttk as ttk

window = tk.Tk() #Should cause window to be created and show up

greeting = tk.ttk.Label(text="How many mass flow rate controllers are you using?") #Creates what is called a label widget
greeting.pack()

pregunta = tk.Entry()
pregunta.pack()
def retrieve_data():
	entered_text = pregunta.get()
	print("entered test:", entered_text)

button = tk.Button(window, text = "Get Data", command = retrieve_data())
button.pack()
button.bind("<Button-1>", lambda event: retrieve_data()) #Left mouse click 

pregunta.bind("<Return>", lambda event: retrieve_data())

window.mainloop()
#This entire series of codde creates a window with a label widget. You MUST end with window.mainloop() to open the window

