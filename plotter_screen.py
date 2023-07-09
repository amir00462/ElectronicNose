import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from joblib import dump, load
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from pyqtgraph import PlotWidget
from mlxtend.plotting import plot_decision_regions

class PlotterScreen(QtWidgets.QMainWindow):

    def __init__(self, x, y, model):
        super().__init__()
        self.setWindowTitle("SVM Model Plot")
        self.resize(800, 600)

        layout = QVBoxLayout()
        self.graphWidget = PlotWidget()
        layout.addWidget(self.graphWidget)

        self.centralWidget = QWidget(self)
        self.centralWidget.setLayout(layout)
        self.setCentralWidget(self.centralWidget)

        self.plot_results(x, y, model)


    def plot_results(self , x, y, model):
        pass