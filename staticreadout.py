import matplotlib.pyplot as plt
import numpy as np

applied_pressure = [0.0721, 1.4998, 3.0002, 4.5000, 6.0000, 7.5000, 9.0000, 10.4999, 12.0000, 13.5000, 15.0000] #in psi
transducer_output = [0.0323, 0.9849, 1.9849, 2.9855, 3.9872, 4.9871, 5.9873, 6.9873, 7.9876, 8.9879, 9.9879]

errors = [0.000, 0.005, -0.002, 0.002, 0.015, 0.010, 0.009, 0.005, 0.004, 0.004, 0.000] #Nonlinearity Errors

coefficients = np.polyfit(transducer_output, applied_pressure, 1) #Linear fit

m = coefficients[0]
b = coefficients[1]

print(f"Linear fit coefficients: m = {m:.4f}, b = {b:.4f}, y = {m:.4f}x+{b:.4f}")

y = m*np.array(transducer_output)+b

plt.scatter(transducer_output, applied_pressure, color='r', label='Data Points')
plt.plot(transducer_output, y, color = 'blue')
plt.xlabel("Applied Pressure (psi)")
plt.ylabel("Transducer Output (VDC)")
plt.title("Setra Static Pressure Transducer Calibration Data")

plt.grid(True)

plt.show()