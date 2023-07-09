import time

from fonts import *
from PyQt5.QtGui import QIcon
from matplotlib.backends.qt_compat import QtWidgets, QtCore
from sklearn.metrics import precision_score, recall_score, f1_score
from queue import Queue
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, cross_val_score
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from joblib import dump, load
import plotter_screen


class SvmAnalyze(QtWidgets.QMainWindow):

    def __init__(self, newDataFrame):
        super().__init__()
        self.resize(1050, 822)
        self.centralwidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralwidget)
        self.logs_queue = Queue(maxsize=1000)

        icon = QIcon("icon.ico")
        self.setWindowIcon(icon)

        self.data = newDataFrame
        columns = self.data.columns.tolist()
        self.columns_formatted = str(columns)
        print(self.columns_formatted)

        # - - - - - - - - - -

        self.labelColumns = QtWidgets.QLabel(self.centralwidget)
        self.labelColumns.setGeometry(QtCore.QRect(40, 40, 900, 20))
        self.labelColumns.setFont(labelFont)

        # - - - - - - - - - -

        self.labelPrediction = QtWidgets.QLabel(self.centralwidget)
        self.labelPrediction.setGeometry(QtCore.QRect(40, 90, 300, 40))
        self.labelPrediction.setFont(labelFont)

        self.textEditPrediction = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditPrediction.setGeometry(QtCore.QRect(340, 90, 670, 35))
        self.textEditPrediction.setFont(textEditFontPrediction)

        # - - - - - - - - - -

        self.labelClassification = QtWidgets.QLabel(self.centralwidget)
        self.labelClassification.setGeometry(QtCore.QRect(40, 180, 300, 40))
        self.labelClassification.setFont(labelFont)

        self.textEditClassification = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditClassification.setGeometry(QtCore.QRect(340, 190, 670, 35))
        self.textEditClassification.setFont(textEditFontPrediction)

        # - - - - - - - - - -

        self.logSvm = QtWidgets.QTextBrowser(self.centralwidget)
        self.logSvm.setGeometry(QtCore.QRect(40, 260, 970, 465))
        self.logSvm.setFont(logFont)

        # - - - - - - - - - -

        self.textEditKernel = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditKernel.setGeometry(QtCore.QRect(282, 730, 240, 40))
        self.textEditKernel.setFont(textEditFontPrediction)

        self.textEditGamma = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditGamma.setGeometry(QtCore.QRect(524, 730, 240, 40))
        self.textEditGamma.setFont(textEditFontPrediction)

        self.textEditCs = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditCs.setGeometry(QtCore.QRect(766, 730, 240, 40))
        self.textEditCs.setFont(textEditFontPrediction)

        self.textEditKernel.setText("Enter Kernel")
        self.textEditGamma.setText("Enter Gamma")
        self.textEditCs.setText("Enter C")
        self.textEditCs.setAlignment(QtCore.Qt.AlignCenter)
        self.textEditGamma.setAlignment(QtCore.Qt.AlignCenter)
        self.textEditKernel.setAlignment(QtCore.Qt.AlignCenter)

        self.gridSearchButton = QtWidgets.QPushButton(self.centralwidget)
        self.gridSearchButton.setGeometry(QtCore.QRect(40, 730, 240, 40))
        self.gridSearchButton.setFont(buttonFont)
        self.gridSearchButton.setAutoDefault(False)
        self.gridSearchButton.clicked.connect(self.gridSearchTap)

        self.svmButton = QtWidgets.QPushButton(self.centralwidget)
        self.svmButton.setGeometry(QtCore.QRect(40, 772, 970, 40))
        self.svmButton.setFont(buttonFont)
        self.svmButton.setAutoDefault(False)
        self.svmButton.clicked.connect(self.svmAlgorithm)

        # - - - - - - - - - -

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def gridSearchTap(self):
        # self.add_log(self.logs_queue, Y)
        X = self.data[str(self.textEditPrediction.toPlainText()).split(',')].values
        Y = self.data[str(self.textEditClassification.toPlainText())]

        # Tunable 80-20 percent data split for train-test
        test_size = 0.2
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(X, Y, test_size=test_size,
                                                                                random_state=42)
        self.add_log(self.logs_queue, "\nWe are using 80-20 percent data split for train-test...")

        self.add_log(self.logs_queue, "\nGrid Search using SVC:")
        self.add_log(self.logs_queue,
                     "kernels = ['linear', 'poly', 'rbf', 'sigmoid']\ngammas = [0.1, 1, 10]\nCs = [0.1, 1, 10]\n")

        # Iterate over the combinations of kernels, gamma, and C
        kernels = ['linear', 'poly', 'rbf', 'sigmoid']
        gammas = [0.1, 1, 10]
        Cs = [0.1, 1, 10]
        for kernel in kernels:
            for gamma in gammas:
                for C in Cs:
                    # Create an instance of SVC with the current kernel, gamma, and C, and fit the training data
                    svc = SVC(kernel=kernel, gamma=gamma, C=C)
                    svc.fit(self.X_train, self.Y_train)

                    # Make predictions on the testing data
                    y_pred = svc.predict(self.X_test)

                    # Calculate and print the accuracy score
                    accuracy = accuracy_score(self.Y_test, y_pred)
                    self.add_log(self.logs_queue, f'Kernel: {kernel}, Gamma: {gamma}, C: {C}, Accuracy: {accuracy}')

        self.add_log(self.logs_queue, "\nGridSearch finished, now choose your config and then tap analyze")

    def svmAlgorithm(self):
        kernel = str(self.textEditKernel.toPlainText())
        gamma = float(str(self.textEditGamma.toPlainText()))
        c = float(str(self.textEditCs.toPlainText()))

        self.add_log(self.logs_queue, "\n\n\nUsing SVC classifier with your config...\n")
        svclassifier = SVC(kernel=kernel, degree=3, gamma=gamma, C=c, decision_function_shape='ovo', probability=True)

        self.add_log(self.logs_queue, "Training data...\n")
        svclassifier.fit(self.X_train, self.Y_train)

        self.add_log(self.logs_queue, "Save Trained model into \'svm_model.joblib\'\n")
        dump(svclassifier, 'svm_model.joblib')

        # Load the model from the file
        loaded_model = load('svm_model.joblib')

        # Make predictions on the testing data using the loaded model
        self.add_log(self.logs_queue, "Predict 20 percent of data, using trained model...\n")
        y_pred = loaded_model.predict(self.X_test)

        # Calculate and print the accuracy score
        self.add_log(self.logs_queue,
                     "\n\nResult -> Accuracy and Classification report: \n(Also you can find report in \'svm_report.txt\')\n")

        accuracy = accuracy_score(self.Y_test, y_pred)
        self.add_log(self.logs_queue, f'Accuracy: {accuracy}\n')

        # self.plot_window = plotter_screen.PlotterScreen(self.X_train, self.Y_train , loaded_model)
        # self.plot_window.show()

    def enqueue(self, queue, clause):
        if queue.full():
            queue.get()

        queue.put(clause)

    def add_log(self, queue, clause):
        self.enqueue(queue, clause)
        self.logSvm.setText('\n'.join(list(self.logs_queue.queue)))

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("SVM", "SVM Analyze"))
        self.labelColumns.setText(_translate("SVM", "DataSet Columns : " + self.columns_formatted))
        self.labelPrediction.setText(_translate("SVM", "Prediction Columns:\nexample: S1,S2,S3,S4,S5,S6"))
        self.labelClassification.setText(_translate("SVM", "Classification Column:\nexample: class_q"))
        self.svmButton.setText(_translate("SVM", "SVM Analyze"))
        self.gridSearchButton.setText(_translate("SVM", "Grid Search"))
        self.add_log(self.logs_queue,
                     "1. Choose prediction and classification columns\n2. tap grid search button\n3. write best config in below inputs\n4. tap analyze button\n 5. analyze will be plotted and trained data will save at same folder \'svm.joblib\'")
        self.textEditPrediction.setText(_translate("SVM", "S1,S2,S3,S4,S5,S6"))
        self.textEditClassification.setText(_translate("SVM", "class_q"))
