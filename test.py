import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import numpy as np
import sys

app = QtWidgets.QApplication(sys.argv)
win = pg.PlotWidget()
win.showGrid(x=True, y=True)
win.setBackground('w')

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)
win.plot(x,y,pen='r')
win.show()
sys.exit(app.exec())