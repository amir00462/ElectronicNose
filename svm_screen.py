import os
import sys
from matplotlib.backends.qt_compat import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QHBoxLayout, QVBoxLayout
import meta
from fonts import *
import pandas as pd
from PyQt5.QtCore import pyqtSignal, QObject

class SvmAnalyze( QtWidgets.QMainWindow ):

    def __init__(self , newDataFrame):
        super().__init__()
        self.resize(1050, 800)
        self.centralwidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralwidget)

        self.dataFrame = newDataFrame
        print(self.dataFrame)

        self.loadDataButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadDataButton.setGeometry(QtCore.QRect(20, 700, 1010, 40))
        self.loadDataButton.setFont(buttonFont)
        self.loadDataButton.setAutoDefault(False)
        self.loadDataButton.clicked.connect(self.loadData)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)


    def loadData(self):
        pass

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("SVM", "SVM Analyze"))
        self.loadDataButton.setText(_translate("SVM", "Load Data"))
