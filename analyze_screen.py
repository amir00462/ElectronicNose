import os
import sys

from PyQt5.QtGui import QIcon
from matplotlib.backends.qt_compat import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QHBoxLayout, QVBoxLayout
import lda_screen
import meta
import svm_screen
from fonts import *
import pandas as pd
from PyQt5.QtCore import pyqtSignal, QObject

class AnalyzeApp(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(1050, 800)
        self.centralwidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralwidget)

        icon = QIcon("icon.ico")
        self.setWindowIcon(icon)

        self.loadDataButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadDataButton.setGeometry(QtCore.QRect(20, 700, 1010, 40))
        self.loadDataButton.setFont(buttonFont)
        self.loadDataButton.setAutoDefault(False)
        self.loadDataButton.clicked.connect(self.loadData)

        self.svmButton = QtWidgets.QPushButton(self.centralwidget)
        self.svmButton.setGeometry(QtCore.QRect(20, 740, 504, 40))
        self.svmButton.setFont(buttonFont)
        self.svmButton.setAutoDefault(False)
        self.svmButton.clicked.connect(self.onSvmClicked)

        self.ldaButton = QtWidgets.QPushButton(self.centralwidget)
        self.ldaButton.setGeometry(QtCore.QRect(525, 740, 504, 40))
        self.ldaButton.setFont(buttonFont)
        self.ldaButton.setAutoDefault(False)
        self.ldaButton.clicked.connect(self.onLdaClicked)

        self.table = QtWidgets.QTableWidget()
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central_widget)

        layout.addWidget(self.table)
        layout.addWidget(self.loadDataButton)
        layout.addWidget(self.svmButton)
        layout.addWidget(self.ldaButton)
        self.setCentralWidget(central_widget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def loadData(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select XLSX File', os.path.dirname(__file__), "Excel Files (*.xlsx)")

        if path:
            file_name = os.path.basename(path)
            file_path = os.path.dirname(path)
            self.showData(file_path + file_name)
    def showData(self, path):
        print(path)

        self.df = pd.read_excel(path.strip())
        if self.df.size == 0:
            return

        self.df.fillna('', inplace=True)
        self.table.setRowCount(self.df.shape[0])
        self.table.setColumnCount(self.df.shape[1])
        self.table.setHorizontalHeaderLabels(self.df.columns)

        # returns pandas array object
        for row in self.df.iterrows():
            values = row[1]
            for col_index, value in enumerate(values):
                if isinstance(value, (float, int)):
                    value = '{0:0,.4f}'.format(value)
                tableItem = QTableWidgetItem(str(value))
                self.table.setItem(row[0], col_index, tableItem)

        self.table.setColumnWidth(2, 300)

    def getDataFrameFromTable(self):
        data = []

        for row in range(self.table.rowCount()):
            rowData = []
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item is not None:
                    rowData.append(item.text())
                else:
                    rowData.append("")
            data.append(rowData)

        headers = self.df.columns.tolist()
        return pd.DataFrame(data , columns=headers)

    def onSvmClicked(self):
        self.svmScreen = svm_screen.SvmAnalyze(self.getDataFrameFromTable())
        self.svmScreen.show()

    def onLdaClicked(self):
        self.ldaScreen = lda_screen.LdaAnalyze(self.getDataFrameFromTable())
        self.ldaScreen.show()

    def onRemoveButtonClicked(self):
        pass

    def onAddButtonClicked(self):
        pass

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("AnalyzeWindow", "Analyze Screen"))
        self.loadDataButton.setText(_translate("AnalyzeWindow", "Load Data"))
        self.svmButton.setText(_translate("AnalyzeWindow", "SVM"))
        self.ldaButton.setText(_translate("AnalyzeWindow", "LDA"))
