import os
import sys
from queue import Queue
from PyQt5.QtGui import QIcon
from matplotlib.backends.qt_compat import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QHBoxLayout, QVBoxLayout
import lda_screen
import meta
from joblib import dump, load
import svm_screen
from fonts import *
import pandas as pd
from PyQt5.QtCore import pyqtSignal, QObject

class PredictScreen(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(1050, 900)
        self.centralwidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralwidget)
        self.logs_queue = Queue(maxsize=1000)

        icon = QIcon("icon.ico")
        self.setWindowIcon(icon)

        self.loadDataButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadDataButton.setGeometry(QtCore.QRect(40, 700, 1010, 40))
        self.loadDataButton.setFont(buttonFont)
        self.loadDataButton.setAutoDefault(False)
        self.loadDataButton.clicked.connect(self.loadData)

        self.loadModelButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadModelButton.setGeometry(QtCore.QRect(40, 700, 1010, 40))
        self.loadModelButton.setFont(buttonFont)
        self.loadModelButton.setAutoDefault(False)
        self.loadModelButton.clicked.connect(self.loadModel)

        self.logSection = QtWidgets.QTextBrowser(self.centralwidget)
        self.logSection.setGeometry(QtCore.QRect(40, 260, 1010, 200))
        self.logSection.setFont(logFont)

        self.PredictButton = QtWidgets.QPushButton(self.centralwidget)
        self.PredictButton.setGeometry(QtCore.QRect(20, 740, 504, 40))
        self.PredictButton.setFont(buttonFont)
        self.PredictButton.setAutoDefault(False)
        self.PredictButton.clicked.connect(self.onPredictClicked)

        self.table = QtWidgets.QTableWidget()
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central_widget)

        layout.addWidget(self.table, stretch=4)
        layout.addWidget(self.logSection , stretch=1)
        layout.addWidget(self.loadDataButton)
        layout.addWidget(self.loadModelButton)
        layout.addWidget(self.PredictButton)
        self.setCentralWidget(central_widget)

        self.retranslateUi()
        self.add_log(self.logs_queue, "Make sure that features = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'] and we use \'class_q\' for prediction (non,sample)")
        self.add_log(self.logs_queue, "Important = your data or model address path should not contains whiteSpace\n")
        QtCore.QMetaObject.connectSlotsByName(self)

    def enqueue(self, queue, clause):
        if queue.full():
            queue.get()

        queue.put(clause)
    def add_log(self, queue, clause):
        self.enqueue(queue, clause)
        self.logSection.setText('\n'.join(list(self.logs_queue.queue)))
    def loadData(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select XLSX File', os.path.dirname(__file__), "Excel Files (*.xlsx)")

        if path:
            file_name = os.path.basename(path)
            file_path = os.path.dirname(path)
            self.add_log(self.logs_queue, "Excel data -> " + file_path + file_name)
            self.showData(file_path + file_name)
    def loadModel(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Trained Model', os.path.dirname(__file__), "Joblib Files (*.joblib)")

        if path:
            file_name = os.path.basename(path)
            file_path = os.path.dirname(path)
            self.add_log(self.logs_queue, "Trained Model -> " + file_path + file_name)
            self.saveModel(file_path + file_name)
    def saveModel(self , path):
        self.loaded_model = load(path)
    def showData(self, path):

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

    def onPredictClicked(self):
        self.excel = self.getDataFrameFromTable()
        features = self.excel[['S1', 'S2', 'S3', 'S4', 'S5', 'S6']]

        self.add_log(self.logs_queue, "\n")
        predictions = self.loaded_model.predict(features)
        index = 1
        for prediction in predictions:
            if prediction == 'non':
                self.add_log(self.logs_queue, "Prediction for row " + str(index) + " is 'non'")
            elif prediction == 'sample':
                self.add_log(self.logs_queue, "Prediction for this row " + str(index) + " is 'sample'")

            index += 1

        accuracy = self.loaded_model.score(features, self.excel['class_q'])
        self.add_log(self.logs_queue, f"\nAccuracy of this prediction: {accuracy}")

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("PredictWindow", "Predict Screen"))
        self.loadDataButton.setText(_translate("PredictWindow", "Load test data"))
        self.loadModelButton.setText(_translate("PredictWindow", "Load trained model"))
        self.PredictButton.setText(_translate("PredictWindow", "Predict"))
