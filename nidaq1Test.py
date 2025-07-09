import nidaqmx
from nidaq1 import NI9474Controller
controller = NI9474Controller()

z = controller.set_line(3, True)
print(z)

sal = [True, False, True, False, True, False, True, False]
b = controller.set_all_lines(sal)
print(b)

lin = [0, 2, 4, 6]
states = [True, False, True, False]
h = controller.set_some_lines(lin, states)
print(h)