
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.qt_compat import QtWidgets, QtCore, QtGui
from matplotlib.figure import Figure

class ChartWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1116, 830)
        self.centralwidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralwidget)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate

        self.setWindowTitle(_translate("MainWindow", "MainWindow"))

